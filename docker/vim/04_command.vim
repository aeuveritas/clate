"*****************************************************************************
"" Command
"*****************************************************************************
" Gtags
:command! Gctags    :AsyncRun gctags

" Refresh vim
:command! Refresh   :source ~/.config/nvim/init.vim

" Command for git grep
" - fzf#vim#grep(command, with_column, [options], [fullscreen])
command! -bang -nargs=* GGrep
    \ call fzf#vim#grep(
    \   'git grep --line-number '.shellescape(<q-args>), 0,
    \   { 'dir': systemlist('git rev-parse --show-toplevel')[0] }, <bang>0)

"*****************************************************************************
"" Key
"*****************************************************************************
let mapleader = ","

map <F5>                   :e<CR>
map <F6>                   :NERDTreeToggle<CR>
map <F7>                   :TagbarToggle<CR>
map <F8>                   :BuffergatorToggle<CR>

map <silent><F12>          :call quickmenu#toggle(0)<CR>

" Quickhl
nmap <leader>h             <Plug>(quickhl-manual-this)
nmap <leader>hh            <Plug>(quickhl-manual-clear)

" Quickfix
nnoremap <C-c>i            :ccl<CR>
nnoremap <C-c>p            :cn<CR>
nnoremap <C-c>o            :cp<CR>

" Buffer
nnoremap <C-c>l            :bn<CR>
nnoremap <C-c>k            :bp<CR>
nnoremap <C-c>j            :bd<CR>

" Git blame
vnoremap b                 :call AsyncBlame()<CR>

" Git grep
nnoremap <leader>s         :Ag <C-R>=expand("<cword>")<CR><CR>

" Gtags
nnoremap <leader>gd        :GtagsCursor<CR>
nnoremap <leader>gr        :Gtags -r <C-R>=expand("<cword>")<CR><CR>
nnoremap <leader>gs        :Gtags -s <C-R>=expand("<cword>")<CR><CR>

" Yank
nnoremap <leader>y         :FZFNeoyank<cr>
vnoremap <leader>y         :FZFNeoyankSelection<cr>

" Hide quit
cnoremap <silent> q<CR>    :call HideQuit()<CR>
cnoremap <silent> qa<CR>   :call HideQuit()<CR>
cnoremap <silent> qall<CR> :call HideQuit()<CR>
cnoremap <silent> q!<CR>   :call HideQuit()<CR>
cnoremap <silent> wqa<CR>  :wa<CR>
cnoremap <silent> wq<CR>   :wa<CR>

" Save with ctrl + s
nnoremap <C-s>             :w<CR>

" coc.nvim
"" Fix error
nmap <leader>f             <Plug>(coc-fix-current)

"" Remap keys for gotos
nmap <leader>d             <Plug>(coc-definition)
nmap <leader>t             <Plug>(coc-type-definition)
nmap <leader>i             <Plug>(coc-implementation)
nmap <leader>r             <Plug>(coc-references)

"" Remap for rename current word
nmap <leader>n             <Plug>(coc-rename)

" Strip white space
nmap <leader>w             :StripWhiteSapce<CR>


