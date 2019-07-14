RUN npm install -g @vue/cli \
    && npm install -g @vue/cli-init \
    && chown $UNAME:$GID $HOME/ -R

