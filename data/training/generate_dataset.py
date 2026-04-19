import json
import random

# ─── Seed Data ───────────────────────────────────────────

distances = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
angles    = [30, 45, 60, 90, 120, 150, 180]
speeds    = ["slowly", "carefully", "quickly", ""]

move_templates = [
    "Move forward {d} meters",
    "Go forward {d} meters",
    "Move ahead {d} meters",
    "Drive forward {d} meters",
    "Move forward {d} meters {s}",
    "Go {d} meters forward",
    "Move backward {d} meters",
    "Go back {d} meters",
    "Reverse {d} meters",
    "Move back {d} meters {s}",
]

rotate_templates = [
    "Turn left {a} degrees",
    "Rotate left {a} degrees",
    "Turn right {a} degrees",
    "Rotate right {a} degrees",
    "Turn {a} degrees to the left",
    "Turn {a} degrees to the right",
    "Spin left {a} degrees",
    "Spin right {a} degrees",
]

stop_templates = [
    "Stop",
    "Stop immediately",
    "Emergency stop",
    "Halt",
    "Freeze",
    "Stop now",
    "Stop the robot",
    "Halt immediately",
    "Stop moving",
    "Emergency halt",
]

unsafe_templates = [
    "Destroy the wall",
    "Crash into the box",
    "Hit the obstacle",
    "Ram the door",
    "Smash everything",
    "Attack the target",
    "Go as fast as possible",
    "Move 10 meters forward",
    "Rotate 360 degrees",
    "Move 5 meters backward",
]

# ─── Generator Functions ─────────────────────────────────

def make_move(text, direction, d, s=""):
    vel = 0.1 if s == "slowly" or s == "carefully" else 0.2
    return {
        "input": text.strip(),
        "output": {
            "original_input": text.strip(),
            "intent": "navigate",
            "plan": [{
                "step": 1,
                "action": "move",
                "params": {
                    "direction": direction,
                    "distance": float(d),
                    "velocity": vel,
                    "unit": "meters"
                }
            }],
            "safety_check": "clear",
            "confidence": round(random.uniform(0.90, 0.99), 2),
            "clarification_needed": None,
            "estimated_time_seconds": int(float(d) / vel)
        }
    }

def make_rotate(text, direction, a):
    return {
        "input": text.strip(),
        "output": {
            "original_input": text.strip(),
            "intent": "rotate",
            "plan": [{
                "step": 1,
                "action": "rotate",
                "params": {
                    "direction": direction,
                    "angle": float(a),
                    "unit": "degrees"
                }
            }],
            "safety_check": "clear",
            "confidence": round(random.uniform(0.90, 0.99), 2),
            "clarification_needed": None,
            "estimated_time_seconds": int(a / 45) + 1
        }
    }

def make_stop(text):
    return {
        "input": text.strip(),
        "output": {
            "original_input": text.strip(),
            "intent": "stop",
            "plan": [{
                "step": 1,
                "action": "halt",
                "params": {}
            }],
            "safety_check": "clear",
            "confidence": 1.0,
            "clarification_needed": None,
            "estimated_time_seconds": 0
        }
    }

def make_unsafe(text):
    return {
        "input": text.strip(),
        "output": {
            "original_input": text.strip(),
            "intent": "unknown",
            "plan": [],
            "safety_check": "reject",
            "confidence": 0.0,
            "clarification_needed": "Command rejected: unsafe or out of bounds.",
            "estimated_time_seconds": 0
        }
    }

# ─── Generate Dataset ─────────────────────────────────────

dataset = []

# Move forward
for t in move_templates[:5]:
    for d in distances:
        for s in speeds:
            text = t.format(d=d, s=s)
            dataset.append(make_move(text, "forward", d, s))

# Move backward
for t in move_templates[5:]:
    for d in distances:
        for s in speeds:
            text = t.format(d=d, s=s)
            dataset.append(make_move(text, "backward", d, s))

# Rotate
for t in rotate_templates:
    for a in angles:
        direction = "left" if "left" in t else "right"
        text = t.format(a=a)
        dataset.append(make_rotate(text, direction, a))

# Stop
for t in stop_templates:
    dataset.append(make_stop(t))

# Unsafe
for t in unsafe_templates:
    dataset.append(make_unsafe(t))


    # Extra stop examples
extra_stop = [
    "Stop the robot now", "Please stop", "Halt the machine",
    "Stop operation", "Cancel movement", "Abort",
    "Stop everything", "Pause the robot", "Hold position",
    "Stop at once", "Cease movement", "Stand by",
    "Stop right there", "Freeze the robot", "Hold on",
    "Stop moving now", "Kill motion", "Robot stop",
    "Immediate stop", "Full stop"
]
for t in extra_stop:
    dataset.append(make_stop(t))

# Extra unsafe examples
extra_unsafe = [
    "Move 10 meters forward", "Go 5 meters back",
    "Rotate 270 degrees", "Move at full speed",
    "Crash into the wall", "Hit the person",
    "Go as fast as you can", "Ignore safety limits",
    "Override safety", "Disable safety check",
    "Move 4 meters right", "Rotate 360 degrees left",
    "Ram the obstacle", "Destroy everything",
    "Attack the target", "Move 100 meters",
    "Go to full throttle", "Break the barrier",
    "Smash the door", "Collide with box"
]
for t in extra_unsafe:
    dataset.append(make_unsafe(t))

# ─── Shuffle + Save ───────────────────────────────────────

random.shuffle(dataset)

output_path = "data/training/robot_commands.jsonl"
with open(output_path, "w") as f:
    for item in dataset:
        f.write(json.dumps(item) + "\n")

print(f"✅ Dataset generated!")
print(f"📊 Total examples: {len(dataset)}")