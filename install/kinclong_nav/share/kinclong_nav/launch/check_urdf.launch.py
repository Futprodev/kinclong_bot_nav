import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_kinclong_nav = get_package_share_directory('kinclong_nav')

    gazebo_models_path, ignore_last_dir = os.path.split(pkg_kinclong_nav)
    os.environ["GZ_SIM_RESOURCE_PATH"] += os.pathsep + gazebo_models_path

    rviz_launch_arg = DeclareLaunchArgument(
        'rviz', default_value='true',
        description='Open RViz'
    )

    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config', default_value='rviz.rviz',
        description='RViz config file'
    )


    model_arg = DeclareLaunchArgument(
        'model', default_value='mogi_bot.urdf',
        description='Name of the URDF description to load'
    )

    x_arg = DeclareLaunchArgument(
        'x', default_value='2.5',
        description='x coordinate of spawned robot'
    )

    y_arg = DeclareLaunchArgument(
        'y', default_value='1.5',
        description='y coordinate of spawned robot'
    )

    yaw_arg = DeclareLaunchArgument(
        'yaw', default_value='-1.5707',
        description='yaw angle of spawned robot'
    )

    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='True',
        description='Flag to enable use_sim_time'
    )

    # Define the path to your URDF or Xacro file
    urdf_file_path = PathJoinSubstitution([
        pkg_kinclong_nav,  # Replace with your package name
        "urdf",
        LaunchConfiguration('model')  # Replace with your URDF or Xacro file
    ])

    # # Launch rviz
    # rviz_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     arguments=['-d', PathJoinSubstitution([pkg_kinclong_nav, 'rviz', LaunchConfiguration('rviz_config')])],
    #     condition=IfCondition(LaunchConfiguration('rviz')),
    #     parameters=[
    #         {'use_sim_time': LaunchConfiguration('use_sim_time')},
    #     ]
    # )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': Command(['xacro', ' ', urdf_file_path]),
             'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    launchDescriptionObject = LaunchDescription()

    launchDescriptionObject.add_action(model_arg)
    launchDescriptionObject.add_action(x_arg)
    launchDescriptionObject.add_action(y_arg)
    launchDescriptionObject.add_action(yaw_arg)
    launchDescriptionObject.add_action(sim_time_arg)
    # launchDescriptionObject.add_action(rviz_node)
    launchDescriptionObject.add_action(robot_state_publisher_node)

    return launchDescriptionObject
