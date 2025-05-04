from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers.UserRouter import user_router

app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


app.include_router(user_router)
