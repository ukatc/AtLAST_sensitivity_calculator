FROM tiangolo/uwsgi-nginx-flask:python3.9
# See https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask for info on this image

RUN apt update ; \
    apt-get -y install nano

COPY ./ /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt; \
    pip install --no-cache-dir git+https://fkirton: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@github.com/ukatc/AtLAST_sensitivity_calculator.git@main#egg=atlast_sc

