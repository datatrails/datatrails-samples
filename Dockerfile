ARG VERSION=3.6
FROM python:${VERSION}-buster

COPY requirements.txt requirements-dev.txt /tmp/

RUN python3 -m pip -qq install --upgrade pip \
  && python3 -m pip -qq install -r /tmp/requirements-dev.txt \
  && rm -f /tmp/requirements-dev.txt \
  && rm -f /tmp/requirements.txt

ENV USER=api
ENV HOME=/home/${USER}
RUN mkdir -p ${HOME}
ENV PYTHONPATH=${HOME}/samples:${PYTHONPATH}
ENV PATH=${HOME}/.local/bin:${PATH}
WORKDIR ${HOME}
