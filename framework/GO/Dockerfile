# Clate
FROM clate:base

COPY artifact/settings.json $HOME
COPY artifact/launch.json $HOME
RUN chown $UID:$GID $HOME/*

COPY artifact/framework /usr/local/bin/framework
RUN chmod 777 /usr/local/bin/framework

RUN wget https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.14.2.linux-amd64.tar.gz && \
    rm go1.14.2.linux-amd64.tar.gz

ENV PATH /usr/local/go/bin:$PATH
ENV PATH /Workspace/bin/:$PATH

RUN echo "PATH=\"$PATH\"" > /etc/environment

RUN mkdir /GOPATH
RUN go env -w GOPATH=/GOPATH

