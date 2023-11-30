from math import ceil
from uuid import uuid4

from fastapi import APIRouter, Query, Path, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import count
from starlette import status
from starlette.responses import RedirectResponse

from core.repositories import user_repository
from core.settings import templating, redis
from core.database import session, Advert
from core.types import UserDetail, UserRegisterForm, UserLoginForm
from core.utils import create_user_verify_url
from core.tasks import send_email
from core.dependencies import IsAuthenticated

router = APIRouter()


PAGINATE_BY = 1


@router.get(
    path="/",
    response_class=HTMLResponse,
    name="advert_index"
)
async def index(request: Request, page: int = Query(default=1, ge=1)):
    print(request.user)
    with session() as s:
        advert_count = s.scalar(
            select(count(Advert.id))
            .filter_by(is_published=True)
        )
        max_page = ceil(advert_count / PAGINATE_BY)
        objs = s.query(Advert).filter_by(is_published=True).limit(PAGINATE_BY).offset(page * PAGINATE_BY - PAGINATE_BY).all()
    return templating.TemplateResponse(
        name="advert/index.html",
        context={
            "request": request,
            "adverts": objs,
            "current_page": page,
            "max_page": max_page
        }
    )


@router.get(
    path="/contact",
    response_class=HTMLResponse,
    name="advert_contact",
    dependencies=[IsAuthenticated]
)
async def contact(request: Request):
    return templating.TemplateResponse(
        name="advert/contact.html",
        context={
            "request": request
        }
    )


@router.post(
    path="/contact",
    response_class=HTMLResponse,
    name="advert_contact"
)
async def _contact(
        request: Request,
        name: str = Form(),
        email: str = Form(),
        message: str = Form()
):
    print(name)
    print(email)
    print(message)
    return await contact(request=request)


@router.get(
    path="/login",
    response_class=HTMLResponse,
    name="login"
)
async def login(request: Request):
    return templating.TemplateResponse(
        name="advert/sign-in.html",
        context={
            "request": request
        }
    )


@router.post(
    path="/login",
    response_class=HTMLResponse,
    name="login"
)
async def _login(request: Request, data: UserLoginForm = Depends(dependency=UserLoginForm.as_form)):
    user = user_repository.get_by_email(email=data.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not active")

    if not data.validate_password(hash_password=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password invalid")

    response = await login(request=request)
    session = str(uuid4())
    await redis.set(
        name=session,
        value=user.id,
        ex=24*60*60
    )
    response.set_cookie(
        key="session",
        value=session,
    )
    return response


@router.get(
    path="/logout",
    response_class=RedirectResponse,
    name="logout"
)
async def logout(request: Request):
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="session")
    await redis.delete(request.cookies.get("session"))
    return response


@router.get(
    path="/register",
    response_class=HTMLResponse,
    name="register"
)
async def register(request: Request):
    return templating.TemplateResponse(
        name="advert/sign-up.html",
        context={
            "request": request
        }
    )


@router.post(
    path="/register",
    response_class=HTMLResponse,
    name="register"
)
async def _register(request: Request, data: UserRegisterForm = Depends(dependency=UserRegisterForm.as_form)):
    user = UserDetail.create(data=data)
    try:
        user = user_repository.create(obj=user, exclude={"date_register"})
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is exists")
    else:
        verify_url = await create_user_verify_url(user_id=user.id)
        send_email.delay(email=user.email, url=verify_url)
    return await register(request=request)


@router.get(
    path="/{slug}",
    response_class=HTMLResponse,
    name="advert_detail"
)
async def detail(request: Request, slug: str = Path()):
    with session() as s:
        obj = s.scalar(
            select(Advert)
            .filter_by(is_published=True, slug=slug)
        )
        if obj is None:
            raise HTTPException(status_code=404)
    return templating.TemplateResponse(
        name="advert/post.html",
        context={
            "request": request,
            "advert": obj
        }
    )
