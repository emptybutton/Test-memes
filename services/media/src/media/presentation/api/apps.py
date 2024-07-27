from fastapi import FastAPI

from media.presentation.api.routes import router


app = FastAPI(prefix="/api/0.1.0v")
app.include_router(router)
