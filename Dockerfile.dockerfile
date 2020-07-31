FROM clangbuiltlinux/ubuntu:latest

RUN apt-get update && \
    apt-get upgrade -y &&\

    # NavBS install
    git clone https://github.com/blockchain-solutions-bcs/navcoin-core && \
    cd navcoin-core/depends && \
    make && \
    cd .. && \
    ./autogen.sh && ./configure && \
    make && make install

ENTRYPOINT ./src/navcoid 