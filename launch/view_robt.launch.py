import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    # The name of your package
    pkg_name = 'roboURDF'
    
    # Path to the rsp.launch.py
    rsp_launch_path = os.path.join(get_package_share_directory(pkg_name), 'launch', 'rsp.launch.py')

    # Path to your RViz config
    rviz_config_path = os.path.join(get_package_share_directory(pkg_name), 'config', 'view_bot.rviz')

    # 1. Include the Robot State Publisher (RSP)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rsp_launch_path]),
        launch_arguments={'use_sim_time': 'false'}.items()
    )

    # 2. Joint State Publisher GUI
    jsp_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # 3. RViz2
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
    )

    return LaunchDescription([
        rsp,
        jsp_gui,
        rviz
    ])