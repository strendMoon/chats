from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from oauth_google import generate_google_oauth_redirect_url

router = APIRouter(prefix="/auth")

@router.get("/google/oauth")
def get_google_oauth_redirect_url():
    url = generate_google_oauth_redirect_url()
    return RedirectResponse(url=url, status_code=302)
    