from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI
from src import get_fts

app = FastAPI()
fts = get_fts()


with open("./assets/index.html", "r") as f:
    index_html = f.read()

@app.get("/")
def index():
    return HTMLResponse(index_html)

@app.get("/api/search")
async def search(query: str):
    return JSONResponse(fts.search(query))