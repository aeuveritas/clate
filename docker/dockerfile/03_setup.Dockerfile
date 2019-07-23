# Set scripts
COPY shell/bashrc $HOME/.bashrc

COPY shell/prepare /usr/local/bin
COPY shell/framework /usr/local/bin
COPY shell/run /usr/local/bin
COPY shell/loop /usr/local/bin
COPY shell/attach_shell /usr/local/bin

RUN chmod 777 /usr/local/bin/prepare
RUN chmod 777 /usr/local/bin/framework
RUN chmod 777 /usr/local/bin/loop
RUN chmod 777 /usr/local/bin/run
RUN chmod 777 /usr/local/bin/attach_shell

ENTRYPOINT [ "bash", "/usr/local/bin/run" ]
