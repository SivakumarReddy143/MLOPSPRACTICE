"""
Setup the python using setuptools
"""
from typing import List
from setuptools import setup,find_packages
def requirements()-> List:
    try:
        with open("requirements.txt",'r') as file:
            requirements_lst:List[str] =[]
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!= "-e .":
                    requirements_lst.append(requirement)
    except Exception as e:
        print(e)
    return requirements_lst


setup(
    name="MlopsProject",
    author="Sivakumar",
    author_email="mshivakumarreddy78@gmail.com",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements()
)
