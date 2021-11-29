from setuptools import setup

setup(
    name="get_time_pp",
    version="0.1",
    description="Show current time",
    author="Dmitry Shirocov",
    author_email="shirocov.dmitry@gmail.com",
    packages=[
        "get_time_namespace.pretty_print_package",
    ],
    install_requires=[
        "requests==2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "get_time_pp=get_time_namespace.pretty_print_package.pretty_print_module:main",
        ]
    },
    namespace_packages=['get_time_namespace']
)