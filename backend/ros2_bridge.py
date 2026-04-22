import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TurtleController(Node):
    def __init__(self):
        super().__init__('nl2rc_controller')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def move(self, direction, distance, velocity=0.2):
        msg = Twist()
        if direction == "forward":
            msg.linear.x = velocity
        elif direction == "backward":
            msg.linear.x = -velocity
        
        duration = distance / velocity
        end_time = time.time() + duration
        
        while time.time() < end_time:
            self.publisher.publish(msg)
            time.sleep(0.1)
        
        # Stop
        self.publisher.publish(Twist())

    def rotate(self, direction, angle):
        msg = Twist()
        speed = 0.5
        msg.angular.z = speed if direction == "left" else -speed
        duration = (angle * 3.14159) / (180 * speed)
        end_time = time.time() + duration
        
        while time.time() < end_time:
            self.publisher.publish(msg)
            time.sleep(0.1)
        
        self.publisher.publish(Twist())

def execute_command(parsed: dict):
    rclpy.init()
    node = TurtleController()
    
    for step in parsed.get("plan", []):
        action = step.get("action")
        params = step.get("params", {})
        
        if action == "move":
            node.move(
                params.get("direction", "forward"),
                params.get("distance", 1.0),
                params.get("velocity", 0.2)
            )
        elif action == "rotate":
            node.rotate(
                params.get("direction", "right"),
                params.get("angle", 90.0)
            )
        elif action == "stop":
            node.publisher.publish(Twist())
    
    node.destroy_node()
    rclpy.shutdown()
