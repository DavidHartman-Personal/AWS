# Bash/Shell AWS CLI scripts

## bash-my-aws

git clone https://github.com/bash-my-aws/bash-my-aws.git bash-my-aws

export PATH="$PATH:$HOME/.bash-my-aws/bin"
source ~/.bash-my-aws/aliases

# For ZSH users, uncomment the following two lines:
# autoload -U +X compinit && compinit
# autoload -U +X bashcompinit && bashcompinit

source ~/.bash-my-aws/bash_completion.sh


# bash users may source the functions instead of loading the aliases
if [ -d ${HOME}/.bash-my-aws ]; then
  for f in ~/.bash-my-aws/lib/*-functions; do source $f; done
fi


