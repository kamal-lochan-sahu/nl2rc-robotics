from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.safety import validate_command
from core.model import parse_command
import asyncio

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

    # Step 1: Parse karo
    parsed = parse_command(request.text)

    if parsed is None:
        raise HTTPException(status_code=503, detail="Parser failed.")

    # Step 2: Safety check
    safety_result = validate_command(parsed)

    if not safety_result["safe"]:
        raise HTTPException(
            status_code=400,
            detail=f"Safety check failed: {safety_result['reason']}"
        )

    # Step 3: ROS2 execute (non-blocking)
    try:
        from ros2_bridge import execute_command
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, execute_command, parsed)
    except Exception as e:
        print(f"ROS2 error: {e}")

    return CommandResponse(
        original_input=request.text,
        intent=parsed.get("intent", "unknown"),
        safety=safety_result,
        parsed=parsed,
        message="Command executed successfully"
    )