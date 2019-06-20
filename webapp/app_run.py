# coding: utf-8
# @Time    : 2019-04-24 21:00
# @Author  : DesertsX
# @Site    : 
# @File    : app_run.py

import os
import sys
from flask import Flask

sys.path.append(".." + os.path.sep)
from webapp.views.graph_view import graph

app = Flask(__name__)
app.register_blueprint(graph)

if __name__ == '__main__':
    app.run()
