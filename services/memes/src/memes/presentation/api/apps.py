from contextlib import asynccontextmanager
from typing import Iterable

from fastapi import FastAPI

from memes.facade import services
from memes.presentation.api import controllers


@asynccontextmanager
async def lifespan(app: FastAPI) -> Iterable:
    yield
    await services.close.perform()


app = FastAPI(lifespan=lifespan)
app.include_router(controllers.memes.router)
