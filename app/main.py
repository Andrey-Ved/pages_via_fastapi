import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import UserExampleException
from app.users.services import get_user_name, get_current_user_id

from app.users.router import router as router_users
from app.pages.router import router as router_pages
from app.chat.router import router as router_chat
from app.video.router import router as router_video


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router_users, prefix="/users", tags=["Users"])
app.include_router(router_pages, prefix="/pages", tags=["Pages"])
app.include_router(router_chat, prefix="/chat", tags=["Chat"])
app.include_router(router_video, prefix="/video", tags=["Video"])

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
        "DELETE",
        "PATCH",
        "PUT"
    ],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"
    ],
)


@app.get("/", tags=["Pages"])
async def root(request: Request) -> Response:
    try:
        await get_user_name(
            await get_current_user_id(request)
        )
        return RedirectResponse("/pages/chat", status_code=303)

    except UserExampleException:
        return RedirectResponse("/pages/login", status_code=303)


def main():

    print(
        f'\n'
        f'INFO:     Documentation is available at -'
        f' http://127.0.0.1:8000/docs'
        f'\n'
    )

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000
    )


if __name__ == '__main__':
    main()
