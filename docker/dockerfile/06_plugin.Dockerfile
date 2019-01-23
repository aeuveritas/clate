# Install Vim-Plug
RUN su - $UNAME -c "curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"

# Install plugins for NeoVim
COPY vim/init_init.vim $HOME/.config/nvim/init.vim
RUN chown $UNAME:$GROUP $HOME -R \
    && su - $UNAME -c "nvim +PlugInstall +qall"

# Link fzf
RUN ln -s /home/$UNAME/.fzf/bin/fzf /usr/local/bin/fzf


