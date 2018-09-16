#!/usr/bin/env python3

import eventlet

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from time import sleep
from app import app, sio
from routes import sio_test_routes, main_routes, auth_routes


if __name__ == '__main__':
    sio.run(app, debug=True)
