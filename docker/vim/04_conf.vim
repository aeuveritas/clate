"*****************************************************************************
"" Vim core
"*****************************************************************************
set hidden

set number

" Turn on the Wild menu
set wildmenu

" Ignore compiled files
set wildignore=*.o,*~,*.pyc
if has("win16") || has("win32")
    set wildignore+=.git\*,.hg\*,.svn\*
else
    set wildignore+=*/.git/*,*/.hg/*,*/.svn/*,*/.DS_Store
endif

" Enable mouse
"set mouse=a

" Always show current position
set ruler

" Height of the command bar
set cmdheight=1

" When searching try to be smart about cases
set smartcase

" Highlight search results
set hlsearch

" Makes search act like search in modern browsers
set incsearch

" Show matching brackets when text indicator is over them
set showmatch

" Sets how many lines of history VIM has to remember
set history=500

" Don't redraw while executing macros (good performance config)
set lazyredraw

" For regular expressions turn magic on
set magic

" Underline for cursor
set cursorline
"augroup BgHighlight
"    autocmd!
"    autocmd WinEnter * set cursorline
"    autocmd WinEnter * set nocursorline
"augroup END

"*****************************************************************************
"" Text, tab and indent related
"*****************************************************************************
" Use spaces instead of tabs
set expandtab

" Be smart when using tabs ;)
set smarttab

" 1 tab == 4 spaces
set shiftwidth=4
set tabstop=4

" Linebreak on 500 characters
set lbr
set tw=500

set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines

" prefer vertical orientation when using :diffsplit
set diffopt+=vertical

"*****************************************************************************
"" VIM user interface
"*****************************************************************************
" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

"*****************************************************************************
"" Colors and Fonts
"*****************************************************************************
" Enable syntax highlighting
syntax enable

" Enable 256 colors palette in Gnome Terminal
if $COLORTERM == 'gnome-terminal'
    set t_Co=256
endif

" Enable dracula theme
color dracula

" Set extra options when running in GUI mode
if has("gui_running")
    set guioptions-=T
    set guioptions-=e
    set t_Co=256
    set guitablabel=%M\ %t
endif

" Set utf8 as standard encoding and en_US as the standard language
set encoding=utf8

" Use Unix as the standard file type
set ffs=unix,dos,mac

"*****************************************************************************
"" coc.nvim
"*****************************************************************************
set completeopt-=preview
highlight Pmenu ctermfg=0 ctermbg=7 guifg=#ffffff guibg=#000000

"*****************************************************************************
"" Status line
"*****************************************************************************
" Always show the status line
set laststatus=2

"*****************************************************************************
"" Helper functions
"*****************************************************************************
" Returns true if paste mode is enabled
function! HasPaste()
    if &paste
        return 'PASTE MODE  '
    endif
    return ''
endfunction

"*****************************************************************************
"" Airline
"*****************************************************************************
let g:airline#extensions#tabline#enabled = 1                " Enable buffer list
let g:airline#extensions#tabline#buffer_nr_show = 1         " Show buffer number
let g:airline#extensions#tabline#buffer_nr_format = '%s:'   " Buffer number format

let g:airline_theme = 'wombat'

let g:asyncrun_status = 'idle'
let g:airline_section_error = airline#section#create_right(['%{g:asyncrun_status}'])

"*****************************************************************************
"" Asyncrun
"*****************************************************************************
let g:asyncrun_open = 6

"*****************************************************************************
"" Ultisnips
"*****************************************************************************
" Trigger configuration. Do no use <tab> if you use
" https://github.com/Valloric/YouCompleteMe
let g:UltiSnipsExpandTrigger = "<tab>"
let g:UltiSnipsJumpForwardTriggers = "<tab>"
let g:UltiSnipsJumpBackwardTrigger = "<s-tab>"

" If you want :UltiSnipsEdit to split your window.
let g:UltiSnipsEditSplit = "vertical"

let g:UltiSnipsSnippetDirectories = ['/Snippet/UltiSnips']

"*****************************************************************************
"" GNU Global
"*****************************************************************************
let g:GtagsCscope_Auto_Load = 1                             " Autoload GtagsCscope

"*****************************************************************************
"" Rtags
"*****************************************************************************
"let g:rtagsUseLocationList = 0

"*****************************************************************************
"" NERDTree
"*****************************************************************************
let g:NERDTreeIndicatorMapCustom = {
    \ "Modified"  : "M",
    \ "Staged"    : "S",
    \ "Untracked" : "t",
    \ "Renamed"   : "N",
    \ "Unmerged"  : "m",
    \ "Deleted"   : "R",
    \ "Dirty"     : "D",
    \ "Clean"     : "C",
    \ 'Ignored'   : 'I',
    \ "Unknown"   : "k"
    \ }

"*****************************************************************************
"" Tagbar
"*****************************************************************************
"let g:tagbar_left = 1

"*****************************************************************************
"" Buffergator
"*****************************************************************************
let g:buffergator_autoupdate = 1
let g:buffergator_mru_cycle_loop = 1
let g:buffergator_viewport_split_policy = "T"

"*****************************************************************************
"" Fzf
"*****************************************************************************
let g:fzf_command_prefix = 'Fzf'
let $FZF_DEFAULT_COMMAND = 'find * -type f'

"*****************************************************************************
"" Bufonly
"*****************************************************************************

"*****************************************************************************
"" Indentline
"*****************************************************************************
let g:indentLine_char = ':'
let g:indentLine_setColors = 0

"*****************************************************************************
"" Quickhl
"*****************************************************************************

"*****************************************************************************
"" Diff-enhanced
"*****************************************************************************
" started in Diff-Mode set diffexpr (plugin not loaded yet)
if &diff
    let &diffexpr='EnhancedDiff#Diff("git diff",
        "--diff-algorithm=histogram")'
    endif

"*****************************************************************************
"" NERDCommenter
"*****************************************************************************
filetype plugin on

" Add spaces after comment delimiters by default
let g:NERDSpaceDelims = 1
" Allow commenting and inverting empty lines (useful when commenting a region)
let g:NERDCommentEmptyLines = 1
" Enable trimming of trailing whitespace when uncommenting
let g:NERDTrimTrailingWhitespace = 1
" Enable NERDCommenterToggle to check all selected lines is commented or not
let g:NERDToggleCheckAllLines = 1
let g:clang_format#auto_format_on_insert_leave = 1

"*****************************************************************************
"" Scratch
"*****************************************************************************

"*****************************************************************************
"" Python highlight
"*****************************************************************************
let g:python_highlight_all = 1
let g:python_version_2 = 1

"*****************************************************************************
"" Markdown
"*****************************************************************************
let g:markdown_include_jekyll_support = 0
let g:markdown_enable_mappings = 0
let g:markdown_enable_spell_checking = 0
let g:markdown_enable_input_abbreviations = 0

let g:markdown_enable_conceal = 1

"*****************************************************************************
"" Better whitespace
"*****************************************************************************
let g:better_whitespace_enabled = 1

"*****************************************************************************
"" Start up
"*****************************************************************************
"autocmd VimEnter * NERDTree
"autocmd VimEnter * Tagbar
"autocmd VimEnter * 2wincmd w

