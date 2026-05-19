#!/usr/bin/env python3
import rclpy
import random                   
from rclpy.node import Node        
from std_msgs.msg import Float32

class DistanceSensor(Node):

    def __init__(self):

        super().__init__("dist_sens")

        self.declare_parameter('publish_rate', 2.0) 
        self.declare_parameter('min_distance', 0.0)
        self.declare_parameter('max_distance', 5.0)
        self.declare_parameter('sensor_name', 'ultrasonic_front')

        self.publish_rate = self.get_parameter('publish_rate').value
        self.min_distance = self.get_parameter('min_distance').value
        self.max_distance = self.get_parameter('max_distance').value
        self.sensor_name = self.get_parameter('sensor_name').value

        self.publisher_1 = self.create_publisher(Float32, "/distance", 10)
        self.timer = self.create_timer(1.0 / self.publish_rate, self.timer_callback)

        self.get_logger().info(f"Узел {self.get_name()} запущен с параметрами {self.publish_rate}, {self.min_distance}, {self.max_distance}, {self.sensor_name}")


    def timer_callback(self):
        
        dist_msg = Float32() 

        dist_msg.data = random.uniform(self.min_distance,self.max_distance)
        self.publisher_1.publish(dist_msg)      
        
        self.get_logger().info(f"{dist_msg.data} записано в топик /distance!")  
            

def main():
    rclpy.init()                  


    node = DistanceSensor()               

    try:
        rclpy.spin(node)       
    except KeyboardInterrupt:
        pass                      
    finally:
        node.destroy_node()        
        rclpy.shutdown()            


if __name__ == '__main__':
    main()
