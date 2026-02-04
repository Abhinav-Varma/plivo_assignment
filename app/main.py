from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import plivo

from app.config import (
    PLIVO_AUTH_ID,
    PLIVO_AUTH_TOKEN,
    FROM_NUMBER,
    TO_NUMBER,
    BASE_URL
)

from app.ivr import router

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

client = plivo.RestClient(
    auth_id=PLIVO_AUTH_ID,
    auth_token=PLIVO_AUTH_TOKEN
)


# ---------------- HOME PAGE ---------------- #

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------- CALL BUTTON ---------------- #

@app.post("/start-call")
async def start_call():

    response = client.calls.create(
        from_=FROM_NUMBER,
        to_=TO_NUMBER,
        answer_url=f"{BASE_URL}/ivr",
        answer_method="POST"
    )

    return RedirectResponse("/", status_code=303)


# ---------------- HEALTH ---------------- #

@app.get("/health")
def health():
    return {"status": "running"}


app.include_router(router)
