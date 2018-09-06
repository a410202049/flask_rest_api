#!/usr/bin/python
# -*- encoding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os

from config import get_config
from server.app import create_app
from task import make_celery

config_name = os.path.basename(__file__)
app = create_app(get_config(config_name[:config_name.find('.')]))
celery = make_celery(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
