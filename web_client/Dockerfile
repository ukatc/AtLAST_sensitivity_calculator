FROM python:3.10

ARG BRANCH=main

# Add a label to associate image with AtLast repo
LABEL org.opencontainers.image.source=https://github.com/ukatc/atlast_sensitivity_calculator
LABEL org.opencontainers.image.description="Container image for AtLast Sensitivity Calculator web client"
LABEL org.opencontainers.image.licenses=MIT

RUN apt update ; \
    apt-get -y install nano

WORKDIR /app

COPY ./ /app/web_client

RUN pip install --no-cache-dir --upgrade -r /app/web_client/requirements.txt

# TODO allow installing from a local branch
RUN --mount=type=secret,id=git_secrets . /run/secrets/git_secrets \
    && pip install --no-cache-dir git+https://${GIT_USERNAME}:${GIT_PAT}@github.com/ukatc/AtLAST_sensitivity_calculator.git@${BRANCH}#egg=atlast_sc

CMD ["python", "-m", "web_client.main"]