import urllib.parse

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse

from auth_service import exchange_code_for_token, fetch_google_user_info
from auth_utils import create_access_token, decode_access_token
from config import settings
from database import get_user_by_google_id, get_user_by_id, upsert_user
from oauth_google import (
    generate_google_oauth_redirect_url,
    generate_youtube_oauth_redirect_url,
)

router = APIRouter(prefix="/auth")


def _build_frontend_redirect(
    error: str | None = None,
    state: str | None = None,
    provider: str | None = None,
    success: bool = False,
) -> str:
    params: dict[str, str] = {}
    if error:
        params["auth_error"] = error
    if state:
        params["state"] = state
    if provider:
        params["provider"] = provider
    if success:
        params["auth_success"] = "1"

    query = urllib.parse.urlencode(params)
    return f"http://localhost:5173/{f'?{query}' if query else ''}"


@router.get("/google/url")
def get_google_oauth_redirect_url():
    url = generate_google_oauth_redirect_url()
    return RedirectResponse(url=url, status_code=302)


@router.get("/google/youtube/url")
def get_youtube_oauth_redirect_url():
    url = generate_youtube_oauth_redirect_url()
    return RedirectResponse(url=url, status_code=302)


@router.get("/google/callback")
async def google_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
):
    if error:
        return JSONResponse(
            {"error": error, "error_description": error_description or "Google authorization failed"},
            status_code=400,
        )

    if not code:
        return RedirectResponse(url=_build_frontend_redirect("missing_code", state), status_code=302)

    try:
        token_data = await exchange_code_for_token(code, settings.OAUTH_GOOGLE_REDIRECT_URI)
        user_info = await fetch_google_user_info(token_data["access_token"])
    except Exception as exc:
        return RedirectResponse(url=_build_frontend_redirect(str(exc), state), status_code=302)

    user_payload = {
        "google_id": user_info["sub"],
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
        "google_access_token": token_data.get("access_token"),
        "google_refresh_token": token_data.get("refresh_token"),
    }
    user_id = upsert_user(user_payload)
    token = create_access_token(user_id)

    response = RedirectResponse(url=_build_frontend_redirect(None, state, provider="google", success=True), status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return response


@router.get("/google/youtube/callback")
async def youtube_callback(code: str | None = None, state: str | None = None, request: Request = None):
    if not code:
        return JSONResponse({"error": "Missing YouTube authorization code"}, status_code=400)

    token = request.cookies.get("access_token") if request else None
    if not token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    payload = decode_access_token(token)
    if not payload:
        return JSONResponse({"error": "Invalid token"}, status_code=401)

    user = get_user_by_id(int(payload["sub"]))
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

    try:
        token_data = await exchange_code_for_token(code, settings.OAUTH_GOOGLE_YOUTUBE_REDIRECT_URI)
        user_payload = {
            "id": user["id"],
            "youtube_access_token": token_data.get("access_token"),
            "youtube_refresh_token": token_data.get("refresh_token"),
        }
        upsert_user(user_payload)
    except Exception as exc:
        return RedirectResponse(
            url=_build_frontend_redirect(str(exc), state, provider="youtube", success=False),
            status_code=302,
        )

    return RedirectResponse(url=_build_frontend_redirect(None, state, provider="youtube", success=True), status_code=302)


@router.get("/me")
def me(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return JSONResponse({"authenticated": False}, status_code=401)

    payload = decode_access_token(token)
    if not payload:
        return JSONResponse({"authenticated": False}, status_code=401)

    user = get_user_by_id(int(payload["sub"]))
    if not user:
        return JSONResponse({"authenticated": False}, status_code=401)

    safe_user = {
        "id": user["id"],
        "google_id": user["google_id"],
        "email": user["email"],
        "name": user["name"],
        "picture": user["picture"],
        "providers": {
            "google": bool(user.get("google_access_token")),
            "youtube": bool(user.get("youtube_access_token")),
            "twitch": bool(user.get("twitch_access_token")),
            "vk": bool(user.get("vk_access_token")),
        },
    }
    return JSONResponse({"authenticated": True, "user": safe_user})


@router.post("/logout")
def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("access_token")
    return response