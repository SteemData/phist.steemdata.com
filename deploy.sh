#!/bin/bash

docker build -t steemdata-ph .
docker tag steemdata-ph furion/steemdata-ph
docker push furion/steemdata-ph
