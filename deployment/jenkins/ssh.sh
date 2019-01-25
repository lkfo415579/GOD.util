REMOTE=/home/newtranx/decoder/test_jenkins
VERSION=$(ls -t $REMOTE/*.tar.gz | head -n 1 | grep -E -o "([0-9]\.)+" | sed 's/.$//g')
echo $VERSION > $REMOTE/version
echo $VERSION >> delpoy.test
cd $REMOTE && ./load.sh $VERSION
