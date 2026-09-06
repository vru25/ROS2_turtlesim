from setuptools import setup

package_name = 'ros2_assignment_1'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    py_modules=[
        'side_length_publisher',
        'linear_velocity_publisher',
        'edge_duration_subscriber',
    ],
    package_dir={'': 'src'},
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vrus0225',
    maintainer_email='vrus0225@example.com',
    description='ROS 2 assignment package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'side_length_publisher = side_length_publisher:main',
            'linear_velocity_publisher = linear_velocity_publisher:main',
            'edge_duration_subscriber = edge_duration_subscriber:main',
        ],
    },
)
