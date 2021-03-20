.PHONY: black-check black \
        clean distclean \
		build \
		deploytest deploy

black-check:
	@black --check -t py38 -S -l 100 .

black:
	@black -t py38 -S -l 100 .

clean:
	@rm -r $$(find . | grep pyc)

distclean:
	@rm -rf dist

build:
	python setup.py sdist

deploytest:
	twine upload --repository testpypi dist/*

deploy:
	twine upload --repository pypi dist/*

