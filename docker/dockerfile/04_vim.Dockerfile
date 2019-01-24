# Environment for NeoVim
ENV TEMP=$HOME/TEMP \
    PLUGIN=$HOME/.config/nvim/plugin \
    AUTOLOAD=$HOME/.config/nvim/autoload

RUN mkdir -p $TEMP \
    && mkdir -p $PLUGIN \
    && chown $UNAME:$GROUP $HOME -R

#Install NeoVim
RUN apt-get install -y \
    python3-dev \
    nodejs \
    npm \
    python3-pip \
    diffutils \
    libboost-all-dev \
    silversearcher-ag

RUN apt-get install -y software-properties-common \
    && add-apt-repository ppa:neovim-ppa/stable \
    && apt-get update \
    && apt-get install -y neovim


