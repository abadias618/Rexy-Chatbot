#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: abd
"""

from flask import Flask

app = Flask(__name__)

from app import views
