from setuptools import find_packages, setup

package_name = "autonomy_mission_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="dev",
    maintainer_email="dev@example.com",
    description="Mission bridge node",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "mission_bridge_node = autonomy_mission_bridge.mission_bridge_node:main",
        ],
    },
)
