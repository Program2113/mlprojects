from setuptools import find_packages,setup
from typing import List
def get_requirements(file_path:str)->List[str]:
    '''
    this function returns the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [line.replace('\n','')for line in requirements]
        if "-e ." in requirements:
            requirements.remove('-e .')
            
    return requirements    


setup(
    name = 'mlproject',
    version = '0.0.1',
    author = 'Satya Bharadwaj',
    author_email = 'bharadwajpendyala2113@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')

)
