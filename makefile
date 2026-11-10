-include web_client/secrets/.env
.PHONY: test

buildpythonpackage: clean
	python -m build

testpackage:
	coverage run -m pytest atlast_sc_tests -s -vv
	coverage report -m

testwebclient:
	coverage run -m pytest fastapi_tests -s -vv
	coverage report -m --omit=atlast_sc/*

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete

GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
