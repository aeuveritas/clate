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
    linux-headers \
    libice \
    libsm \
    libxt \
    zlib-dev \
    isl-dev


