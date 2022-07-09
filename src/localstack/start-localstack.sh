#!/bin/sh
export COMPOSE_PROJECT_NAME='ginger'
docker-compose pull
docker-compose up $@