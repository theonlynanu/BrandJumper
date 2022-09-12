from fastapi import FastAPI, HTTPException
from app import generate_brand_name, generate_tagline

max_input_length = 32

app = FastAPI()

@app.get("/generate_name")
async def generate_name_api(prompt: str):
    validate_input_length(prompt)
    names = generate_brand_name(prompt)
    return {"names": names, "tagline": None}

@app.get("/generate_tagline")
async def generate_tagline_api(prompt: str):
    validate_input_length(prompt)
    tagline = generate_tagline(prompt)
    return {"names": [], "tagline": tagline}

@app.get("/generate_all")
async def generate_all_api(prompt:str):
    validate_input_length(prompt)
    names = generate_brand_name(prompt)
    tagline = generate_tagline(prompt)
    return {"names": names, "tagline": tagline}

def validate_input_length(prompt: str):
    if len(prompt) >= max_input_length:
        raise HTTPException(status_code=400, detail=f"Prompt is limited to {max_input_length} characters. Please try again.")

# uvicorn app_api:app --reload