from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.safety import validate_command

router = APIRouter()

class CommandRequest(BaseModel):
    text: str

class CommandResponse(BaseModel):
    original_input: str
    intent: str
    safety: dict
    parsed: dict
    message: str

@router.post("/command", response_model=CommandResponse)
async def process_command(request: CommandRequest):
    
    # Step 1: Basic parsed response (model integration baad mein)
    parsed = {
        "original_input": request.text,
        "intent": "navigate",
        "plan": [
            {
                "step": 1,
                "action": "move",
                "params": {
                    "direction": "forward",
                    "distance": 2.0,
                    "velocity": 0.2,
                    "unit": "meters"
                }
            }
        ],
        "safety_check": "pending",
        "confidence": 0.97,
        "clarification_needed": None,
        "estimated_time_seconds": 10
    }

    # Step 2: Safety check
    safety_result = validate_command(parsed)

    if not safety_result["safe"]:
        raise HTTPException(
            status_code=400,
            detail=f"Safety check failed: {safety_result['reason']}"
        )

    return CommandResponse(
        original_input=request.text,
        intent=parsed["intent"],
        safety=safety_result,
        parsed=parsed,
        message="Command validated successfully"
    )