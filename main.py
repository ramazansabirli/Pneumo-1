from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uvicorn

app = FastAPI()

UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def main_form():
    content = """
    <html>
        <head>
            <title>BT ve Vital Veri Yükleme</title>
        </head>
        <body>
            <h2>Toraks BT (AVI) Yükle ve Vital Verileri Gir</h2>
            <form action="/upload/" enctype="multipart/form-data" method="post">
                Video Dosyası: <input type="file" name="file"><br><br>
                SpO₂: <input type="text" name="spo2"><br>
                RR: <input type="text" name="rr"><br>
                HR: <input type="text" name="hr"><br>
                BP: <input type="text" name="bp"><br>
                Bilinç: <input type="text" name="bilinc"><br>
                Yaş: <input type="text" name="yas"><br>
                Cinsiyet: <input type="text" name="cinsiyet"><br>
                Uygulanan Tedavi: <input type="text" name="tedavi"><br><br>
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=content)

@app.post("/upload/")
async def upload(
    file: UploadFile = File(...),
    spo2: str = Form(...),
    rr: str = Form(...),
    hr: str = Form(...),
    bp: str = Form(...),
    bilinc: str = Form(...),
    yas: str = Form(...),
    cinsiyet: str = Form(...),
    tedavi: str = Form(...)
):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Veriler yüklendi.",
        "video_path": f"/static/{file.filename}",
        "spo2": spo2,
        "rr": rr,
        "hr": hr,
        "bp": bp,
        "bilinc": bilinc,
        "yas": yas,
        "cinsiyet": cinsiyet,
        "tedavi": tedavi
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
