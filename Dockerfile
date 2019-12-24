FROM alpine:latest

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

COPY config/crontab /etc/crontabs/root

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY index.py index.py

CMD ["crond", "-f", "-d", "8"]
