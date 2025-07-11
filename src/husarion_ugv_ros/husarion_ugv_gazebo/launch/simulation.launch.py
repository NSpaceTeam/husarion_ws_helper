#!/usr/bin/env python3

# Copyright 2024 Husarion sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node, SetUseSimTime
from launch_ros.substitutions import FindPackageShare
from nav2_common.launch import ReplaceString


def generate_launch_description():

    gz_gui = LaunchConfiguration("gz_gui")
    declare_gz_gui = DeclareLaunchArgument(
        "gz_gui",
        default_value=PathJoinSubstitution(
            [FindPackageShare("husarion_ugv_gazebo"), "config", "teleop_with_estop.config"]
        ),
        description="Run simulation with specific GUI layout.",
    )

    log_level = LaunchConfiguration("log_level")
    declare_log_level_arg = DeclareLaunchArgument(
        "log_level",
        default_value="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"],
        description="Logging level",
    )

    namespace = LaunchConfiguration("namespace")
    declare_namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value=EnvironmentVariable("ROBOT_NAMESPACE", default_value=""),
        description="Add namespace to all launched nodes.",
    )

    use_rviz = LaunchConfiguration("use_rviz")
    declare_use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="True",
        description="Run RViz simultaneously.",
        choices=["True", "true", "False", "false"],
    )

    namespaced_gz_gui = ReplaceString(
        source_file=gz_gui,
        replacements={"{namespace}": namespace},
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("husarion_gz_worlds"), "launch", "gz_sim.launch.py"]
            )
        ),
        launch_arguments={"gz_gui": namespaced_gz_gui, "gz_log_level": "1"}.items(),
    )

    gz_bridge_config = PathJoinSubstitution(
        [FindPackageShare("husarion_ugv_gazebo"), "config", "gz_bridge.yaml"]
    )
    gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="gz_bridge",
        parameters=[{"config_file": gz_bridge_config}],
    )

    simulate_robots = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("husarion_ugv_gazebo"),
                    "launch",
                    "simulate_robot.launch.py",
                ]
            )
        ),
        launch_arguments={"log_level": log_level}.items(),
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("husarion_ugv_description"),
                    "launch",
                    "rviz.launch.py",
                ]
            )
        ),
        condition=IfCondition(use_rviz),
    )
    zed_cam_bridge_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("ros_components_description"), # Assuming this is the package where gz_lidar_slamtec_launch.py is
                    "launch", # Or whatever subdirectory it's in
                    "gz_stereolabs_zed.launch.py", # The name of THIS file
                ]
            )
        ),
        launch_arguments={
            "robot_namespace": namespace, 
            "device_namespace": "front_cam", # Pass the main namespace
            # "device_namespace": "lidar", # Optional: if you want to further namespace this specific lidar
                                          # If not passed, it will use the default "" from its own declaration
            # "gz_bridge_name": "lidar_bridge" # Optional: to give it a unique name if you have other bridges
        }.items(),
    )
    zed_cam_bridge_launch_front = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("ros_components_description"), # Assuming this is the package where gz_lidar_slamtec_launch.py is
                    "launch", # Or whatever subdirectory it's in
                    "gz_stereolabs_zed.launch.py", # The name of THIS file
                ]
            )
        ),
        launch_arguments={
            "robot_namespace": namespace, 
            "device_namespace": "front_cam", # Pass the main namespace
            # "device_namespace": "lidar", # Optional: if you want to further namespace this specific lidar
                                          # If not passed, it will use the default "" from its own declaration
            # "gz_bridge_name": "lidar_bridge" # Optional: to give it a unique name if you have other bridges
        }.items(),
    )
    zed_cam_bridge_launch_back = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("ros_components_description"), # Assuming this is the package where gz_lidar_slamtec_launch.py is
                    "launch", # Or whatever subdirectory it's in
                    "gz_stereolabs_zed.launch.py", # The name of THIS file
                ]
            )
        ),
        launch_arguments={
            "robot_namespace": namespace, 
            "device_namespace": "back_cam", # Pass the main namespace
            # "device_namespace": "lidar", # Optional: if you want to further namespace this specific lidar
                                          # If not passed, it will use the default "" from its own declaration
            # "gz_bridge_name": "lidar_bridge" # Optional: to give it a unique name if you have other bridges
        }.items(),
    )
    zed_cam_bridge_launch_left = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("ros_components_description"), # Assuming this is the package where gz_lidar_slamtec_launch.py is
                    "launch", # Or whatever subdirectory it's in
                    "gz_stereolabs_zed.launch.py", # The name of THIS file
                ]
            )
        ),
        launch_arguments={
            "robot_namespace": namespace, 
            "device_namespace": "left_cam", # Pass the main namespace
            # "device_namespace": "lidar", # Optional: if you want to further namespace this specific lidar
                                          # If not passed, it will use the default "" from its own declaration
            # "gz_bridge_name": "lidar_bridge" # Optional: to give it a unique name if you have other bridges
        }.items(),
    )
    zed_cam_bridge_launch_right = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("ros_components_description"), # Assuming this is the package where gz_lidar_slamtec_launch.py is
                    "launch", # Or whatever subdirectory it's in
                    "gz_stereolabs_zed.launch.py", # The name of THIS file
                ]
            )
        ),
        launch_arguments={
            "robot_namespace": namespace, 
            "device_namespace": "right_cam", # Pass the main namespace
            # "device_namespace": "lidar", # Optional: if you want to further namespace this specific lidar
                                          # If not passed, it will use the default "" from its own declaration
            # "gz_bridge_name": "lidar_bridge" # Optional: to give it a unique name if you have other bridges
        }.items(),
    )
    lidar_bridge_launch= IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("ros_components_description"), # Assuming this is the package where gz_lidar_slamtec_launch.py is
                    "launch", # Or whatever subdirectory it's in
                    "gz_velodyne.launch.py", # The name of THIS file
                ]
            )
        ),
        launch_arguments={
            "robot_namespace": namespace, 
            "device_namespace": "lidar", # Pass the main namespace
            # "device_namespace": "lidar", # Optional: if you want to further namespace this specific lidar
                                          # If not passed, it will use the default "" from its own declaration
            # "gz_bridge_name": "lidar_bridge" # Optional: to give it a unique name if you have other bridges
        }.items(),
    )
    actions = [
        declare_gz_gui,
        declare_log_level_arg,
        declare_namespace_arg,
        declare_use_rviz_arg,
        SetUseSimTime(True),
        gz_sim,
        gz_bridge,
        simulate_robots,
        rviz_launch,
        zed_cam_bridge_launch_front,
        zed_cam_bridge_launch_back,
        zed_cam_bridge_launch_left,
        zed_cam_bridge_launch_right,
        lidar_bridge_launch,
    ]

    return LaunchDescription(actions)
