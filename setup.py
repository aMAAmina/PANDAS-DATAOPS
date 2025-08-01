from setuptools import setup, find_packages

setup(
    name="pandas-dataops",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.3.1,<2.4",
        "requests>=2.32.4,<3.0",
        "dask>=2025.7.0",
        "dask[distributed]>=2025.7.0"
    ],
)
