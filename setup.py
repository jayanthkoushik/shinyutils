from setuptools import setup

setup(
    name="matwrap",
    author="Jayanth Koushik",
    author_email="jnkoushik@gmail.com",
    license="MIT",
    packages=["matwrap"],
    package_data={"matwrap": ["data/default.json"]},
    install_requires=["matplotlib", "seaborn"],
    python_requires=">=3.4",
)
