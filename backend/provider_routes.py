from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth")


@router.get("/twitch/url")
def twitch_url():
    return RedirectResponse(url="http://localhost:5173/", status_code=302)


@router.get("/vk/url")
def vk_url():
    return RedirectResponse(url="http://localhost:5173/", status_code=302)
