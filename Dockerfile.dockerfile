FROM phusion/baseimage:0.11

ENV LANG=en_US.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get install -yq --no-install-recommends \
    git \
    autoconf \
    cmake \
    build-essential \
    libcurl3-dev \
    libdb++-dev \
    libtool \ 
    unbound \
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
    vim
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN whereis libunbound
#--------------------------------------------------------------------------------
# Build + install Berkeley DB
#--------------------------------------------------------------------------------
ARG BDB_URL=http://download.oracle.com/berkeley-db
ARG BDB_VER=db-4.8.30.NC
ARG BDB_PKG=${BDB_VER}.tar.gz
ARG BDB_CHK=12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef
ARG BDB_DIR=/usr/local/berkeley-db-4.8
ARG CONFIGURE_FLAGS

WORKDIR /tmp
RUN mkdir -p ${BDB_DIR}
RUN wget "${BDB_URL}/${BDB_PKG}" -q
RUN echo "${BDB_CHK}  ${BDB_PKG}" | sha256sum -c
RUN tar -xzf ${BDB_PKG}

WORKDIR /tmp/${BDB_VER}/build_unix/
RUN ../dist/configure --enable-cxx \
    --disable-shared \
    --with-pic \
    --prefix=$BDB_DIR
RUN make install
#--------------------------------------------------------------------------------
# BsmBS Build + Install
#--------------------------------------------------------------------------------
WORKDIR /tmp
RUN git clone https://github.com/Blockchain-Solutions-BCS/bsmcoin-core.git

WORKDIR /tmp/bsmcoin-core/
RUN ./autogen.sh
RUN ./configure LDFLAGS="-L${BDB_DIR}/lib/" \
    CPPFLAGS="-I${BDB_DIR}/include/" \
    --enable-hardening \
    --without-gui \
    --enable-upnp-default
RUN make && make install

EXPOSE 8430
EXPOSE 8434
EXPOSE 8435
EXPOSE 8430/udp
EXPOSE 8434/udp
EXPOSE 8435/udp

WORKDIR /tmp/bsmcoin-core/src
RUN ./bsmcoind -port=8430 -rpcport=8434 -debug=rpc -dns=0 -dnsseed=0

ENTRYPOINT ["/bin/bash"]