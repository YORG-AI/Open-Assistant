import os

# load dotenv first, then import other modules
from dotenv import load_dotenv
import subprocess

load_dotenv()

import src.routers

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from .app import app

# app.include_router(agenda.router)


@app.get("/start_jupyter/")
def start_jupyter():
    # Launch Jupyter Notebook in the background
    subprocess.Popen(["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"])
    return {"message": "Jupyter Notebook started"}


app.mount(
    "/data",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    ),
    name="data",
)
