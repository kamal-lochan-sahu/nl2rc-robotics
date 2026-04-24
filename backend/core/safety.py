# Safety limits - NON NEGOTIABLE
MAX_VELOCITY = 0.3      # m/s
MAX_DISTANCE = 3.0      # meters
MAX_ROTATION = 180.0    # degrees
MIN_CONFIDENCE = 0.7    # reject below this

HARMFUL_KEYWORDS = [
    "attack", "destroy", "kill", "harm",
    "crash", "smash", "break", "damage"
]

def validate_command(parsed: dict) -> dict:
    """
    Returns: {"safe": True/False, "reason": "..."}
    """
    # 1. Confidence check
    confidence = parsed.get("confidence", 0)
    if confidence < MIN_CONFIDENCE:
        return {"safe": False, "reason": f"Low confidence: {confidence}"}

    # 2. Unknown intent check
    intent = parsed.get("intent", "unknown")
    if intent == "unknown":
        return {"safe": False, "reason": "Unknown intent"}

    # 3. Harmful keyword check
    original = parsed.get("original_input", "").lower()
    for word in HARMFUL_KEYWORDS:
        if word in original:
            return {"safe": False, "reason": f"Harmful keyword: {word}"}

    # 4. Plan limits check
    for step in parsed.get("plan", []):
        params = step.get("params", {})

        velocity = params.get("velocity", 0)
        if velocity > MAX_VELOCITY:
            return {"safe": False, "reason": f"Velocity {velocity} exceeds max {MAX_VELOCITY}"}

        distance = params.get("distance", 0)
        if distance > MAX_DISTANCE:
            return {"safe": False, "reason": f"Distance {distance} exceeds max {MAX_DISTANCE}"}

        angle = params.get("angle", 0)
        if angle > MAX_ROTATION:
            return {"safe": False, "reason": f"Angle {angle} exceeds max {MAX_ROTATION}"}

    return {"safe": True, "reason": "All checks passed"}