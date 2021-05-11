#交互方式开启docker 后面有个.
docker-compose up -d --build 更新镜像
docker build -t recruitment-base:0.0.1 .
docker run -it --rm -p 8000:8000 --entrypoint /bin/sh recruitment-base:0.0.1
docker run --rm -p 8000:8000 -v "$(pwd)":/data/recruitment --env server_params="--settings=settings.local" recruitment-base:0.0.1
docker run --rm -p 8000:8000 -v E:\PycharmProject\recruitment:/data/recruitment --env server_params="--settings=settings.local" recruitment-base:0.0.1