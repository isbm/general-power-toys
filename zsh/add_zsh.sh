#!/usr/bin/sh

sudo apt install zsh curl git -y
sudo chsh $(whoami) -s /usr/bin/zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions
curl https://raw.githubusercontent.com/isbm/bobtheshell/master/bobtheshell.zsh-theme -o ~/.oh-my-zsh/themes/bobtheshell.zsh-theme

cat >> ~/.zshrc <<EOF
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="bobtheshell"
ENABLE_CORRECTION="true"
COMPLETION_WAITING_DOTS="true"

plugins=(git zsh-autosuggestions zsh-completions last-working-dir wd)
autoload -U compinit && compinit
source $ZSH/oh-my-zsh.sh

export EDITOR=emacs-nox
EOF
