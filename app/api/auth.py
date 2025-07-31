from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings
from app.database.db import get_db
from app.schemas.user import UserCreate, UserLogin
from app.crud import user as crud_user
from app.models.models import User

SECRET_KEY = SECRET_KEY = settings.SECRET_KEY
ALGORITHM = ALGORITHM = settings.ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней

router = APIRouter(tags=["auth"])


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = crud_user.create_user(db, user_data.username, user_data.password)
    access_token = create_access_token(user=new_user)

    # Issue a redirect to the homepage and persist the auth token.
    # Explicitly set the cookie path to "/" so that the JWT is sent on
    # every request. Without specifying the path the browser will default
    # it to the current route ("/api/auth/register"), which prevents the
    # homepage and other pages from receiving the cookie, resulting in
    # endless redirect loops after registration.
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,
        path="/"
    )
    return response


@router.post("/login")
def login(request: Request, user_data: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, user_data.username)
    if not db_user or not crud_user.verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(user=db_user)
    next_url = request.query_params.get("next") or "/"

    response = RedirectResponse(url=next_url, status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,
        path="/"   # <-- добавь это!
)
    return response


@router.post("/logout")
def logout():
    # Clear the JWT cookie on logout. Specify the same path used when
    # setting the cookie so that it is properly removed in the browser.
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token", path="/")
    return response


def create_access_token(user: User, expires_delta: timedelta = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {
        "sub": str(user.id),
        "username": user.username,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return db.query(User).filter(User.id == int(user_id)).first()
    except JWTError:
        return None
