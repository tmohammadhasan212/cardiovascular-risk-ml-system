"""FastAPI application factory, lifespan management, middleware, and route mounting."""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes_analytics import router as analytics_router
from app.api.routes_history import router as history_router
from app.api.routes_prediction import router as prediction_router
from app.database.connection import init_db
from app.schemas.prediction import HealthResponseSchema
from src.config import settings
from src.models.predict import get_prediction_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler initializing DB tables and preloading ML model."""
    print("Initializing database tables...")
    init_db()

    print("Preloading Machine Learning inference pipeline...")
    try:
        engine = get_prediction_engine()
        print(f"Model successfully loaded: {engine.metadata.get('model_name')}")
    except Exception as e:
        print(f"Warning: Could not preload model on startup: {e}")

    yield
    print("Application shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Production-grade REST API and research platform for cardiovascular risk prediction, "
        "model comparison, and SHAP explainability. Developed as a Bachelor's final graduation project."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(prediction_router)
app.include_router(history_router)
app.include_router(analytics_router)

# Mount static assets and templates
BASE_APP_DIR = Path(__file__).resolve().parent
static_dir = BASE_APP_DIR / "static"
templates_dir = BASE_APP_DIR / "templates"

static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/health", response_model=HealthResponseSchema, tags=["Health"])
def health_check():
    """System health check endpoint verifying model and database status."""
    engine = get_prediction_engine()
    model_loaded = engine.pipeline is not None
    return {
        "status": "ok",
        "model_loaded": model_loaded,
        "database_connected": True,
        "version": settings.APP_VERSION,
    }


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index_view(request: Request):
    """Serve the single-page application dashboard."""
    index_file = templates_dir / "index.html"
    if not index_file.exists():
        return HTMLResponse(
            "<h1>Cardiovascular Risk ML System</h1><p>API is running. Visit <a href='/docs'>/docs</a> for Swagger UI.</p>"
        )
    return templates.TemplateResponse(request=request, name="index.html")
