from setuptools import setup

setup(
    name="shinyutils",
    author="Jayanth Koushik",
    author_email="jnkoushik@gmail.com",
    license="MIT",
    packages=["shinyutils"],
    package_data={"shinyutils": ["data/mplcfg.json"]},
    install_requires=["matplotlib", "seaborn", "crayons"],
    python_requires=">=3.4",
)
