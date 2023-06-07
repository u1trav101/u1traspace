#!/bin/sh
# This project depends on python v3.10 or later
# These commands apply for debian 11
# - libmariadb-dev in the debian repos is too out of date, add the mariadb repo beforehand
# - redis must be installed through the redis repository

sudo apt install libjpeg-dev zlib1g-dev mariad libmariadb3 libmariadb-dev mariadb-server ffmpeg redis
