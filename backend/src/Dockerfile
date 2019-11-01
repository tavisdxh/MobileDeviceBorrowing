FROM python:3.7.5-buster

LABEL maintainer="TavisD <tavisdxh@outlook.com>"

WORKDIR /data/src

COPY requirements.txt /data/src/requirements.txt

RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && rm -rf /var/lib/apt \
    && pip install --no-cache-dir -r /data/src/requirements.txt

#CMD ["/bin/bash","/data/src/scripts/run.sh"]

#CMD ["tail", "-f", "/dev/null"]