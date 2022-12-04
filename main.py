import io
from starlette.responses import StreamingResponse
from datetime import date
import users
from fastapi import FastAPI, File, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import cv2
import numpy as np
import math

app = FastAPI()
security = HTTPBasic()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/picture/invert")
async def invert_image(image: bytes = File(...)):
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    inverted = cv2.bitwise_not(img_np)
    _, im_png = cv2.imencode(".png", inverted)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@app.get("/prime/{num}")
async def primes(num: int):
    flag = True
    if num > 1:
        for i in range(2, int(math.sqrt(num) + 1)):
            if (num % i) == 0:
                flag = False
                break

    return {"Is prime": flag}


@app.get("/date")
def read_current_user(cred: HTTPBasicCredentials = Depends(security)):
    login = cred.username
    pwd = cred.password
    if login == users.login and pwd == users.pwd:
        return {"Date": date.today()}



