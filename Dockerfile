 # syntax=docker/dockerfile:1
FROM jupyter/scipy-notebook
RUN pip install bash_kernel
RUN python -m bash_kernel.install

WORKDIR /home/jovyan
COPY *.ipynb .
COPY passenger-trips.csv .
ADD images images

 