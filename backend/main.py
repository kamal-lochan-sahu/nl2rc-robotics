import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotCommander(Node):
    def __init__(self):
        super().__init__('robot_commander')
        self.publisher = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10)

    def move_forward(self, speed=0.5, duration=2):
        msg = Twist()
        msg.linear.x = speed
        self.publisher.publish(msg)
        self.get_logger().info(f'Moving forward!')

def main():
    rclpy.init()
    node = RobotCommander()
    node.move_forward()
    rclpy.spin_once(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()