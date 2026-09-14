from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from json import loads, dumps
import os

load_dotenv()

router = APIRouter()

IS_PROD = os.getenv("ENV") == "production"
if not IS_PROD:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")
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
        secure=IS_PROD,
    )
    return response


@router.get("/callback")
def auth_callback(code: str, request: Request):
    flow = get_oauth_flow()
    flow.code_verifier = request.cookies.get("code_verifier")
    flow.fetch_token(code=code)
    creds = flow.credentials

    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "scopes": creds.scopes,
    }

    response = RedirectResponse(url=FRONTEND_URL)
    response.set_cookie(
        key="google_tokens",
        value=dumps(token_data),
        httponly=True,
        samesite="lax",
        secure=IS_PROD,
    )
    response.delete_cookie("code_verifier")
    return response


def load_credentials(cookie_value: str | None) -> Credentials | None:
    if not cookie_value:
        return None
    data = loads(cookie_value)
    return Credentials(
        token=data["token"],
        refresh_token=data.get("refresh_token"),
        token_uri=data["token_uri"],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=data.get("scopes"),
    )
