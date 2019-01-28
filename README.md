# Clate
VIM for C/C++ & Python on Docker

![clate](img/clate.png "clate")

# Installation
1. You can find your information with **id** linux command.
```
$ id [YOUR_ID]
```
  - If you use root account
```
$ id root
 uid=0(root) gid=0(root) groups=0(root),0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
```
2. Fill config.json
  - COMMON_PATH is directory to keep sharing files among **Clate** instances.
  - Set "true" for target language.
3. Execute install.py

# Console
* **Clate** console helps to manage projects.
  - create, show, remove project.
```
$ clate
[ INF ] Clate - 0.2
    [C]reate new project
    [L]ist projects
    [A]ctivate project
dele[T]e proect
chan[E] version

  st[O]p running project
  li[S]t running project

gene[R]ate compile_commands.json

   e[X]it
[ ASK ] command:
```
* Creates new project
```
Command: c
Project name: [PROJECT_NAME]
Project directory: [PROJECT_PATH]
Do you have additional directory? (y/N)
Created: {'directory': {'Base': u'[COMMON_PATH]/[PROJECT_NAME]/', 'Workspace': '[PROJECT_PATH]'}, 'name': '[PROJECT_NAME]'}
```
* Lists up all projects
```
[ ASK ] command: l
COMMON
{
    "default_version": "0.2",
    "directory": {
        "Config": "/home/xaliver/clate/Config/",
        "Path": "/home/xaliver/clate/",
        "Share": "/home/xaliver/clate/Share/",
        "Snippet": "/home/xaliver/clate/Snippet/"
    },
    "language": {
        "CPP": true,
        "JAVASCRIPT": false,
        "PYTHON": true
    }
}
PROJECT
[
    {
        "clang": {
            "directory": "CLATE/",
            "option": "-DCMAKE_BUILD_TYPE=Debug"
        },
        "directory": {
            "Temp": "/home/xaliver/clate/Temp/clate/",
            "Workspace": "/home/xaliver/Workspace/clate/"
        },
        "name": "clate",
        "version": "0.2"
    }
]

```
* Run project directly.
```
$ clate -a [PROJECT_NAME]
```

# Plugin
* neoclide/coc.nvim
* kana/vim-operator-user
* skywind3000/asyncrun.vim
* Shougo/denite.nvim
* tpope/vim-fugitive
* mhinz/vim-signify
* chrisbra/vim-diff-enhanced
* mg979/vim-visual-multi
* Shougo/neoyank.vim
* justinhoward/fzf-neoyank
* schickling/vim-bufonly
* jiangmiao/auto-pairs
* scrooloose/nerdcommenter
* bfrg/vim-cpp-modern
* vim-python/python-syntax
* t9md/vim-quickhl
* chrisbra/csv.vim
* ntpeters/vim-better-whitespace
* gabrielelana/vim-markdown
* scrooloose/nerdtree
* Xuyuanp/nerdtree-git-plugin
* jeetsukumaran/vim-buffergator
* majutsushi/tagbar
* skywind3000/quickmenu.vim
* dracula/vim
* vim-airline/vim-airline
* vim-airline/vim-airline-themes
* Yggdroot/indentLine
* junegunn/fzf
* junegunn/fzf.vim
* jesseleite/vim-agriculture
* SirVer/ultisnips
* honza/vim-snippets

# Usage

## Function key
* F1: This README.md
* F5: Refresh
* F6: NERDTree
* F7: TagBar
* F8: Buffergator
* F12: Quick menu

## Command
* FZF       : List all files in fzf window
```:FZF```
* AgRaw     : Grep [PATTERN] in current project
```:AgRaw -Q [PATTERN] [DIRECTORY]```

## Short-cut
* Next buffer               : &lt;C-c> l
* Prev buffer               : &lt;C-c> k
* Close buffer              : &lt;C-c> j

* Next quickfix             : &lt;C-c> p
* Prev quickfix             : &lt;C-c> o
* Close quickfix            : &lt;C-c> i

* &lt;leader>               : ,
* GtagsCursor               : &lt;leader> g
* Mark word highlight       : &lt;leader> h
* Clear word highlight      : &lt;leader> c
* List for yank             : &lt;leader> y

