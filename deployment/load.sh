VERSION=8.0.1
tar zxvsf newtranx_server-gpu.v$VERSION.tar.gz && sudo docker image load -i newtranx_server-gpu.v$VERSION.tar
rm newtranx_server-gpu.v$VERSION.tar
./rm.ALL_NONE_IMAGE.sh
sudo docker images

