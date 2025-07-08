import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    # --- This is the new, crucial part ---
    # Declare a launch argument for use_sim_time
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true', # SET TO TRUE FOR SIMULATION
        description='Use simulation (Gazebo) clock if true'
    )
    # Create a LaunchConfiguration to use the arugment's value
    use_sim_time = LaunchConfiguration('use_sim_time')
    # --- End of new part ---

    # Common parameters for RTAB-Map
    parameters = {
    # --- Core Parameters ---
    'frame_id': 'base_link',
    'subscribe_depth': False,
    'subscribe_rgb': False,
    'subscribe_scan_cloud': True,
    'approx_sync': True,
    'use_sim_time': use_sim_time,

    # --- SLAM & Loop Closure Parameters ---
    'Reg/Strategy': '1',              # 0=Visual, 1=ICP
    'Reg/Force3DoF': 'false',         # <-- CRUCIAL: Set to 'false' to allow for full 6-DoF (3D) motion.
    'Icp/VoxelSize': '0.1',           # Can be slightly larger for 3D to manage performance.
    'Icp/MaxCorrespondenceDistance': '0.3',

    # --- Memory Management (Important for 3D) ---
    'Rtabmap/DetectionRate': '1.0',    # Process a new keyframe at 1 Hz.
    'Mem/RehearsalSimilarity': '0.45', # Helps with loop closure detection.

    # --- You can disable 2D map generation to save resources ---
    'Grid/FromDepth': 'false',
    'Grid/FromScan': 'false',
    'Grid/MapPublishRate': '0.0',     # Set to 0 to disable publishing the 2D map.
}

    # Remappings for the topics
    remappings = [
        ('scan_cloud', '/lidar/velodyne_points'), 
        ('odom', '/odometry/filtered')
    ]

    return LaunchDescription([
        # Add the new launch argument to the description
        use_sim_time_arg,

        # SLAM Node
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            output='screen',
            parameters=[parameters], # The use_sim_time is now inside the dict
            remappings=remappings,
            arguments=['-d']
        ),

        # Viz Node
        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            output='screen',
            parameters=[parameters], # The use_sim_time is now inside the dict
            remappings=remappings
        ),
    ])