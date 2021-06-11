from setuptools import setup, find_packages

setup(
    name="model-hub",
    version="0.1",
    description="Model Hub Downloader and Cache",
    author="Manuel Faysse",
    author_email='manuel.fay@gmail.com',
    packages=find_packages(include=["model_hub", "model_hub.*"]),
    install_requires=[
        "tqdm",
        "requests"
    ],
    python_requires=">=3.6,<4.0",
)
