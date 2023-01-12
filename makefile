.PHONY: test
test:
	PYTHONPATH=. pytest

pip-install: build
    pip install -e

build: clean
	python -m build

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete