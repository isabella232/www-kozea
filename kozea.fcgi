#!/usr/bin/env python3
from flipflop import WSGIServer
import app

WSGIServer(app).run()

