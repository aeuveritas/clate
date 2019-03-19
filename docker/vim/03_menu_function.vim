"*****************************************************************************
"" Quickmenu
"*****************************************************************************
" Clear all the items
call quickmenu#reset()

" Enable cursorline (:) and cmdline help (H)
let g:quickmenu_options = "HL"

call quickmenu#append("# Tags", '')
call quickmenu#append("Generate compile_commands.json", 'call AsyncCMake()', "generate compile_commands")
call quickmenu#append("Generate tag", 'Gctags', "generate tag")

call quickmenu#append("# Analysis", '')
call quickmenu#append("Diagnostics", 'CocList diagnostics', "diagnostics")

call quickmenu#append("# Build/Run", '')
call quickmenu#append("Build", 'call AsyncBuild()', "build project")
call quickmenu#append("Run", 'call AsyncRunBinary()', "run project")

call quickmenu#append("# Tab/Window/Buffer", '')
call quickmenu#append("Clear rest of buffers", 'BufOnly', "clear rest of buffers")

call quickmenu#append("# Look", '')
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

function! HideQuit()
    let nr_bufs = len(filter(range(1, bufnr('$')), 'buflisted(v:val)'))
    echo nr_bufs
    if nr_bufs == 1
        echo 'this is the last buffer.'
    else
        execute 'bd'
    endif
endfunction

function! AsyncCMake()
    execute 'AsyncRun ' . $CMAKE_CMD
endfunction

function! AsyncBuild()
    execute 'AsyncRun ' . $BUILD_CMD
endfunction

function! AsyncRunBinary()
    execute 'AsyncRun ' . $RUN_CMD
endfunction

