# Practical Test
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Architecture
### AWS
[![](https://i.ibb.co/b30cft4/aws-drawio.png)]

### GCP

[![](https://i.ibb.co/F3vqzXZ/gcp-Pa-gina-2-drawio.png)]

## Installation

Practical test requires permission in the project folder in order to execute the apply.sh file that contains all the project settings. 

Follow the following commands in the terminal

```sh
cd practical_test
chmod +x apply.sh
```

## Deploy

In order to deploy the application you must follow the following commands:

```sh
cd practical_test
./apply.sh
```

To stop the application:

```sh
docker stop [id_container]
```


## API 

### Ingest Data

Input variables:
 
| Parameter | Value |
| ------ | ------ |
| Method | POST |
| Host | localhost:4000/api/ingest |
| Body type | Multipart Form |
| Body name input | file |

##### Example

[![](https://i.ibb.co/jVbf2TG/Captura-de-pantalla-2023-07-05-a-la-s-03-39-56.png)]

### Number Employee by year

Input variables:
 
| Parameter | Value |
| ------ | ------ |
| Method | POST |
| Host | localhost:4000/api/employee/number_by_year |
| Body type | json |
| Body name input | year |

##### Example

[![](https://i.ibb.co/RCCHDyr/Captura-de-pantalla-2023-07-05-a-la-s-03-46-12.png)]

### Number Employee by department

Input variables:
 
| Parameter | Value |
| ------ | ------ |
| Method | POST |
| Host | localhost:4000/api/employee/list_by_deparment |
| Body type | json |
| Body name input | year |

##### Example

[![](https://i.ibb.co/L1FGpGC/Captura-de-pantalla-2023-07-05-a-la-s-03-50-42.png)]

## Docker

This is very easy to install and deploy in a Docker container.

the Docker will expose port 4000, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

Dockerfile

```sh
FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set environment variables
ENV FLASK_APP=api.py

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip3 install --user -r requirements.txt
EXPOSE 4000
CMD ./entrypoint.sh
```

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 4000 of the host to
port 4000 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker build -t globantcompiler:1.0.0 .
docker run --name flasgger -p 4000:4000 -d globantcompiler:1.0.0
```


Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:4000
```

## License

MIT

**Free Software, Hell Yeah!**
