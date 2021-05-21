PROJECT_NAME = www_kozea
export FLASK_APP = $(PROJECT_NAME)
export FLASK_ENV = development

HOST ?= 0.0.0.0
API_PORT ?= 5000

PYTHON_SRCDIR ?= www_kozea
