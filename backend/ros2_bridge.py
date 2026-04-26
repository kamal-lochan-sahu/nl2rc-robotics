import subprocess
import os

def get_ros2_env():
    env = os.environ.copy()
    env["AMENT_PREFIX_PATH"] = "/opt/ros/jazzy"
    env["ROS_DISTRO"] = "jazzy"
    env["ROS_DOMAIN_ID"] = "0"
    env["PATH"] = "/opt/ros/jazzy/bin:" + env.get("PATH", "")
    env["LD_LIBRARY_PATH"] = "/opt/ros/jazzy/lib:" + env.get("LD_LIBRARY_PATH", "")
    env["PYTHONPATH"] = "/opt/ros/jazzy/lib/python3.12/site-packages:" + env.get("PYTHONPATH", "")
    return env

def execute_command(parsed: dict):
    env = get_ros2_env()
    for step in parsed.get("plan", []):
        action = step.get("action")
        params = step.get("params", {})

        if action == "move":
            direction = params.get("direction", "forward")
            distance = params.get("distance", 1.0)
            velocity = params.get("velocity", 0.2)
            linear_x = velocity if direction == "forward" else -velocity

            cmd = [
                "/opt/ros/jazzy/bin/ros2", "topic", "pub",
                "--times", "20", "--rate", "10",
                "/turtle1/cmd_vel",
                "geometry_msgs/msg/Twist",
                f"{{linear: {{x: {linear_x}, y: 0.0, z: 0.0}}, angular: {{x: 0.0, y: 0.0, z: 0.0}}}}"
            ]
            subprocess.run(cmd, env=env, timeout=15)

        elif action == "rotate":
            direction = params.get("direction", "right")
            angle = params.get("angle", 90.0)
            speed = 0.5
            angular_z = speed if direction == "left" else -speed

            cmd = [
                "/opt/ros/jazzy/bin/ros2", "topic", "pub",
                "--times", "20", "--rate", "10",
                "/turtle1/cmd_vel",
                "geometry_msgs/msg/Twist",
                f"{{linear: {{x: 0.0, y: 0.0, z: 0.0}}, angular: {{x: 0.0, y: 0.0, z: {angular_z}}}}}"
            ]
            subprocess.run(cmd, env=env, timeout=15)

        elif action == "stop":
            subprocess.run([
                "/opt/ros/jazzy/bin/ros2", "topic", "pub",
                "--times", "1",
                "/turtle1/cmd_vel",
                "geometry_msgs/msg/Twist",
                "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
            ], env=env)