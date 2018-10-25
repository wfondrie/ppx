help:
	@echo 'Build the binaries for PyPI upload'
	@echo '    make help: Display this text.'
	@echo '    make clean: Remove old binary builds.'
	@echo '    make build: Build new binaries.'
	@echo '    make update: Update setuptools, wheel, and twine'
	@echo ' '
	@echo 'Normal usage is: update -> clean -> build -> upload'

clean:
	rm -r dist

build:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*

update:
	python3 -m pip install --upgrade setuptools wheel twine

.PHONY: help clean build upload update
