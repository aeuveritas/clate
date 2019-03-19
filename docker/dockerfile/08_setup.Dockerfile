# Set running environment
ENV TERM=xterm-256color

ENTRYPOINT ["bash", "/usr/local/bin/run"]

# Set running enviroment
COPY shell/bashrc $HOME/.bashrc
COPY shell/run /usr/local/bin
RUN chmod 777 /usr/local/bin/run
RUN echo "* hard nofile 773280" >> /etc/security/limits.conf \
    && echo "* soft nofile 773280" >> /etc/security/limits.conf

# Copy artifact
## GNU Global
COPY artifact/gnu-global/gctags /usr/local/bin

## MANUAL.md
COPY artifact/MANUAL.md $HOME

## Set GNU Global
RUN cp $TEMP/gtags.vim $PLUGIN/ \
    && cp $TEMP/gtags-cscope.vim $PLUGIN/

# Set GNU global working directory
RUN mkdir $HOME/.cache/tags_dir \
    && ln -s /Workspace $HOME/.cache/tags_dir

# Set vimrc
COPY vim/init.vim $HOME/.config/nvim/init.vim
RUN chown $UNAME:$GROUP $HOME -R \
    && su - $UNAME -c "nvim +qall"

