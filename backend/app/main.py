from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import auth, predict, data_management

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIH Crop Yield API")

origins = ["http://localhost:5173"] # Your frontend URL

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