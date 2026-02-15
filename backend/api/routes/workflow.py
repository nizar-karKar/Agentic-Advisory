from fastapi import APIRouter
from api.models.workflow_models import (
    WorkflowRequest,
    WorkflowResponse,
)
from orchestrators.langgraph_workflow import run_workflow

router = APIRouter(prefix="/workflow", tags=["Workflow"])


@router.post("/", response_model=WorkflowResponse)
def execute_workflow(request: WorkflowRequest):
    result = run_workflow(
        question=request.question,
        max_iterations=request.max_iterations,
    )

    return WorkflowResponse(**result)