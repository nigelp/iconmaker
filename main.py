import io
import base64
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

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
    use_cuda: bool = False
    resolution: int = 64
    steps: int = 20
    format: str = "jpeg"


@app.on_event("startup")
def startup_event():
    load_pipeline()


@app.post("/api/generate")
def generate_icon(payload: GenerateRequest):
    used_cuda = False
    cuda_message = ""
    if payload.use_cuda:
        if torch.cuda.is_available():
            try:
                pipe.to("cuda")
                torch.cuda.synchronize()
                used_cuda = True
                cuda_message = "CUDA enabled"
            except Exception as e:
                pipe.to("cpu")
                cuda_message = f"CUDA error: {str(e)}"
        else:
            pipe.to("cpu")
            cuda_message = "CUDA not available"
    else:
        pipe.to("cpu")
        cuda_message = "CUDA not requested"

    prompt = f"model:icons, {payload.prompt}, simple colorful app icon, minimal vector, transparent background"
    image = pipe(prompt, num_inference_steps=payload.steps).images[0]
    image = image.resize((payload.resolution, payload.resolution), Image.LANCZOS)

    buffered = io.BytesIO()
    save_format = "JPEG" if payload.format.lower() == "jpeg" else "PNG"
    image.save(buffered, format=save_format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return JSONResponse(content={"image": img_str, "used_cuda": used_cuda, "cuda_message": cuda_message})

# Mount React static build LAST, so it won't override /api/* endpoints
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")
