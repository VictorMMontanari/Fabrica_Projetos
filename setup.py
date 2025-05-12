from setuptools import setup, find_packages

setup(
    name="fabrica_projetos",
    version="0.1",
    packages=find_packages(),
    package_dir={
        '': '.'  # Indica que os pacotes estão na raiz
    },
)