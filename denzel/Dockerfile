FROM python
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/denzel
WORKDIR /opt/denzel
COPY ./requirements.txt /opt/denzel/requirements.txt

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip --no-cache-dir install --upgrade" && \
    GIT_CLONE="git clone --depth 10" && \

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
# falcon-api
# ------------------------------------------------------------------

    $PIP_INSTALL \
        cython \
        --no-binary :all: falcon \
        ujson \
        celery \
        gunicorn \
        requests \
        redis && \

# ==================================================================
# user specific python installations
# ------------------------------------------------------------------

    $PIP_INSTALL -r requirements.txt

# ==================================================================
# config & cleanup
# ------------------------------------------------------------------

RUN ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*

