#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='normal',
        description="Режим работы"
    )
    
    rate = DeclareLaunchArgument(
        'publish_rate',
        default_value='2.0',
        description="Частота публикации"
    )

    warning_dist = DeclareLaunchArgument(
        'warning_threshold',
        default_value='1.0',
        description="Предупредительная уставка"
    )

    critical_dist = DeclareLaunchArgument(
        'critical_threshold',
        default_value='0.5',
        description="Аварийная уставка"
    )


    publish_rate = PythonExpression(["5.0 if '", LaunchConfiguration('mode'), "' == 'test' else ", LaunchConfiguration('publish_rate')])
    warning_threshold = PythonExpression(["1.5 if '", LaunchConfiguration('mode'), "' == 'test' else ",LaunchConfiguration('warning_threshold')])
    critical_threshold = PythonExpression(["0.8 if '", LaunchConfiguration('mode'), "' == 'test' else ",LaunchConfiguration('critical_threshold')])

    node_1 =  Node(
            package='BB_lab1_pkg',
            executable='dist_sens',
            name="dist_sens",
            output='screen',
            parameters=[
                {'publish_rate': publish_rate},
                {'min_distance': 0.0},
                {'max_distance': 5.0},
                {'sensor_name': 'ultrasonic_front'},
            ],
        )
    
    node_2 = Node(
            package='BB_lab1_pkg',
            executable='dist_monitor',
            name="dist_monitor",
            output='screen',
            parameters=[
                {'warning_threshold': warning_threshold},
                {'critical_threshold': critical_threshold},
            ],
    )
    
    return LaunchDescription([
        mode_arg,
        rate,
        warning_dist,
        critical_dist,
        node_1,
        node_2  
    ])
