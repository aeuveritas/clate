# Clate
FROM clate:base

RUN pip3 install --upgrade pip

COPY artifact/settings.json $HOME
RUN chown $UID:$GID $HOME/settings.json

COPY artifact/framework /usr/local/bin/framework
RUN chmod 777 /usr/local/bin/framework

