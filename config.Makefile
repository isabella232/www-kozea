API_PORT ?= 5000
HOST ?= 0.0.0.0

export PROJECT_NAME = kozea
export FLASK_APP = $(PWD)/$(PROJECT_NAME).py

# Python env
PYTHON_ONLY = 1
VENV = $(PWD)/.env
PYTHON = python3.7

URL_PROD = https://www.kozea.fr
