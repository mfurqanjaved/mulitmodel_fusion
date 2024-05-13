from setuptools import setup, find_packages
from typing import List


hyphen_e_dot= "-e ."


def get_requirements(file_path:str) -> List[str]:
    requirements=[]
    with open("requirements.txt") as file_obj:
        requirememts=file_obj.readlines()
        [req.replace("\n","") for req in requirements]

    if hyphen_e_dot in requirements:
        requirements.remove(hyphen_e_dot)
    return requirements


setup(
    name="multimodel_fusion",
    version="0.0.1",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    author="MF_javed",
    author_email="mfurqanjaved@gmail.com"
    
)