"""
FastAPI Main Application

This is the entry point for the backend API.

Educational Notes:
- FastAPI is a modern, fast web framework for building APIs
- Automatic OpenAPI (Swagger) documentation at /docs
- Dependency injection for database sessions and other resources
- CORS middleware allows frontend to call the API
- Lifespan events for startup/shutdown tasks
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.

    Educational Note:
    This replaces the older @app.on_event decorators and provides
    a cleaner way to manage resources that need setup/teardown.
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(
        f"📚 API documentation available at: http://{settings.API_HOST}:{settings.API_PORT}/docs"
    )

    # Create database tables (in production, use migrations instead)
    # This is here for educational purposes to make setup easier
    Base.metadata.create_all(bind=engine)

    yield

    # Shutdown
    print("👋 Shutting down gracefully...")


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A text-based adventure game API built for educational purposes",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ============================================================================
# Middleware Configuration
# ============================================================================


# CORS Middleware - Allows frontend to make requests to the API
# Educational Note:
# CORS (Cross-Origin Resource Sharing) is a security feature that restricts
# which domains can access your API. In production, be specific about origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# ============================================================================
# Exception Handlers
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler to catch unhandled exceptions.

    Educational Note:
    This prevents the API from exposing internal error details to users,
    which is both a security best practice and better user experience.
    """
    print(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "An internal server error occurred. Please try again later."
        },
    )


# ============================================================================
# Routes
# ============================================================================


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API welcome message."""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Educational Note:
    Health checks are used by container orchestrators (like Kubernetes)
    to determine if the application is running properly.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "database": "connected",
    }


# Include API v1 routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ============================================================================
# Development Server
# ============================================================================


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
