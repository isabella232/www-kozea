include MakeCitron.Makefile

.PHONY: build
build: $(PROJECT_NAME)/static/tailwind.css
	python freeze.py

$(PROJECT_NAME)/static/tailwind.css: $(PROJECT_NAME)/static/style.css
	tailwindcss build $< -o $@

.PHONY: clean
clean:
	rm --force --recursive $(PROJECT_NAME)/build

lint-node:
	$(LOG)
