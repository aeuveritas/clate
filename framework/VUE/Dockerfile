# Clate
FROM clate:base
MAINTAINER Karl.Jeong <aeuveritas@gmail.com>

RUN npm install -g yarn \
    && yarn global add @vue/cli \
    && yarn global add @vue/cli-init \
    && chown $UNAME:$GID $HOME/ -R
