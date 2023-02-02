FROM tiangolo/uwsgi-nginx-flask:python3.9
# See https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask for info on this image

ARG BRANCH=main

# Add a label to associate image with AtLast repo
LABEL org.opencontainers.image.source=https://github.com/ukatc/atlast_sensitivity_calculator
LABEL org.opencontainers.image.description="Container image for AtLast Sensitivity Calculator web client"
LABEL org.opencontainers.image.licenses=MIT

RUN apt update ; \
    apt-get -y install nano

COPY ./ /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN --mount=type=secret,id=git_secrets . /run/secrets/git_secrets \
    && pip install --no-cache-dir git+https://${GIT_USERNAME}:${GIT_PAT}@github.com/ukatc/AtLAST_sensitivity_calculator.git@${BRANCH}#egg=atlast_sc
