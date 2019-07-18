# Clate
FROM clate:user
MAINTAINER Karl.Jeong <aeuveritas@gmail.com>

COPY artifact/generate_compile_commands.sh /usr/local/bin
RUN chmod 777 /usr/local/bin/generate_compile_commands.sh

COPY artifact/settings.json $HOME
RUN chown $UID:$GID $HOME/settings.json

COPY artifact/pre_run /usr/local/bin/pre_run
RUN chmod 777 /usr/local/bin/pre_run
ENTRYPOINT [ "/usr/local/bin/pre_run" ]

