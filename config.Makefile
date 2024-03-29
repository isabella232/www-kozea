PROJECT_NAME = www_kozea
export FLASK_APP = $(PROJECT_NAME)
export FLASK_CONFIG ?= $(PWD)/application.cfg
export FLASK_ENV = development

HOST ?= 0.0.0.0
API_PORT ?= 5000

PYTHON ?= python3.8
PYTHON_SRCDIR ?= www_kozea
PYTHON_ONLY ?= 1
VENV ?= $(PWD)/.env

URL_PROD = https://www.kozea.fr

# Disable API endpoint tests
URL_PROD_API =
URL_TEST_API =
