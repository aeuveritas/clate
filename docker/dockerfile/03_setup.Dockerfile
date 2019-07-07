# Set scripts
COPY shell/bashrc $HOME/.bashrc
COPY shell/run /usr/local/bin
RUN chmod 777 /usr/local/bin/run
ENTRYPOINT [ "bash", "/usr/local/bin/run" ]
