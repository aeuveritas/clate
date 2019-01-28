# Install dependencies
RUN apt-get install -y \
    cmake \
    ncurses-dev \
    zlib1g-dev \
    ninja-build \
    curl \
    xz-utils \
    python3-dev

# Build LLVM
RUN git clone https://git.llvm.org/git/llvm.git \
    && git clone https://git.llvm.org/git/clang.git llvm/tools/clang \
    && git clone https://git.llvm.org/git/lld.git llvm/tools/lld \
    && cd llvm && cmake -H. -BRelease -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DLLVM_TARGETS_TO_BUILD=X86 \
    && ninja -C Release install && cd .. \
    && cd llvm && cmake -H. -BRelease -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DLLVM_TARGETS_TO_BUILD=X86 -DLLVM_ENABLE_LLD=ON \
    && ninja -C Release install && cd .. \
# Build ccls
    && git clone --depth=1 --recursive https://github.com/MaskRay/ccls \
    && cd ccls \
    && cmake -H. -BRelease -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld -DCMAKE_PREFIX_PATH="$HOME/llvm/Release;$HOME/llvm/Release/tools/clang;$HOME/llvm;$HOME/llvm/tools/clang" \
    && ninja -C Release install && cd .. \
    && rm -rf ccls && rm -rf llvm

RUN mkdir -p /usr/local/clang/9.0.0 \
    && cp -a /usr/local/lib/clang/9.0.0/include/ /usr/local/clang/9.0.0/

