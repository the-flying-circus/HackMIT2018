#!/usr/bin/env python3

import eventlet

from flask import Flask, render_template, request, jsonify
from app import app, sio, db
from routes import sio_test_routes, main_routes, auth_routes, chat_routes


@app.before_first_request
def setup_db():
    db.create_all(app=app)


if __name__ == '__main__':
    sio.run(app, debug=True)
