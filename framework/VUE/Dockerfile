# Clate
FROM clate:base
MAINTAINER Karl.Jeong <aeuveritas@gmail.com>

RUN npm install -g @vue/cli \
    && npm install -g @vue/cli-init \
    && npm install -g json-server \
    && chown $UNAME:$GID $HOME/ -R
