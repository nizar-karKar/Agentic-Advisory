from fastapi import FastAPI
from api.routes.workflow import router as workflow_router


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Agentic AI LangGraph API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router)


@app.get("/")
def health_check():
    return {"status": "healthy"}
