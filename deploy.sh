#!/bin/bash

docker build -t steemdata-phist .
docker tag steemdata-phist furion/steemdata-phist
docker push furion/steemdata-phist
