from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.backend import setup, process_message, reset
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global in-memory state (basic; can use session keys instead)
websmith = {"agent": None, "history": []}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")
    success = data.get("success_criteria", "")

    if websmith["agent"] is None:
        websmith["agent"] = await setup()

    response, agent = await process_message(
        websmith["agent"], message, success, websmith["history"]
    )
    websmith["history"].append((message, response))
    websmith["agent"] = agent
    return JSONResponse({"response": response, "history": websmith["history"]})

@app.post("/reset")
async def reset_all():
    message, success, agent, history = await reset()
    websmith["agent"] = agent
    websmith["history"] = []
    return JSONResponse({"message": message, "success": success, "history": history})
