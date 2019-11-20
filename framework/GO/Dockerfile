# Clate
FROM clate:base

COPY artifact/settings.json $HOME
RUN chown $UID:$GID $HOME/settings.json

COPY artifact/framework /usr/local/bin/framework
RUN chmod 777 /usr/local/bin/framework

RUN wget https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.13.3.linux-amd64.tar.gz && \
    rm go1.13.3.linux-amd64.tar.gz

ENV PATH /usr/local/go/bin:$PATH
RUN echo "PATH=\"$PATH\"" > /etc/environment
