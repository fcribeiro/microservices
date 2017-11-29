#!/bin/bash

#Build Images
( cd Users_MS && docker build -t jaimelive/users_ms . )
( cd Main_App && docker build -t jaimelive/main_app . )
#Push images
docker push jaimelive/users_ms
docker push jaimelive/main_app