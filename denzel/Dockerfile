FROM python
ENV PYTHONUNBUFFERED 1

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip --no-cache-dir install --upgrade" && \
    GIT_CLONE="git clone --depth 10" && \

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
# python
# ------------------------------------------------------------------

    $PIP_INSTALL \
	setup-tools \
	&& \
    $PIP_INSTALL \
	numpy \
	scipy \
	scikit-learn \
	cython \
	&& \

# ==================================================================
# falcon-api
# ------------------------------------------------------------------

    pip install --nobinary :all: falcon	&& \
    $PIP_INSTALL \
    celery \
	gunicorn \
	flower \
	redis \
	&& \

# ==================================================================
# config & cleanup
# ------------------------------------------------------------------

    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*




