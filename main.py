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

END_POINT = "http://www.boredapi.com/api/activity/"


# def get_activity():
#     activity_request = requests.get(END_POINT)
#     activity = activity_request.json()["activity"]
#     return activity


def get_activity():
    try:
        activity_request = requests.get(END_POINT)
        # Check if the response status code indicates success (e.g., 200 OK)
        if activity_request.status_code == 200:
            # Attempt to parse the JSON response
            activity_data = activity_request.json()
            # Ensure the 'activity' key exists in the JSON data
            if "activity" in activity_data:
                return activity_data["activity"]
            else:
                print("No 'activity' field found in the response.")
                return None
        else:
            print(f"Request failed with status code {activity_request.status_code}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


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
