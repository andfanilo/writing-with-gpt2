from os.path import dirname
from os.path import join
import setuptools


setuptools.setup(
    name="writing-with-transformers-server",
    version="0.1.0",
    author="Fanilo ANDRIANASOLO",
    author_email="andfanilo@gmail.com",
    description="",
    long_description="",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "fastapi==0.61.1",
        "transformers",
        "typer==0.3.2",
        "uvicorn==0.11.8"
    ],
)
