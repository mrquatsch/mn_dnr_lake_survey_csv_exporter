#!/bin/bash

docker build -f docker/Dockerfile . -t mn_dnr:latest
docker run --name mn_dnr_exporter --rm -v $PWD:/output mn_dnr:latest
