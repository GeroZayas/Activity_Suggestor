from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

# ----------------------------------------------------------------
# FASTAPI APP
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


def get_activity():
    activity_request = requests.get("http://www.boredapi.com/api/activity/")
    activity = activity_request.json()["activity"]
    return activity


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    image = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.p7wf8LY3zpmEek1blEGtSAHaE8%26pid%3DApi&f=1&ipt=0b79c766195d77161917547a994247fac44701caa0d7c911f9e7a69cbf1eff5f&ipo=images"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "activity": get_activity(),
            "image": image,
        },
    )


@app.get("/activity", response_class=HTMLResponse)
async def suggested_activity(request: Request):
    return RedirectResponse(url="http://www.boredapi.com/api/activity/")