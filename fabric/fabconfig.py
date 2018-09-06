#!/usr/bin/python
# -*- coding:utf-8 -*-


environments = {
    "develop": {
        "hosts": ["xxxxxxx@xx:22"],
        "passwords": {"xxx@xxx:22": "xxxx"},
        "colorize_errors": True,
        "project_name": "eaccount-service",
        "local_path": "../",
        "remote_path": "/home/xxxxxxxx/eaccount-service",
        "build": "docker build -t eaccount-service-nginx ./nginx && docker build -t eaccount-service .",
        "server_up": "docker-compose up -d",
        "server_stop": "docker-compose stop",
        "server_down": "docker-compose down",
        "server_ps": "docker-compose ps",
    },
}
