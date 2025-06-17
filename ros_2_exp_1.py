import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import time

class EightShapePublisher(Node):

    def __init__(self):
        super().__init__('eight_shape_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer_ = self.create_timer(0.05, self.timer_callback) # 更高的更新频率 (20 Hz)
        self.get_logger().info('Eight shape controller node started. Adjusting parameters for a better 8.')

        # *** 关键参数调整 ***
        self.forward_speed = 2.0  # 直线速度 (m/s) - 越大8字越大
        self.turn_duration = 3.5  # 单次转弯的持续时间 (秒) - 越大转得越慢/圈越大
        self.pause_duration = 0.1 # 每段之间微小的停顿 (秒) - 确保转弯指令清晰
        self.angular_speed = 1.8  # 角速度 (rad/s) - 越大转弯越急

        self.current_time = 0.0
        self.command_start_time = self.get_clock().now().nanoseconds / 1e9
        self.state = 0 # 0:直线, 1:左转, 2:直线, 3:右转, 4:直线, 5:左转, 6:直线, 7:右转

    def timer_callback(self):
        msg = Twist()
        self.current_time = (self.get_clock().now().nanoseconds / 1e9) - self.command_start_time

        # 定义每个阶段的持续时间
        duration_straight = self.turn_duration / 2.0 # 直线阶段持续时间
        duration_turn = self.turn_duration / 2.0     # 转弯阶段持续时间

        # 8字形共有4个转弯和4个直线段，总共8个状态
        # 0: 直线 (开始)
        # 1: 左转 (第一个半圆)
        # 2: 直线 (第一个8字交叉点)
        # 3: 右转 (第二个半圆)
        # 4: 直线 (第二个8字交叉点 - 相当于第一个直线的延续)
        # 5: 左转 (第三个半圆)
        # 6: 直线 (第三个8字交叉点)
        # 7: 右转 (第四个半圆 - 回到起点)

        # 这是一个简化版的逻辑，通过交替直线和转弯实现8字
        # 我们可以把它看作：向前 -> 左弧 -> 向前 -> 右弧 -> (形成一个循环)
        
        # 简化为2个主循环状态：左转和右转，每次持续一定时间
        # 这样更像一个标准的8字形

        # 状态机：0-左转，1-右转
        # 通过不断交替左转和右转来实现8字循环
        
        if self.state == 0: # 移动并左转 (第一个圈的左半边)
            msg.linear.x = self.forward_speed
            msg.angular.z = self.angular_speed # 逆时针
            if self.current_time > self.turn_duration:
                self.state = 1
                self.command_start_time = self.get_clock().now().nanoseconds / 1e9
        elif self.state == 1: # 移动并右转 (第一个圈的右半边，形成交叉)
            msg.linear.x = self.forward_speed
            msg.angular.z = -self.angular_speed # 顺时针
            if self.current_time > self.turn_duration:
                self.state = 0 # 循环回左转，开始下一个8字
                self.command_start_time = self.get_clock().now().nanoseconds / 1e9
        
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    eight_shape_publisher = EightShapePublisher()
    rclpy.spin(eight_shape_publisher)
    eight_shape_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()