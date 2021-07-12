include MakeCitron.Makefile

.PHONY: build
build:
	python freeze.py

.PHONY: clean
clean:
	rm --force --recursive $(PROJECT_NAME)/build

lint-node:
	$(LOG)
