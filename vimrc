set encoding=utf-8 fileencodings=ucs-bom,utf-8,cp936,gbk,gb2312
syntax on

set nu


set mouse=a
set mouse=nv
"将所有鼠标选择的文本放在未命名寄存器中和剪切板寄存器中
set clipboard=unnamed

set selection=exclusive
set selectmode=mouse,key

set backspace=2

filetype on
filetype plugin on

filetype indent on


set hlsearch

set incsearch

set ambiwidth=double

set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent
set expandtab
"显示括号匹配
set showmatch
"括号匹配显示时间为1(单位是十分之一秒)
set matchtime=1


"增强模式中的命令行自动完成操作
set wildmenu
"不要生成swap文件，当buffer被丢弃的时候隐藏它
setlocal noswapfile
set bufhidden=hide

set nowrap         " 不自动换行
set wrap           " 自动换行
set linebreak      " 整词换行
set whichwrap=b,s,<,>,[,]       " 光标从行首和行末时可以跳到另一行去

"add robot supporting to vim to highlight keywords
"git clone git://github.com/mfukar/robotframework-vim.git
"mkdir ~/.vim/
"cd robotframework-vim && cp -R * ~/.vim/
"

