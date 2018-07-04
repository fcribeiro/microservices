#!/bin/bash

# Delete images
docker rmi fcribeiro/aggregator_ms_p3
docker rmi fcribeiro/authentication_ms_p3
docker rmi fcribeiro/playlists_ms_p3
docker rmi fcribeiro/songs_ms_p3
docker rmi fcribeiro/users_ms_p3


# Aggregator
cd Aggregator_MS
docker build -t fcribeiro/aggregator_ms_p3 .
cd ..

# Authentication
cd Authentication_MS
docker build -t fcribeiro/authentication_ms_p3 .
cd ..

# Playlists
cd Playlists_MS
docker build -t fcribeiro/playlists_ms_p3 .
cd ..

# Songs
cd Songs_MS
docker build -t fcribeiro/songs_ms_p3 .
cd ..

# Users
cd Users_MS
docker build -t fcribeiro/users_ms_p3 .
cd ..


# Upload images to docker hub
docker push fcribeiro/aggregator_ms_p3
docker push fcribeiro/authentication_ms_p3
docker push fcribeiro/playlists_ms_p3
docker push fcribeiro/songs_ms_p3
docker push fcribeiro/users_ms_p3
