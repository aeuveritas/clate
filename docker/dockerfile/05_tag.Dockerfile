# Install dependencies
RUN apt-get install -y \
    autoconf \
    bison \
    flex \
    gperf \
    libtool-bin \
    texinfo \
    ncurses-dev

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
    && cp gtags.vim $TEMP \
    && cp gtags-cscope.vim $TEMP \
    && cp gtags.conf $HOME/.globalrc \
    && cd .. \
    && rm -rf global-${GLOBAL_VERSION}.tar.gz global-${GLOBAL_VERSION}

