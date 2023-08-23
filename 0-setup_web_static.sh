#!/usr/bin/env bash
# Set up Web Servers

apt-get update -y
apt-get install -y nginx
if ! [[ -d /data ]]
then
        mkdir -p "/data/web_static/releases/test/"
        mkdir -p "/data/web_static/shared/"
        echo 'Hello Moto !' > "/data/web_static/releases/test/index.html"
        ln -s  "/data/web_static/releases/test" "/data/web_static/current"
fi
chown -R ubuntu:ubuntu /data
if [[ $(grep -c "location \/hbnb_static\/" /etc/nginx/sites-enabled/default) -eq 0 ]]
then
        sed -i "s/^\}$/\tlocation \/hbnb_static\/ \{\n\t\talias \/data\/web_static\/current\/\;\n\t\}\n\}/" /etc/nginx/sites-enabled/default
fi
service nginx restart
