from sys import version as python_version

from dotenv import load_dotenv
from fastapi import FastAPI, __version__ as fastapi_version
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request

from api.auth.main import auth_router
from api.comments.main import comments_router
from api.posts.main import posts_router
from api.users.main import users_router

load_dotenv()

app = FastAPI(
    root_path='/api',
    title='Бложик',
    version='1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
)


@app.middleware('http')
async def add_x_powered_by(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Powered-By-Python"] = f"Python {python_version}"
    response.headers["X-Powered-By-FastApi"] = f"FastAPI {fastapi_version}"
    return response


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)
