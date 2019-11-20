# Clate
FROM clate:base

RUN npm install -g yarn \
    && yarn global add eslint \
    && yarn global add @vue/cli \
    && yarn global add @vue/cli-init \
    && yarn global add create-nuxt-app \
    && chown $UNAME:$GID $HOME/ -R
