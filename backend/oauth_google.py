import urllib.parse
from config import settings

def generate_google_oauth_redirect_url(client_id: str, redirect_uri: str, scope: str) -> str:
    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:8000/auth/google",
        "response_type": "code",
        "scope": " ".join([
            "https://www.googleapis.com/auth/dataportability.youtube.channel",
            "https://www.googleapis.com/auth/dataportability.youtube.subscriptions",
            "https://www.googleapis.com/auth/dataportability.youtube.comments",
            "https://www.googleapis.com/auth/dataportability.youtube.live_chat",
            "openid",
            "email",
            "profile",     
        ]),
        "access_type": "offline",
    }

    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    response_type = "code"
    return f"{base_url}?{query_string}"