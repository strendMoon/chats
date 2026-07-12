import urllib.parse

from config import settings


def _build_google_oauth_url(scopes: list[str], redirect_uri: str, state: str | None = None) -> str:
    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
    }

    if state:
        query_params["state"] = state

    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    return f"{settings.OAUTH_GOOGLE_BASE_URI}?{query_string}"


def generate_google_oauth_redirect_url() -> str:
    return _build_google_oauth_url(
        scopes=["openid", "email", "profile"],
        redirect_uri=settings.OAUTH_GOOGLE_REDIRECT_URI,
    )


def generate_youtube_oauth_redirect_url(state: str = "youtube") -> str:
    return _build_google_oauth_url(
        scopes=[
            # "https://www.googleapis.com/auth/dataportability.youtube.channel",
            # "https://www.googleapis.com/auth/dataportability.youtube.subscriptions",
            # "https://www.googleapis.com/auth/dataportability.youtube.comments",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube.force-ssl",
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtubepartner",
            # "https://www.googleapis.com/auth/dataportability.youtube.live_chat",
        ],
        redirect_uri=settings.OAUTH_GOOGLE_YOUTUBE_REDIRECT_URI,
        state=state,
    )


# https://www.googleapis.com/auth/youtube.upload
# https://www.googleapis.com/auth/youtube
# https://www.googleapis.com/auth/youtubepartner
# https://www.googleapis.com/auth/youtube.force-ssl