# Clate
VIM for C/C++ on Docker

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
2. Fill user_info.json
  - COMMON_PATH is directory to keep sharing files among **Clate** instances.
3. Execute install.py

# Console
* **Clate** console helps to manage projects.
  - create, show, remove project.
```
$ clate
Clate - 0.1
    [C]reate new project
    [L]ist projects
    [A]ctivate project
dele[T]e project
   s[E]lect version

   e[X]it
Command:
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
Command: l
{
    "common": {
        "Config": "[COMMON_PATH]/Config/",
        "Share": "[COMMON_PATH]/Share/",
        "Snippet": "[COMMON_PATH]/Snippet/"
    },
    "path": "[COMMON_PATH]/",
    "project": [
        {
            "directory": {
                "Base": "[COMMON_PATH]/Debug/",
                "Workspace": "[PROJECT_PATH]"
            },
            "name": "debug"
        },
        {
            "directory": {
                "Base": "[COMMON_PATH]/[PROJECT_NAME]/",
                "Workspace": "[PROJECT_PATH]"
            },
            "name": "test_clate"
        }
    ],
    "version": "0.1"
}
```
* Run project directly.
```
$ clate -p [PROJECT_NAME]
```

# Plugin
* kana/vim-operator-user
* skywind3000/asyncrun.vim
* tpope/vim-fugitive
* chrisbra/vim-diff-enhanced
* schickling/vim-bufonly
* mg979/vim-visual-multi
* justinhoward/fzf-neoyank
* mhinz/vim-signify
* jiangmiao/auto-pairs
* scrooloose/nerdcommenter
* t9md/vim-quickhl
* chrisbra/csv.vim
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
* vim-scripts/confirm-quit
* gabrielelana/vim-markdown
* ntpeters/vim-better-whitespace

# Usage

## Function key
* F1: This README.md
* F5: NERDTree
* F6: TagBar
* F7: Buffergator
* F8: Most Recently Used file list
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

