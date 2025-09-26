from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import auth, predict, data_management
from .ml_service import initialize_ml_service
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIH Crop Yield API")

# Initialize ML service on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing ML service...")
    success = initialize_ml_service()
    if success:
        logger.info("✅ ML service initialized successfully")
    else:
        logger.warning("⚠️ ML service initialization failed, using fallback model")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174"
] # Your frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(predict.router, prefix="/predict", tags=["Predictions"])
app.include_router(data_management.router, prefix="/manage", tags=["Data Management"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the SIH API"}