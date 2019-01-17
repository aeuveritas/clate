# Clate
FROM alpine:latest
MAINTAINER Karl.Jeong <aeuveritas@gmail.com>


# User info
ENV UID="1000" \
    UNAME="xaliver" \
    GID="1000" \
    GNAME="xaliver" \
    SHELL="/bin/bash" \
    HOME=/home/xaliver


    # User
RUN apk --no-cache add sudo \
    # Create home dir
    && mkdir -p "${HOME}" \
    && chown "${UID}":"${GID}" "${HOME}" \
    # Create user
    && echo "${UNAME}:x:${UID}:${GID}:${UNAME},,,:${HOME}:${SHELL}" \
    >> /etc/passwd \
    && echo "${UNAME}::17032:0:99999:7:::" \
    >> /etc/shadow \
    # No password sudo
    && echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" \
    > "/etc/sudoers.d/${UNAME}" \
    && chmod 0440 "/etc/sudoers.d/${UNAME}" \
    # Create group
    && echo "${GNAME}:x:${GID}:${UNAME}" \
    >> /etc/group

WORKDIR $HOME

# Install dependencies
RUN apk add --update --no-cache \
    bash \
    build-base \
    git \
    make \
    bison \
    flex \
    ncurses-dev \
    ncurses-libs \
    ncurses-terminfo \
    libtool \
    curl \
    mpfr-dev \
    mpc1-dev \
    autoconf \
    automake \
    isl-dev


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
    cmake \
    linux-headers \
    lua-dev \
    perl-dev \
    py3-pip \
    xz \
    luarocks \
    diffutils \
    libice \
    libsm
RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
RUN apk add --update --no-cache neovim==0.3.1-r1 neovim-doc==0.3.1-r1 neovim-lang==0.3.1-r1

# Install neovim python support
RUN pip3 install pynvim pep8 clang

RUN npm install -g neovim

# Environment for NeoVim
ENV PLUGIN=$HOME/.config/nvim/plugin \
    AUTOLOAD=$HOME/.config/nvim/autoload

RUN mkdir -p $PLUGIN \
    && chown $UNAME:$GROUP $HOME -R

# Environment
ENV GLOBAL_VERSION=6.6.2

# Build Ctags
RUN git clone https://github.com/universal-ctags/ctags.git \
    && cd ctags \
    && ./autogen.sh \
    && ./configure \
    && make -j $(nproc) && make install-strip \
    && cd .. \
    && rm -rf ctags

# Build GNU Global
RUN wget https://ftp.gnu.org/pub/gnu/global/global-${GLOBAL_VERSION}.tar.gz \
    && tar xvzf global-${GLOBAL_VERSION}.tar.gz \
    && cd global-${GLOBAL_VERSION} \
    && rm -rf ./libltdl \
    && sh reconf.sh \
    && ./configure --with-universal-ctags=/usr/local/bin/ctags \
    && make -j $(nproc) && make install-strip \
    && cp gtags.vim $PLUGIN \
    && cp gtags-cscope.vim $PLUGIN \
    && cp gtags.conf $HOME/.globalrc \
    && cd .. \
    && rm -rf global-${GLOBAL_VERSION}.tar.gz global-${GLOBAL_VERSION}

# Vim plugins deps
RUN apk add --update --no-cache \
    libxt \
    build-base \
    cmake \
    python-dev \
    the_silver_searcher \
    #cargo \
    boost-dev

#RUN cargo install fd-find

# Create temp directories
RUN mkdir -p \
    /ext \
    $HOME/.vim_runtime/temp_dirs \
    && chown $UNAME:$GROUP $HOME -R

# Install Vim-Plug
RUN su - $UNAME -c "curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"

# Install plugins for NeoVim
COPY vim/init_init.vim $HOME/.config/nvim/init.vim
RUN chown $UNAME:$GROUP $HOME -R \
    && su - $UNAME -c "nvim +PlugInstall +qall"

# Cleanup
RUN rm -rf \
    /usr/lib/go \
    /var/log/* \
    /var/tmp/* \
    && mkdir -p /var/cache/apk

ENV TERM=xterm-256color

ENTRYPOINT ["bash", "/usr/local/bin/run"]

# Copy artifact
## YouCompleteMe
COPY artifact/youcompleteme/ycm_extra_conf.py $HOME

## GNU Global
COPY artifact/gnu-global/gctags /usr/local/bin

# Set running enviroment
COPY shell/bashrc $HOME/.bashrc
COPY shell/run /usr/local/bin
RUN chmod 777 /usr/local/bin/run

# Set vimrc
COPY vim/init_proc.vim $HOME/.config/nvim/init.vim
RUN chown $UNAME:$GROUP $HOME -R \
    && su - $UNAME -c "nvim +PlugInstall +qall"

COPY vim/init.vim $HOME/.config/nvim/init.vim
COPY artifact/README.md $HOME

RUN chown $UNAME:$GROUP $HOME -R

