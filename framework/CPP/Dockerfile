# Clate
FROM clate:base

COPY artifact/generate_compile_commands.sh /usr/local/bin
RUN chmod 777 /usr/local/bin/generate_compile_commands.sh

COPY artifact/settings.json $HOME
RUN chown $UID:$GID $HOME/settings.json

COPY artifact/framework /usr/local/bin/framework
RUN chmod 777 /usr/local/bin/framework

