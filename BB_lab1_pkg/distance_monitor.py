#!/usr/bin/env python3
import rclpy                     
from rclpy.node import Node        
from std_msgs.msg import Float32    

class DistanceMonitor(Node):

    def __init__(self):


        super().__init__('dist_monitor')

        self.declare_parameter('warning_threshold', 1.0)
        self.declare_parameter('critical_threshold', 0.5)
        
        self.warning_threshold = self.get_parameter('warning_threshold').value
        self.critical_threshold = self.get_parameter('critical_threshold').value

        self.subscription = self.create_subscription(
            Float32,
            '/distance',
            self.callback,
            10)

        self.get_logger().info(f"Узел {self.get_name()} запущен c параметрами {self.warning_threshold} и {self.critical_threshold} и слушает топик /distance!")

    def callback(self, msg):
        if msg.data < self.warning_threshold:
            self.get_logger().warn(f"Внимание! Расстояние {msg.data} меньше предупредительной уставки!")
        if msg.data < self.critical_threshold:
            self.get_logger().error(f"Авария! Расстояние {msg.data} меньше аварийной уставки!")
        else:
            self.get_logger().info(f"Текущее расстояние {msg.data}") 

def main():
    rclpy.init()                   
    node = DistanceMonitor()            
    try:
        rclpy.spin(node)         
    except KeyboardInterrupt:
        pass                       
    finally:
        node.destroy_node()       
        rclpy.shutdown()        

if __name__ == '__main__':
    main()