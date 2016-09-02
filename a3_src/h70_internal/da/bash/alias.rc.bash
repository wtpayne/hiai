# ---
# type:
#     bash_script
#
# copyright:
#     "Copyright 2015 High Integrity Artificial Intelligence Systems"
#
# license:
#     "Licensed under the Apache License, Version 2.0 (the License);
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an AS IS BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License."
# ...

if [ "$USER" = "root"  ]; then
	sucmd=''
else
	sucmd='sudo'
fi


# -----------------------------------------------------------------------------
# Clear screen
# ============
#
alias clc='clear'
alias cls='clear'


# -----------------------------------------------------------------------------
# Directory listings
# ==================
#
alias ls='\ls  -CFh   --color=auto --sort=extension'
alias la='\ls  -CFAh  --color=auto --sort=extension'
alias l='\ls   -CFAlh --color=auto --sort=extension --group-directories-first'
alias lal='\ls -CFAlh --color=auto --sort=extension --group-directories-first'

alias dir='\dir   --color=auto'
alias vdir='\vdir --color=auto'


# -----------------------------------------------------------------------------
# Navigation
# ==========
#
alias ..='cd ..'
alias ...='cd ../..'
alias cd..='cd ..'
alias cd...='cd ../..'


# -----------------------------------------------------------------------------
# Search
# ======
#
unalias grep 2>/dev/null
alias llgrep='\grep     --color=never -E'
alias   grep='\grep  -n --color=auto'
alias  fgrep='\fgrep    --color=auto'
alias  egrep='\egrep    --color=auto'
alias f='find . | grep'


# -----------------------------------------------------------------------------
# Move, Copy, Delete
# ==================
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'


# -----------------------------------------------------------------------------
# Git
# ===
#
alias g='git'
alias gd='git-diff'
alias gf='git fetch'
alias gl="git log --all --decorate --oneline --graph -n30"
alias gp='git pull'
alias gr='git-reflog'
alias gs='git status'
alias glf='git-ls-files'
alias gpom='git push origin master:refs/for/master'


# -----------------------------------------------------------------------------
# Make
# ====
#
alias make='clear && make'
alias m='make'


# -----------------------------------------------------------------------------
# Anger Management
# ================
#
alias FFS='sudo'
alias JUSTFUCKING='sudo'


# -----------------------------------------------------------------------------
# Misc
# ====
#
alias rebash='source ~/.bashrc'
alias less='less -r'
alias explore='nautilus'

alias godev='cd ~/dev/hiai/b0_dev'
alias gosrc='cd ~/dev/hiai/b0_dev/a3_src'

# alias gotmux='cd ~/dev/algo/work/master/source/ && ./tmux.sh'
# alias gobuild='cd ~/dev/algo/work/master/source/ && ./build.sh quick'
# alias build='cd ~/dev/algo/work/master/source/ && ./build.sh'
# alias svim='sudo vim'
# alias back='cd $OLDPWD'
# alias root='sudo su'
# alias runlevel='sudo /sbin/init'
# alias grep='grep --color=auto'
# alias dfh='df -h'
# alias gvim='gvim -geom 84x26'
# alias start='dbus-launch startx'
# alias da='./da'
# alias pms='sudo pm-suspend'
# alias se='sudo gvim'
# alias e='gvim'
# alias smi='sudo make install'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
