# k-anonymity

Jupyter Lab environment to demonstrate containerised labs for both scipy and bash

## Pre-requisites

Have docker installed and running

## Build

To build the container run the following in a terminal

```/bin/sh
docker build -t eusholli:k-anon .

This builds a docker image named eusholli:k-anon using the [Dockerfile](./Dockerfile).  For demonstration purposes this also installs additional bash kernal to show how to build different environment support for workbooks.
```

## Start containerized Lab

To run a containerized instance execute

```/bin/sh
run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "${PWD}/common":/home/jovyan/common eusholli:k-anon
```

To run a second container instance (change the port mapping)

```/bin/sh
run --rm -p 8080:8888 -e JUPYTER_ENABLE_LAB=yes -v "${PWD}/common":/home/jovyan/common eusholli:k-anon
```

Look for the url in the startup logging that allows access through the browser. Note you need to use the external port to connect to the second container (e.g. 8080)

The workbook is individual per container. There is a mapping to a common directory that when written is shared by all containers. (the directory is created within the starting directory)
