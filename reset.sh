docker cp ig_process_container:/home/ImageWin/util/db/ "$(pwd)"/ImageWin/util/
docker cp ig_process_container:/home/ImageWin/log/ "$(pwd)"/ImageWin/

docker stop ig_process_container
docker container rm ig_process_container
docker image rm ig_process_image_py37

docker build ./ --tag ig_process_image_py37
docker run -it --name ig_process_container ig_process_image_py37
