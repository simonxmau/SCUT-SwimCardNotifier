#!/bin/bash

scp -r app dev1:/data/docker/SCUT-SwimCardNotifier
scp -r docker dev1:/data/docker/SCUT-SwimCardNotifier
scp -r docker-compose.yml dev1:/data/docker/SCUT-SwimCardNotifier
scp -r Dockerfile dev1:/data/docker/SCUT-SwimCardNotifier
scp -r main.py dev1:/data/docker/SCUT-SwimCardNotifier