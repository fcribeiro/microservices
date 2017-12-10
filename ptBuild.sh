#!/bin/bash

$REMOTEREPO=/home/jaime/workspace/phd/microservices

git add -u
COMMITMESSAGE="Remote build "$(date +"%D-%T")
git commit -m "$COMMITMESSAGE"
git push
ssh jaime@powertrip.pt "cd ~/workspace/phd/microservices; git pull; ./build.sh"
docker pull jaimelive/users_ms
docker pull jaimelive/main_app




