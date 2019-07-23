# Set network
RUN su -m - $UNAME -c 'ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa' \
    && ssh-keyscan -H $HOST >> $HOME/.ssh/known_hosts \
    && sshpass -p$PASSWORD ssh-copy-id -i $HOME/.ssh/id_rsa.pub -o StrictHostKeyChecking=no -f $UNAME@$HOST

RUN echo "$UNAME:$PASSWORD" | chpasswd

RUN mkdir -p $HOME/.ssh \
    && chown $UID:$GID $HOME/ \
    && chmod 700 $HOME/.ssh
COPY ssh_key/id_rsa.pub $HOME
RUN cat $HOME/id_rsa.pub >> $HOME/.ssh/authorized_keys \
    && chown $UID:$GID $HOME/ -R \
    && chmod 600 $HOME/.ssh/authorized_keys

ENV PASSWORD=""

