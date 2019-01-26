"*****************************************************************************
"" Quickmenu
"*****************************************************************************
" Clear all the items
call quickmenu#reset()

" Enable cursorline (:) and cmdline help (H)
let g:quickmenu_options = "HL"

call quickmenu#append("# Analysis", '')
call quickmenu#append("Diagnostics", 'CocList diagnostics', "diagnostics")

call quickmenu#append("# Gtags", '')
call quickmenu#append("Build tag", 'Gctags', "build tag")

call quickmenu#append("# Tab/Window/Buffer", '')
call quickmenu#append("Clear windows", 'call Clear()', "clear all windows and open last buffer")
call quickmenu#append("Clear rest of buffers", 'BufOnly', "clear rest of buffers")

call quickmenu#append("# File", '')
call quickmenu#append("List all files in current project", 'FZF', "list all files in current project")

call quickmenu#append("# Look", '')
call quickmenu#append("Indent line", 'IndentLinesToggle', "show indent line")
call quickmenu#append("Reset multi highlight", 'QuickhlManualReset', "Reset multi highlight")

call quickmenu#append("# Config", '')
call quickmenu#append("Refresh vimrc", 'Refresh', "refresh vimrc")

call quickmenu#append("# help", '')
call quickmenu#append("All commands", 'FzfCommands', "all commands")

"*****************************************************************************
"" Function
"*****************************************************************************
function! AsyncBlame() range
    execute 'AsyncRun git blame -L ' . a:firstline . ',' . a:lastline . ' %'
endfunction

function! Clear()
    execute 'on'
    execute 'blast'
    execute 'set number'
endfunction

"*****************************************************************************
"" Command
"*****************************************************************************
" Gtags
:command! Gctags    :AsyncRun gctags

" Source
:command! Refresh   :source ~/.config/nvim/init.vim

"*****************************************************************************
"" Key
"*****************************************************************************
let mapleader = ","

map <F1> :e ~/README.md<CR>
map <F5> :NERDTreeToggle<CR>
map <F6> :TagbarToggle<CR>
map <F7> :BuffergatorToggle<CR>

map <silent><F12> :call quickmenu#toggle(0)<CR>

" Quickhl
nmap <leader>h <Plug>(quickhl-manual-this)
nmap <leader>c <Plug>(quickhl-manual-clear)

" Quickfix
nnoremap <C-c>i     :ccl<CR>
nnoremap <C-c>p     :cn<CR>
nnoremap <C-c>o     :cp<CR>

" Buffer
nnoremap <C-c>l     :bn<CR>
nnoremap <C-c>k     :bp<CR>
nnoremap <C-c>j     :bd<CR>

" Git blame
vnoremap b          :call AsyncBlame()<CR>

" Gtags
nnoremap <leader>g  :GtagsCursor<CR>

" Yank
nnoremap <leader>y  :FZFNeoyank<cr>
nnoremap <ldeaer>r  :FZFNeoyankSelection<cr>

" Hide quit
cnoremap <silent> q<CR>            :echo 'Please, use clate console'<CR>
cnoremap <silent> qa<CR>           :echo 'Please, use clate console'<CR>
cnoremap <silent> wqa<CR>          :wa<CR>
cnoremap <silent> wq<CR>           :wa<CR>

" Stop clate
cnoremap <silent> stop_clate<CR>   :q<CR>


