# Environment for NeoVim
ENV TEMP=$HOME/TEMP \
    PLUGIN=$HOME/.config/nvim/plugin \
    AUTOLOAD=$HOME/.config/nvim/autoload

RUN mkdir -p $TEMP \
    && mkdir -p $PLUGIN \
    && chown $UNAME:$GROUP $HOME -R

#Install NeoVim
RUN apk add --update --no-cache \
    libx11-dev \
    libxpm-dev \
    libxt-dev \
    python3 \
    python3-dev \
    nodejs \
    npm \
    gperf \
    texinfo \
    lua-dev \
    py3-pip \
    luarocks \
    diffutils \
    boost-dev \
    the_silver_searcher \
    yarn

RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
RUN apk add --update --no-cache neovim==0.3.1-r1 neovim-doc==0.3.1-r1 neovim-lang==0.3.1-r1


