import os
import requests
import logging # For logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

# --- Environment Variables & Configuration ---
# Load environment variables from .env in the backend directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(title="Advisory API", version="1.0.0")

# --- CORS Middleware ---
# Allows requests from your frontend (and potentially other origins)
# For development, allowing all origins ("*") is common.
# For production, restrict this to your frontend's actual domain(s).
origins = [
        "http://localhost",
    "http://localhost:3000", # Common React dev port
    "http://localhost:5173", # Common Vite dev port
    "http://localhost:8000", # Default Uvicorn/FastAPI port if you ever use it
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",

    # THE CRUCIAL ONE FOR YOUR CURRENT SETUP:
    "http://127.0.0.1:5500",  # This is the origin from your error message
    "http://localhost:5500",   # Also add this one for completeness
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # More secure to list specific origins
    # allow_origins=["*"], # Allows all origins - use with caution
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- Pydantic Models for Request/Response Validation ---
class AdvisoryRequest(BaseModel):
    location: str

class AdvisoryResponse(BaseModel):
    advisories: str

class ErrorResponse(BaseModel):
    error: str

# --- API Endpoints ---
@app.post("/api/advisories", response_model=AdvisoryResponse, responses={
    400: {"model": ErrorResponse, "description": "Bad Request"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
    503: {"model": ErrorResponse, "description": "Service Unavailable (Perplexity API issue)"}
})
async def get_advisories(payload: AdvisoryRequest): # FastAPI uses type hints for request body
    if not PERPLEXITY_API_KEY:
        logger.error("Perplexity API key not configured")
        raise HTTPException(status_code=500, detail="Perplexity API key not configured")

    location = payload.location # Access data from Pydantic model

    if not location:
        # This check is technically redundant if AdvisoryRequest has location as a required field,
        # Pydantic would raise a validation error before reaching here.
        # But keeping it for explicit clarity if needed.
        raise HTTPException(status_code=400, detail="Location is required")

    try:
        state, country = map(str.strip, location.split(','))
    except ValueError:
        raise HTTPException(status_code=400, detail="Location format should be 'State, Country'")

    prompt_text = f"""
    You are a specialized AI assistant tasked with finding official public health advisories.
    Your goal is to return the top 5 most relevant and current official medical advisories issued by government or public health authorities in the last 30 days for the location: {state}, {country}.

    These advisories should be related to public health, disease outbreaks, or specific health warnings for that region.

    Please ensure the advisories meet these criteria:
    1. Issued by governmental or official public health bodies (e.g., CDC, WHO, Ministry of Health, state health departments).
    2. Dated or updated within the last 30 days from today.
    3. Presented as clear, summarized bullet points.
    4. For each advisory, include:
       - Date of issue (or last update if applicable)
       - Issuing Agency
       - A concise summary of the key recommendation or alert.
    5. Avoid duplication. Only list distinct advisories.
    6. Avoid irrelevant content such as general health tips, news articles not directly issuing an advisory, blog posts, or unofficial forums. Focus strictly on official advisories.

    If no official advisories matching these criteria are found for {state}, {country} within the last 30 days, you MUST explicitly state:
    "No relevant official medical advisories were found for {state}, {country} in the last 30 days."

    Present the findings as a numbered list if advisories are found.
    Do not include any introductory or concluding remarks beyond the requested list or the "no advisories found" statement.
    Do not include URLs unless they are part of the official advisory title or summary.
    """

    perplexity_payload = {
        "model": "sonar-pro", # Or "pplx-70b-online", "sonar-pro" etc.
        "messages": [
            {"role": "system", "content": "You are an expert assistant in public health advisories."},
            {"role": "user", "content": prompt_text}
        ],
        "max_tokens": 1000,
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    try:
        # Use an async HTTP client like httpx for true async benefits,
        # but `requests` will work (it runs synchronously in a thread pool).
        # For simplicity with your existing code, `requests` is kept here.
        # To use httpx (recommended for async FastAPI):
        # import httpx
        # async with httpx.AsyncClient(timeout=60) as client:
        #     response = await client.post(PERPLEXITY_API_URL, json=perplexity_payload, headers=headers)
        
        response = requests.post(PERPLEXITY_API_URL, json=perplexity_payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        api_response_data = response.json()
        
        if api_response_data.get("choices") and len(api_response_data["choices"]) > 0:
            advisory_text = api_response_data["choices"][0]["message"]["content"]
            return {"advisories": advisory_text} # FastAPI automatically converts dict to JSON
        else:
            logger.error(f"Unexpected Perplexity API response structure: {api_response_data}")
            error_message = f"Could not retrieve advisories. API response was: {api_response_data.get('error', {}).get('message', 'Unknown error')}"
            raise HTTPException(status_code=500, detail=error_message)

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error calling Perplexity API: {e.response.status_code} - {e.response.text}")
        error_message = f"Error from Perplexity API: Status {e.response.status_code}"
        try:
            error_detail = e.response.json()
            error_message += f" - Details: {error_detail}"
        except ValueError:
            error_message += f" - Body: {e.response.text[:200]}"
        raise HTTPException(status_code=503, detail=error_message)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Perplexity API: {e}")
        error_message = f"Error communicating with Perplexity API: {str(e)}"
        raise HTTPException(status_code=503, detail=error_message)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Note: The `if __name__ == '__main__':` block is not needed for FastAPI.
# You run FastAPI apps with an ASGI server like Uvicorn.

# To add a simple root endpoint for testing if the server is up:
@app.get("/")
async def root():
    return {"message": "Advisory API is running!"}