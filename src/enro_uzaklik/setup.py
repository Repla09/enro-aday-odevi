from setuptools import find_packages, setup

package_name = 'enro_uzaklik'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Alpar Garib',
    maintainer_email='garibalper@gmail.com',
    description='Service and client nodes that check the distance between the robot and a target',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            # ros2 run enro_uzaklik <name>  ->  runs main() in that file
            'uzaklik_sunucu = enro_uzaklik.uzaklik_sunucu:main',
            'uzaklik_istemci = enro_uzaklik.uzaklik_istemci:main',
        ],
    },
)
