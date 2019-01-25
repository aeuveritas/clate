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
" LSP
Plug 'neoclide/coc.nvim', { 'tag': '*', 'do': 'yarn install' }

" Utility
Plug 'kana/vim-operator-user'

" Async worker
Plug 'skywind3000/asyncrun.vim'
Plug 'Shougo/denite.nvim', { 'do': ':UpdateRemotePlugins' }

" Git
Plug 'tpope/vim-fugitive'
Plug 'mhinz/vim-signify'
Plug 'chrisbra/vim-diff-enhanced'

" Edit
Plug 'mg979/vim-visual-multi'
Plug 'Shougo/neoyank.vim'
Plug 'justinhoward/fzf-neoyank'

" Tab/Window/Buffer
Plug 'schickling/vim-bufonly'

" Auto fill
Plug 'jiangmiao/auto-pairs'
Plug 'scrooloose/nerdcommenter'

" Highlight
Plug 'bfrg/vim-cpp-modern'
Plug 'vim-python/python-syntax', { 'for': 'python' }
Plug 't9md/vim-quickhl'
Plug 'chrisbra/csv.vim', { 'for': 'csv' }
Plug 'ntpeters/vim-better-whitespace'
Plug 'gabrielelana/vim-markdown', { 'for': 'markdown' }

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

" Search
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'
Plug 'jesseleite/vim-agriculture'

" Snippets
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

" Interface
Plug 'vim-scripts/confirm-quit'

