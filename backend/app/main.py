from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine, Base
from .api import vendors, products, dashboard, scanner, settings
from .scheduler import start_scheduler


# Create database tables
Base.metadata.create_all(bind=engine)

# Scheduler instance
scheduler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    global scheduler
    scheduler = start_scheduler()
    print("Application started - scheduler running")
    yield
    # Shutdown
    if scheduler:
        scheduler.shutdown()
    print("Application shutdown - scheduler stopped")


app = FastAPI(
    title="Price Tracker API",
    description="API for tracking product prices across multiple vendors",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://geekom-gt1-a:3000",  # Local network hostname
        "http://geekom-gt1-a.tail425a06.ts.net:3000",  # Tailscale hostname
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vendors.router)
app.include_router(products.router)
app.include_router(dashboard.router)
app.include_router(scanner.router)
app.include_router(settings.router)


@app.get("/")
def root():
    return {
        "message": "Price Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


