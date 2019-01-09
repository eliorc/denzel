FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/denzel
WORKDIR /opt/denzel
COPY ./requirements.txt /opt/denzel/requirements.txt

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip --no-cache-dir install --upgrade" && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \

# ==================================================================
# tools
# ------------------------------------------------------------------
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        build-essential \
        ca-certificates \
        cmake \
        wget \
        git \
        nano \
        && \

# ==================================================================
# denzel python essentials
# ------------------------------------------------------------------
    $PIP_INSTALL \
        pip \
        cython \
        --no-binary :all: falcon \
        ujson \
        celery \
        gunicorn \
	    flower \
        requests \
        redis

# ==================================================================
# config & cleanup
# ------------------------------------------------------------------
RUN ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*
