import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os
from ament_index_python.packages import get_package_share_path,get_package_share_directory

def generate_launch_description():

    default_model_path = os.path.join(get_package_share_path('my_robot_description'),
                             'urdf', 'my_robot.urdf.xacro')
    default_rviz_config_path = os.path.join(get_package_share_path('my_robot_bringup'),
                                    'rviz', 'urdf_config.rviz')
    default_ekf_config_path = os.path.join(get_package_share_directory('my_robot_bringup'),
                                    'config', 'ekf.yaml')
    

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )


    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
     )
    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-topic', 'robot_description'],
        output='screen'
    )

    robot_localization_node = launch_ros.actions.Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[default_ekf_config_path,{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )   


    return launch.LaunchDescription([

        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),

        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        
        launch.actions.ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
              output='screen'
        ),

        robot_state_publisher_node,
        spawn_entity,
        robot_localization_node,
        rviz_node,
    ])