#!/bin/bash
# build pipinstaller
python --version
# rm -r dist/ build/
# pyinstaller -y ./server_batch.py
cp -r dist/server_batch/* jenkins_data/SERVER/bin/
# build docker image
DOCKER_VERSION=$(<version)
# Get project
PROJECT=$(cat project)
PREFIX_DOCKER_NAME=newtranx_server-gpu
docker build . -t $PREFIX_DOCKER_NAME:v$DOCKER_VERSION
# IMAGE_ID=$(docker images | grep -E "$PREFIX_DOCKER_NAME " | grep -E "${DOCKER_VERSION} " | tr -s ' ' | cut -d ' ' -f3)
docker image save $PREFIX_DOCKER_NAME:v$DOCKER_VERSION -o $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar
tar zcvf $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar.gz $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar
# move image to scp folder
mkdir -p scp
rm scp/*
rm $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar
mv $PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar.gz scp/$PREFIX_DOCKER_NAME.v${DOCKER_VERSION}.tar.gz

###POST SCRIPT ON REMOTE SERVER
REMOTE=/home/newtranx/decoder/test_jenkins
VERSION=$(ls -t $REMOTE/*.tar.gz | head -n 1 | grep -E -o "([0-9]\.)+" | sed 's/.$//g')
echo $VERSION > $REMOTE/version
echo $VERSION >> delpoy.test
cd $REMOTE && ./load.sh $VERSION
