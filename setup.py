from setuptools import find_packages
from setuptools import setup

setup(
    name="readwise_onyx_boox",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "black",
        "plyer==2.1.0",
        "tqdm==4.65.0",
        "requests",
        "pydantic",
        "python-dotenv",
        "omegaconf",
        "streamlit",
    ],
    author="Adam Szummer",
)
