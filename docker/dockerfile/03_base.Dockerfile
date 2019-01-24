WORKDIR $HOME

# Install dependencies
RUN apt-get update

RUN apt-get install -y \
    build-essential \
    git \
    curl \
    wget

