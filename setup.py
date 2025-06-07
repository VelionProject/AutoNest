from setuptools import setup, find_packages

setup(
    name="autonest",
    version="0.2",
    packages=find_packages(),
    install_requires=["openai"],
    entry_points={"console_scripts": ["autonest-gui=interface.autonest_gui:main"]},
    author="Solen",
    description="Semantic Python code inserter with GPT and GUI support",
)
