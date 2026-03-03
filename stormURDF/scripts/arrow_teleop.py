#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import curses
import time

class ArrowTeleop(Node):
    def __init__(self):
        super().__init__('arrow_teleop')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Base Velocity settings
        self.speed = 0.6  # Boosted slightly from 0.5
        self.turn = 1.8   # Boosted from 1.5 to overcome 6-wheel friction
        
        # Target vs Current velocity for smoothing
        self.target_linear = 0.0
        self.target_angular = 0.0
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        # Smoothing factor (higher = more instant, lower = smoother)
        self.accel_factor = 0.2 
        
        # Steady publishing timer (20Hz)
        self.timer = self.create_timer(0.05, self.publish_callback)
        
        self.get_logger().info("--- Professional Responsive Teleop ---")
        self.get_logger().info("UP/DOWN: Forward/Back | LEFT/RIGHT: Spin")
        self.get_logger().info("Press 'q' to quit.")

    def update_state(self, key):
        """Updates the target velocity. Resets if no key is found."""
        new_linear = 0.0
        new_angular = 0.0

        if key == curses.KEY_UP:
            new_linear = self.speed
        elif key == curses.KEY_DOWN:
            new_linear = -self.speed
        elif key == curses.KEY_LEFT:
            # Added a tiny extra kick to the left to match the right's feel
            new_angular = self.turn + 0.1 
        elif key == curses.KEY_RIGHT:
            new_angular = -self.turn
        elif key in [ord('q'), ord('Q')]:
            return False
        
        self.target_linear = new_linear
        self.target_angular = new_angular
        return True

    def publish_callback(self):
        """Linearly interpolates to targets and publishes."""
        # Simple Linear Interpolation (Lerp) for smooth acceleration
        # This helps the physics engine not 'stutter'
        self.current_linear += (self.target_linear - self.current_linear) * self.accel_factor
        self.current_angular += (self.target_angular - self.current_angular) * self.accel_factor

        # Round very small values to zero
        if abs(self.current_linear) < 0.01: self.current_linear = 0.0
        if abs(self.current_angular) < 0.01: self.current_angular = 0.0

        msg = Twist()
        msg.linear.x = float(self.current_linear)
        msg.angular.z = float(self.current_angular)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ArrowTeleop()

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    try:
        while rclpy.ok():
            # Clear input buffer to get only the most recent command
            current_key = -1
            while True:
                k = stdscr.getch()
                if k == -1: break
                current_key = k
            
            if not node.update_state(current_key):
                break
            
            rclpy.spin_once(node, timeout_sec=0.01)
            time.sleep(0.01)

    except Exception as e:
        print(f"Teleop Error: {e}")
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        
        if rclpy.ok():
            # Send hard stop
            stop_msg = Twist()
            node.publisher_.publish(stop_msg)
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()