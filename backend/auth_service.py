import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from config import settings


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
