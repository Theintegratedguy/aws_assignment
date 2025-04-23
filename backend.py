from fastapi import FastAPI, Query # type: ignore
from fastapi.middleware.cors import CORSMiddleware# type: ignore
from fastapi.responses import StreamingResponse# type: ignore
import segno# type: ignore
from PIL import Image# type: ignore
import io

app = FastAPI()

# Allow all CORS (for frontend from S3 to access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/generate")
def generate_qr(
    text: str = Query(...),
    scale: int = Query(5, ge=1, le=10),
    border: int = Query(4, ge=0, le=10),
    dark: str = Query("#000000"),
    light: str = Query("#FFFFFF"),
    rotate: int = Query(0, ge=0, le=360)
):
    qr = segno.make(text)
    temp_stream = io.BytesIO()

    qr.save(temp_stream, kind='png', scale=scale, border=border, dark=dark, light=light)
    temp_stream.seek(0)

    img = Image.open(temp_stream)
    if rotate != 0:
        img = img.rotate(rotate, expand=True)

    output_stream = io.BytesIO()
    img.save(output_stream, format='PNG')
    output_stream.seek(0)

    return StreamingResponse(output_stream, media_type="image/png")
