# Install Vim-Plug
RUN su - $UNAME -c "curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"

# Install yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y yarn

# Install plugins for NeoVim
COPY vim/init_init.vim $HOME/.config/nvim/init.vim
RUN chown $UNAME:$GROUP $HOME -R \
    && su - $UNAME -c "nvim +PlugInstall +qall"

# Link fzf
RUN ln -s /home/$UNAME/.fzf/bin/fzf /usr/local/bin/fzf


