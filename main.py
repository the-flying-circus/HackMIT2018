#!/usr/bin/env python3

import eventlet

from flask import Flask, render_template, request, jsonify
from app import app, sio
from routes import sio_test_routes, main_routes, auth_routes


if __name__ == '__main__':
    sio.run(app, debug=True)
