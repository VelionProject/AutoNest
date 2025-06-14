from setuptools import setup, find_packages

setup(
    name="autonest",
    version="0.3",
    packages=find_packages(),
    install_requires=["openai", "requests"],
    entry_points={"console_scripts": ["autonest=core.main:main"]},
    author="Solen",
    description="Semantic Python code inserter with GPT and GUI support",
)
