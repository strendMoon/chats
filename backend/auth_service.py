import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from config import settings


async def _request_json(url: str, access_token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    query = urllib.parse.urlencode(params or {}, doseq=True)
    full_url = f"{url}?{query}" if query else url
    req = urllib.request.Request(
        full_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"YouTube API request failed: {exc.code} {body}") from exc
    except Exception as exc:
        raise RuntimeError(f"YouTube API request failed: {exc}") from exc


async def exchange_code_for_token(code: str, redirect_uri: str) -> dict[str, Any]:
    data = urllib.parse.urlencode(
        {
            "code": code,
            "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
            "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
    ).encode("utf-8")

    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Google token exchange failed: {exc.code} {body}") from exc
    except Exception as exc:
        raise RuntimeError(f"Google token exchange failed: {exc}") from exc


async def fetch_google_user_info(access_token: str) -> dict[str, Any]:
    req = urllib.request.Request(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Google userinfo failed: {exc.code} {body}") from exc
    except Exception as exc:
        raise RuntimeError(f"Google userinfo failed: {exc}") from exc


async def fetch_youtube_channel_data(access_token: str) -> dict[str, Any]:
    data = await _request_json(
        "https://www.googleapis.com/youtube/v3/channels",
        access_token,
        {"part": "snippet,statistics,contentDetails", "mine": "true", "maxResults": "1"},
    )
    items = data.get("items", [])
    return {"channel": items[0] if items else None}


async def fetch_youtube_live_broadcasts(access_token: str) -> dict[str, Any]:
    data = await _request_json(
        "https://www.googleapis.com/youtube/v3/liveBroadcasts",
        access_token,
        {"part": "snippet,contentDetails,status", "mine": "true", "maxResults": "5"},
    )
    items = data.get("items", [])
    return {"broadcasts": items}


async def fetch_youtube_live_chat(access_token: str, live_chat_id: str) -> dict[str, Any]:
    data = await _request_json(
        "https://www.googleapis.com/youtube/v3/liveChatMessages",
        access_token,
        {"liveChatId": live_chat_id, "part": "snippet,authorDetails", "maxResults": "20"},
    )
    return {"messages": data.get("items", []), "available": True, "reason": None, "live_chat_id": live_chat_id}


async def fetch_youtube_data(access_token: str) -> dict[str, Any]:
    channel_data = await fetch_youtube_channel_data(access_token)
    broadcasts_data = await fetch_youtube_live_broadcasts(access_token)
    broadcasts = broadcasts_data.get("broadcasts", [])
    stream = broadcasts[0] if broadcasts else None
    live_chat = {
        "messages": [],
        "available": False,
        "reason": "Чат будет доступен только для активной трансляции. Откройте эфир или проверьте, что у трансляции есть liveChatId.",
        "live_chat_id": None,
    }

    if stream:
        lifecycle = stream.get("status", {}).get("lifeCycleStatus")
        if lifecycle != "live":
            live_chat = {
                "messages": [],
                "available": False,
                "reason": f"Трансляция сейчас в статусе '{lifecycle or 'unknown'}'. Для live chat нужен активный эфир.",
                "live_chat_id": stream.get("contentDetails", {}).get("liveChatId"),
            }
        else:
            live_chat_id = stream.get("contentDetails", {}).get("liveChatId")
            if live_chat_id:
                try:
                    live_chat = await fetch_youtube_live_chat(access_token, live_chat_id)
                except Exception as exc:
                    live_chat = {
                        "messages": [],
                        "available": False,
                        "reason": f"YouTube API вернул ошибку для live chat: {exc}",
                        "live_chat_id": live_chat_id,
                    }
            else:
                live_chat = {
                    "messages": [],
                    "available": False,
                    "reason": "У активной трансляции пока нет liveChatId. Это обычно значит, что YouTube ещё не открыл чат для эфира.",
                    "live_chat_id": None,
                }

    return {
        "connected": True,
        "channel": channel_data.get("channel"),
        "stream": stream,
        "live_chat": live_chat,
        "live_chat_url": "https://studio.youtube.com/live_chat?is_popout=1",
    }
