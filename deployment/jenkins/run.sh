#!/bin/bash
python --version
rm -r dist/ build/
pyinstaller -y ./server_batch.py
cp -r dist/server_batch/* jenkins_data/SERVER/bin/

DOCKER_VERSION=$(<version)
PREFIX_DOCKER_NAME=newtranx_server-gpu
docker build . -t $PREFIX_DOCKER_NAME:v$DOCKER_VERSION
IMAGE_ID=$(docker images | grep -E "$PREFIX_DOCKER_NAME " | grep -E "${DOCKER_VERSION} " | tr -s ' ' | cut -d ' ' -f3)
# docker image save ${IMAGE_ID} -o $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar
docker image save $PREFIX_DOCKER_NAME:v$DOCKER_VERSION -o $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar
tar zcvf $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar.gz $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar
#
mkdir -p scp
rm scp/*
rm $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar
#
mv $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar.gz scp/$PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar.gz
# sudo scp -P 10086 $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar.gz newtranx@121.46.13.39:/home/newtranx/decoder/
