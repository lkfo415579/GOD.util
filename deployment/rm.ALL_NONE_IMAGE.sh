sudo docker images | grep none | tr -s " " | cut -f3 -d " " | sudo xargs docker rmi
