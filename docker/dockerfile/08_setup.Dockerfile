# Set running environment
ENV TERM=xterm-256color

ENTRYPOINT ["bash", "/usr/local/bin/run"]

# Set running enviroment
COPY shell/bashrc $HOME/.bashrc
COPY shell/run /usr/local/bin
RUN chmod 777 /usr/local/bin/run

# Set post nvim plugin
COPY vim/init_proc.vim $HOME/.config/nvim/init.vim
RUN chown $UNAME:$GROUP $HOME -R \
    && su - $UNAME -c "nvim +PlugInstall +qall"

# Copy artifact
## GNU Global
COPY artifact/gnu-global/gctags /usr/local/bin

## README.ME
COPY artifact/README.md $HOME

## Set GNU Global
RUN cp $TEMP/gtags.vim $PLUGIN/ \
    && cp $TEMP/gtags-cscope.vim $PLUGIN/

# Set vimrc
COPY vim/init.vim $HOME/.config/nvim/init.vim
RUN chown $UNAME:$GROUP $HOME -R \
    && su - $UNAME -c "nvim +PlugInstall +qall"

