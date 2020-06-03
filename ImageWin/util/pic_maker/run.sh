docker container rm ig-maintain
docker image rm ig
docker build -t ig .
docker run --name ig-maintain -it ig bash

