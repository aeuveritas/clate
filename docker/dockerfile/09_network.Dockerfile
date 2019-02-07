# Set network
RUN apt install sshpass \
    && su -m - $UNAME -c 'ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa' \
    && ssh-keyscan -H $HOST >> $HOME/.ssh/known_hosts \
    && sshpass -p$PASSWORD ssh-copy-id -i $HOME/.ssh/id_rsa.pub -o StrictHostKeyChecking=no -f $UNAME@$HOST

ENV PASSWORD=""

