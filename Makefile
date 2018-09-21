clean:
	rm -r dist

build:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*

.PHONY: clean, build, upload
