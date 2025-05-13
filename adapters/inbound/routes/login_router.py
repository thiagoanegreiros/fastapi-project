from datetime import timedelta
from urllib.parse import parse_qs, urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from ta_envy import Env

from adapters.inbound.auth import create_access_token, verify_access_token

env = Env(
    required=[
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "JWT_SECRET_KEY",
        "REDIRECT_URI",
        "FRONT_REDIRECT_URI",
    ]
)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


router = APIRouter()
oauth = OAuth()

oauth.register(
    name="google",
    client_id=env.get("GOOGLE_CLIENT_ID", type=str),
    client_secret=env.get("GOOGLE_CLIENT_SECRET", type=str),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = env.get("REDIRECT_URI")
    frontend_redirect_uri = request.query_params.get("redirect_uri")
    state = urlencode({"redirect_uri": frontend_redirect_uri})
    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)


@router.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    state_raw = request.query_params.get("state", "")
    state_data = parse_qs(state_raw)
    redirect_uri = state_data.get("redirect_uri", [env.get("FRONT_REDIRECT_URI")])[0]

    access_token = create_access_token(
        data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=60)
    )

    refresh_token = create_access_token(
        data={"sub": user_info["email"]}, expires_delta=timedelta(days=7)
    )

    return RedirectResponse(
        url=f"{redirect_uri}?token={access_token}&refresh_token={refresh_token}"
    )


@router.post("/auth/refresh")
async def refresh_token_endpoint(body: RefreshTokenRequest):
    email = verify_access_token(body.refresh_token)["sub"]

    new_access_token = create_access_token(
        data={"sub": email}, expires_delta=timedelta(minutes=60)
    )
    return {"access_token": new_access_token}


@router.get("/me")
async def me(request: Request):
    token = request.query_params.get("token")
    payload = verify_access_token(token)
    return payload
