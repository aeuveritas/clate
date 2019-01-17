"*****************************************************************************
"" Vim-PLug core
"*****************************************************************************
if has('vim_starting')
  set nocompatible               " Be iMproved
endif

let vimplug_exists=expand('~/.config/nvim/autoload/plug.vim')

let g:vim_bootstrap_langs = "cpp,python,c"
let g:vim_bootstrap_editor = "nvim"				" nvim or vim

if !filereadable(vimplug_exists)
  echo "Installing Vim-Plug..."
  echo ""
  silent !\curl -fLo ~/.config/nvim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  let g:not_finish_vimplug = "yes"

  autocmd VimEnter * PlugInstall
endif

" Required:
call plug#begin(expand('~/.config/nvim/plugged'))

"*****************************************************************************
"" Plug install packages
"*****************************************************************************
" Utility
Plug 'kana/vim-operator-user'
Plug 'ervandew/supertab'

" YouCompleteMe
Plug 'rdnetto/YCM-Generator', { 'branch': 'stable' }
Plug 'Valloric/YouCompleteMe', {
    \ 'dir': '~/.youcompleteme',
    \ 'do' : 'python3 ./install.py --clang-completer --system-libclang --system-boost --clang-tidy'
    \ }

" Async worker
Plug 'skywind3000/asyncrun.vim'

" Active function
Plug 'tpope/vim-fugitive'
Plug 'chrisbra/vim-diff-enhanced'
Plug 'schickling/vim-bufonly'
Plug 'mg979/vim-visual-multi'

" Passive function
Plug 'mhinz/vim-signify'
Plug 'jiangmiao/auto-pairs'
Plug 'scrooloose/nerdcommenter'

" Highlight
Plug 'octol/vim-cpp-enhanced-highlight', { 'for': 'cpp' }
Plug 'vim-python/python-syntax', { 'for': 'python' }
Plug 't9md/vim-quickhl'
Plug 'chrisbra/csv.vim', { 'for': 'csv' }

" Sidebar
Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
Plug 'Xuyuanp/nerdtree-git-plugin', { 'on': 'NERDTreeToggle' }
Plug 'jeetsukumaran/vim-buffergator', { 'on': 'BuffergatorToggle' }
Plug 'majutsushi/tagbar', { 'on': 'TagbarToggle' }
Plug 'skywind3000/quickmenu.vim'

" Look
Plug 'dracula/vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'Yggdroot/indentLine', { 'on': 'IndentLinesToggle' }
Plug 'yegappan/mru'

" Search
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'
Plug 'epmatsw/ag.vim'

" Snippets
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

" Interface
Plug 'vim-scripts/confirm-quit'

