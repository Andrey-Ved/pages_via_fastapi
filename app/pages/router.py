from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/chat")
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.get("/video")
async def get_video_page(request: Request):
    return templates.TemplateResponse(
        "video.html",
        {"request": request, "path": "video-001.mp4"}
    )


@router.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


print('init pages routers')
