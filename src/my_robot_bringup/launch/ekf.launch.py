import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import LifecycleNode


def generate_launch_description():
    ekf_config = os.path.join(
        get_package_share_directory('my_robot_bringup'),
        'config',
        'ekf.yaml'
    )


    slam_toolbox_config = os.path.join(
        get_package_share_directory('my_robot_bringup'),'config','mapper_params_online_async.yaml')

    return LaunchDescription([
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config,{'use_sim_time': True}]
        ),

        # LifecycleNode(
        #     package='slam_toolbox',
        #     executable='async_slam_toolbox_node',
        #     name='slam_toolbox',
        #     output='screen',
        #     parameters=[slam_toolbox_config,{
        #     'use_lifecycle_manager': False,
        #     'use_sim_time': True}],
        #     namespace=''          
        # )
    ])
