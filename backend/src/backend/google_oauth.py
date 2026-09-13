from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from json import loads
import os

load_dotenv()

router = APIRouter()
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
FRONTEND_URL = "http://localhost:4200"
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_oauth_flow() -> Flow:
    client_config = {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI],
        }
    }
    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )


@router.get("/login")
def login():
    flow = get_oauth_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )
    response = RedirectResponse(auth_url)
    response.set_cookie(
        key="code_verifier",
        value=flow.code_verifier,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/callback")
def auth_callback(code: str, request: Request):
    flow = get_oauth_flow()
    flow.code_verifier = request.cookies.get("code_verifier")
    flow.fetch_token(code=code)
    creds = flow.credentials

    response = RedirectResponse(url=FRONTEND_URL)
    response.set_cookie(
        key="google_tokens",
        value=creds.to_json(),
        httponly=True,
        samesite="lax",
    )
    response.delete_cookie("code_verifier")
    return response


def load_credentials(cookie_value: str | None) -> Credentials | None:
    if not cookie_value:
        return None
    return Credentials.from_authorized_user_info(loads(cookie_value), SCOPES)
