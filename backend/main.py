from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Local LLM Testcase Generator")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "llama3.2"
    system_template: str | None = None

class GenerateResponse(BaseModel):
    content: str
    status: str
    error_message: str | None = None

@app.post("/generate", response_model=GenerateResponse)
async def generate_testcases(request: GenerateRequest):
    logger.info(f"Received generation request for model: {request.model}")
    try:
        # Default system prompt if none provided
        system_prompt = request.system_template or (
            "You are a QA automation expert. "
            "Your task is to generate comprehensive test cases based on the user's input. "
            "Format the output in Markdown."
        )

        response = ollama.chat(model=request.model, messages=[
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': request.prompt,
            },
        ])

        generated_content = response['message']['content']
        return GenerateResponse(
            content=generated_content,
            status="success"
        )
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return GenerateResponse(
            content="",
            status="error",
            error_message=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
