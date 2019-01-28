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

" Use `:Format` for format current buffer
command! -nargs=0 Format :call CocAction('format')

" Use `:Fold` for fold current buffer
command! -nargs=? Fold :call     CocAction('fold', <f-args>)

"*****************************************************************************
"" Key
"*****************************************************************************
let mapleader = ","

map <F1> :e ~/README.md<CR>
map <F5> :e<CR>
map <F6> :NERDTreeToggle<CR>
map <F7> :TagbarToggle<CR>
map <F8> :BuffergatorToggle<CR>

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
nnoremap <leader>yy :FZFNeoyankSelection<cr>

" Hide quit
cnoremap <silent> q<CR>            :BuffergatorToggle<CR>
cnoremap <silent> qa<CR>           :BuffergatorToggle<CR>
cnoremap <silent> qall<CR>         :BuffergatorToggle<CR>
cnoremap <silent> q!<CR>           :BuffergatorToggle<CR>
cnoremap <silent> wqa<CR>          :wa<CR>
cnoremap <silent> wq<CR>           :wa<CR>

" Save with ctrl + s
nnoremap <C-s>      :w<CR>

" CCLS
"" Fix error
nmap <leader>f  <Plug>(coc-fix-current)

"" Remap keys for gotos
nmap <leader>d <Plug>(coc-definition)
nmap <leader>t <Plug>(coc-type-definition)
nmap <leader>i <Plug>(coc-implementation)
nmap <leader>r <Plug>(coc-references)

"" Remap for rename current word
nmap <leader>n <Plug>(coc-rename)

"" Use <cr> for confirm completion, `<C-g>u` means break undo chain at current position.
"" Coc only does snippet and additional edit on confirm.
inoremap <expr> <cr> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"

"" Remap for format selected region
vnoremap <leader>o  <Plug>(coc-format-selected)
