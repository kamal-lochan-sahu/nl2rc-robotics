import re

def parse_command(text: str) -> dict:
    text_lower = text.lower().strip()

    # Stop commands
    if any(w in text_lower for w in ["stop", "halt", "freeze", "emergency"]):
        return {
            "original_input": text,
            "intent": "stop",
            "plan": [{"step": 1, "action": "stop", "params": {}}],
            "confidence": 0.99,
            "clarification_needed": None,
            "estimated_time_seconds": 0
        }

    # Rotate commands
    if any(w in text_lower for w in ["rotate", "turn", "spin"]):
        angle = 90.0
        match = re.search(r'(\d+\.?\d*)\s*(degree|deg|°)', text_lower)
        if match:
            angle = float(match.group(1))
        direction = "left" if any(w in text_lower for w in ["left", "anticlockwise"]) else "right"
        return {
            "original_input": text,
            "intent": "rotate",
            "plan": [{"step": 1, "action": "rotate", "params": {
                "direction": direction,
                "angle": min(angle, 180.0),
                "unit": "degrees"
            }}],
            "confidence": 0.95,
            "clarification_needed": None,
            "estimated_time_seconds": 3
        }

    # Navigate commands
    if any(w in text_lower for w in ["move", "go", "forward", "backward", "back"]):
        distance = 1.0
        match = re.search(r'(\d+\.?\d*)\s*(meter|metre|m\b)', text_lower)
        if match:
            distance = float(match.group(1))
        direction = "backward" if any(w in text_lower for w in ["back", "backward"]) else "forward"
        return {
            "original_input": text,
            "intent": "navigate",
            "plan": [{"step": 1, "action": "move", "params": {
                "direction": direction,
                "distance": min(distance, 3.0),
                "velocity": 0.2,
                "unit": "meters"
            }}],
            "confidence": 0.95,
            "clarification_needed": None,
            "estimated_time_seconds": int(min(distance, 3.0) / 0.2)
        }

    # Unknown
    return {
        "original_input": text,
        "intent": "unknown",
        "plan": [],
        "confidence": 0.0,
        "clarification_needed": "Command not understood",
        "estimated_time_seconds": 0
    }