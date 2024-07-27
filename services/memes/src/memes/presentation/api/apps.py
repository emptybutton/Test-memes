from fastapi import FastAPI

from memes.presentation.api import controllers


app = FastAPI()
app.include_router(controllers.memes.router)
