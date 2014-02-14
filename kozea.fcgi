#!/usr/bin/env python3
from flipflop import WSGIServer
from app import app

WSGIServer(app).run()
