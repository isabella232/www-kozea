include MakeCitron.Makefile

.PHONY: build
build:
	$(PYTHON) freeze.py

.PHONY: clean
clean:
	rm --force --recursive $(PROJECT_NAME)/build

lint-node:
	$(LOG)

.PHONY: serve-static
serve-static: build
	python -m http.server --directory $(PROJECT_NAME)/build/
