from setuptools import setup

with open("requirements.txt") as req_file:
    requirements = list(map(lambda x: x.strip(), req_file.readlines()))

setup(name='CRUD-users',
      version='0.0.1',
      description="CRUD methods for control users",
      author='Timur',
      author_email='timkin99@mail.ru',
      url="https://github.com/FeltsAzn/FastAPI-user-methods",
      install_requires=requirements
      )
