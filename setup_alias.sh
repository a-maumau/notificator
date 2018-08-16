#!/bin/bash
set -Ceu

INS_DIR="$HOME"/.scripts
INS_SCRIPT="notify.py"
RC_FILE=0

# find default shell rc file of major shells
if [[ $(echo $SHELL | grep bash) ]]; then
    RC_FILE=$HOME/.bashrc
elif [[ $(echo $SHELL | grep zsh) ]]; then
    RC_FILE=$HOME/.zshrc
elif [[ $(echo $SHELL | grep csh) ]]; then
    RC_FILE=$HOME/.cshrc
elif [[ $(echo $SHELL | grep ksh) ]]; then
    RC_FILE=$HOME/.kshrc
elif [[ $(echo $SHELL | grep tcsh) ]]; then
    RC_FILE=$HOME/.tcshrc
elif [[ $(echo $SHELL | grep ash) ]]; then
    RC_FILE=$HOME/.ashrc
elif [[ $(echo $SHELL | grep sh) ]]; then
    RC_FILE=$HOME/.profile
else
	echo "Non-standard shell $SHELL detected. sorry"
	echo "See the source and setup by yourself XD"
fi

if [ -f "$RC_FILE" ]; then
	mkdir -p "$INS_DIR"
	cp "$RC_FILE" "$RC_FILE".notify.back
	cp ./"$INS_SCRIPT" "$INS_DIR"/
	chmod 755 "$INS_DIR"/"$INS_SCRIPT"

	# please use ">>" not ">"
	echo ""                                           >> "$RC_FILE"
	echo "# notify"                                   >> "$RC_FILE"
	echo "alias notify='python $INS_DIR/$INS_SCRIPT'" >> "$RC_FILE"

	source "$RC_FILE"
fi