From ubuntu:14.04.5

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -yq --no-install-recommends \
    ca-certificates \
    git \
    libhdf5-7 \
    libhdf5-dev \
    libatlas-dev \
    libatlas3gf-base \
    python-dev \
    wget

RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python get-pip.py \
    && rm get-pip.py \
    && git clone https://github.com/simphony/simphony-common.git \
    && cd simphony-common \
    && pip install -r requirements.txt \
    && python setup.py install \
    && cd .. \
    && rm -rf simphony-common \
    && apt-get remove --purge wget -yq \
    && apt-get autoremove -yq \
    && apt-get clean -yq && \
    rm -rf /var/lib/apt/lists/*