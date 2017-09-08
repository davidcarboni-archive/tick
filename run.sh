#!/usr/bin/env bash
docker-compose pull
docker-compose build --pull
docker-compose up -d --remove-orphans
docker-compose logs --follow
