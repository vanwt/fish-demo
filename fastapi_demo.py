from fastapi import FastAPI
from uvicorn.main import run

app = FastAPI()


@app.post("/index")
async def req():
    return {"code": 0, "msg": "Hello Word"}

@app.get("/in")
async def req():
    return {"code": 1, "msg": "Test Word"}

if __name__ == '__main__':
    run(app, host="0.0.0.0")
