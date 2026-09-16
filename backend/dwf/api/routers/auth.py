from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from dwf.api.deps import get_db, get_settings
from dwf.domain.models.user import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from dwf.services.auth_service import AuthService
from dwf.settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    auth_service = AuthService(db, settings)
    try:
        user = await auth_service.register(request.email, request.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return TokenResponse(
        access_token=auth_service.create_access_token(str(user.id)),
        refresh_token=auth_service.create_refresh_token(str(user.id)),
    )


@router.post("/login")
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    auth_service = AuthService(db, settings)
    user = await auth_service.login(request.email, request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    return TokenResponse(
        access_token=auth_service.create_access_token(str(user.id)),
        refresh_token=auth_service.create_refresh_token(str(user.id)),
    )


@router.post("/refresh")
async def refresh(
    request: RefreshRequest,
    settings: Settings = Depends(get_settings),
):
    auth_service = AuthService(None, settings)
    try:
        payload = auth_service.decode_token(request.refresh_token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        ) from exc

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is not a refresh token",
        )

    return TokenResponse(
        access_token=auth_service.create_access_token(payload["sub"]),
        refresh_token=auth_service.create_refresh_token(payload["sub"]),
    )
