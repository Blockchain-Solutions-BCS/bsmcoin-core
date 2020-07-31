FROM phusion/baseimage:0.11

RUN apt-get update && \
    apt-get install -y &&\
    g++ \
    autoconf \
    cmake \
    git \
    libboost-all-dev \


    # NavBS install
    git clone https://github.com/blockchain-solutions-bcs/navcoin-core && \
    cd navcoin-core/depends && \
    make && \
    cd .. && \
    ./autogen.sh && ./configure && \
    make && make install

ENTRYPOINT ./src/navcoid 

STOPSIGNAL SIGINT