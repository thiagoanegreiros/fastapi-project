from fastapi import HTTPException, Request


def require_auth(request: Request):
    user = getattr(request, "session", {}).get("user")

    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
