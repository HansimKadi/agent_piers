import os
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles # <--- NEW: For serving images
from fastapi.middleware.cors import CORSMiddleware # <--- NEW: For connecting React
from .ai.gemini import Gemini
from .auth.dependencies import get_user_identifier
from .auth.throttling import apply_rate_limit
from src.DTOs.eventstate import ChatRequest, ChatResponse
from google.genai import types
from .db.database import Base, engine

app = FastAPI()

# ---------------------------------------------------------
# 1. CORS CONFIGURATION (The Bridge)
# ---------------------------------------------------------
# This allows your React app (running on localhost:5173) to talk to this Python API.
origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# ---------------------------------------------------------
# 2. STATIC ASSETS (The Images)
# ---------------------------------------------------------
# We calculate the path to the 'static' folder relative to this file.
current_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_dir, "static")

# Only mount if the directory actually exists to prevent startup errors
if os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
else:
    print(f"WARNING: Static folder not found at {static_path}. Images will not load.")


# ---------------------------------------------------------
# 3. EXISTING LOGIC (Database & AI)
# ---------------------------------------------------------

# Initialize database on app startup
@app.on_event("startup")
def startup_event():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database ready.")

# --- AI Configuration ---
def load_system_prompt():
    try:
        # Ensure this path is correct relative to where you run uvicorn
        with open("src/prompts/system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        print("WARNING: System prompt file not found.")
        return None
    
system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


# --- Chat history storage ---
# (Note: See "Intellectual Push" below regarding this line)
chat_history = [] 

# --- API Endpoints ---
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, user_id: str = Depends(get_user_identifier)):
    apply_rate_limit(user_id)

    # 1. Append user message
    chat_history.append(
        types.Content(
            role="user", 
            parts=[types.Part(text=request.prompt)] # Note: Added 'text=' for clarity
    ))

    # 2. Call the AI
    response_text = ai_platform.generate_text(contents=chat_history)
    
    if response_text is None:
        print("Tool calling attempted but no response received.")
        response_text = "I am attempting to use a tool, but was unable to get confirmation."
        
    # 3. Append AI response
    chat_history.append(
        types.Content(
            role="model",
            parts=[types.Part(text=response_text)]
        )
    )
    
    return ChatResponse(response=response_text)

@app.get("/")
async def root():
    return {"message": "API is running"}