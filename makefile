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

buildwebclientimage:
	@echo "Building web client image for current branch '${GIT_BRANCH}'..."
	# TODO: tag image built from main branch "latest"
	DOCKER_BUILDKIT=1 docker build --no-cache --build-arg BRANCH=${GIT_BRANCH} -t ${GIT_CR_REPO}:${GIT_BRANCH} --secret id=git_secrets,src=web_client/secrets/.env ./web_client
	@echo "Image build complete."

pushwebclientimage: buildwebclientimage
	@echo "Logging in to GitHub Container Registry..."
	@echo ${GIT_CR_PAT} | docker login ghcr.io -u ${GIT_USERNAME} --password-stdin ; \
	echo "Pushing web client image for current branch '${GIT_BRANCH}'..." ; \
	docker push ${GIT_CR_REPO}:${GIT_BRANCH}
	@echo "Push complete."

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete

GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
