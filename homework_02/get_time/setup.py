from setuptools import setup, find_namespace_packages

setup(
    name="get_time_packages",
    version="0.1",
    description="Show current time",
    author="Dmitry Shirocov",
    author_email="shirocov.dmitry@gmail.com",
    packages=["get_time_namespace.get_time_package"],
    install_requires=[
        "requests==2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "get_time=get_time_namespace.get_time_package.get_time_module:main",
        ]
    },
    namespace_packages = ['get_time_namespace']
)