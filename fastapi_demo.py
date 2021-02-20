from fastapi import FastAPI
from uvicorn.main import run

app = FastAPI()


@app.get("/index")
async def req():
    return {"code": 0, "msg": "Hello Word"}


if __name__ == '__main__':
    run(app, host="0.0.0.0")