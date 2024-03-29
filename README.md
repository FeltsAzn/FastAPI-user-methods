# Implementation of resource access

A simple FastAPI application for user access to the service via GET, POST, PUT, DELETE.

Database for storing information: PostreSQL

Implemented protection against external access based on the **jwt** library.

When a new user is created or an old user is authorized, a JWT token is issued to access application handlers.

Each issued token has a lifetime of 1 hour (checking the creation of the token and its lifetime is implemented).

The application is completely asynchronous.

___________________________________________________

## Local deployment

Copy via terminal repository:
```bash
git clone https://github.com/FeltsAzn/FastAPI-user-methods
```

#### If you are working with code editors `vim`, `nano`, `notepad` and others:
Installing a virtual environment if you don't have one locally.
```bash
python3 -m pip install --user virtualenv
```

Create a virtual environment in the copied repository:
```bash
python3 -m venv env
```

Activate the virtual environment:
```bash
source env/bin/activate
```

Install the dependency file in the virtual environment:
```bash
(venv):~<project path>$ pip install -r requirements.txt
```

Create a `.env` file in the `bot` folder
```bash
touch.env
```

#### If you are using the IDE:
Create a ***.env*** file in the ***bot*** project folder


Contents of the `.env` file
```sh
DATABASE = postgresql+asyncpg://{user}:{passsword}@localhost/postgres
SECRET_KEY = {secretkey}
JWT_KEY = {secret phrase with hs256 (or another) encrypt}
JWT_ALGORITHM = 'HS256'
```

#### Docker container
You can deploy the application on a server or locally in a container using ***dockerfile***:
```bash
docker build . -t <image name>
```

And run the built image in a container:
```bash
docker run -d <image name>
```


![изображение](https://user-images.githubusercontent.com/107147438/197282935-a64f1bc2-5323-4275-b302-04b6a545767d.png)
