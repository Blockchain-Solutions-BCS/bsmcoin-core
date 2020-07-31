FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install -yq --no-install-recommends \
    build-essential \
    libcurl3-dev \
    libdb++-dev \
    libtool \ 
    autotools-dev \
    automake \
    pkg-config \
    libssl-dev \
    libevent-dev\
    bsdmainutils \
    libzmq3-dev\
    libqrencode-dev \
    qrencode \
    wget \
    curl \
    libboost-system-dev\
    libboost-filesystem-dev\
    libboost-chrono-dev \
    libboost-program-options-dev \
    libboost-test-dev \
    libboost-thread-dev \
    libminiupnpc-dev \
    ca-certificates	 \
    libunbound-dev \
    git \
    vim
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#--------------------------------------------------------------------------------
# NavBS Build + Install
#--------------------------------------------------------------------------------


WORKDIR /tmp
RUN git clone https://github.com/Blockchain-Solutions-BCS/navcoin-core.git

WORKDIR /tmp/navcoin-core
RUN ./autogen.sh
RUN ./configure  \
    --enable-hardening \
    --without-gui \
    --enable-upnp-default \
    ${CONFIGURE_FLAGS}
RUN make && make install

EXPOSE 8430
EXPOSE 8434
EXPOSE 8435
EXPOSE 8430/udp
EXPOSE 8434/udp
EXPOSE 8435/udp

WORKDIR /
RUN rm -fr /tmp/*

ENTRYPOINT ["/bin/bash", "-c"]