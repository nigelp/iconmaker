import io
import base64
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
from fastapi.middleware.cors import CORSMiddleware

MODEL_PATH = "LiberteRedmond.safetensors"
LORA_PATH = "IconsRedmond15V-Icons.safetensors"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipe = None

def load_pipeline():
    global pipe
    pipe = StableDiffusionPipeline.from_single_file(MODEL_PATH, torch_dtype=torch.float32)
    pipe.to("cpu")
    pipe.load_lora_weights(LORA_PATH)


class GenerateRequest(BaseModel):
    prompt: str


@app.on_event("startup")
def startup_event():
    load_pipeline()


@app.post("/api/generate")
def generate_icon(payload: GenerateRequest):
    prompt = f"model:icons, {payload.prompt}, simple colorful app icon, minimal vector, transparent background"
    image = pipe(prompt).images[0]

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return JSONResponse(content={"image": img_str})

# Mount React static build LAST, so it won't override /api/* endpoints
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")
