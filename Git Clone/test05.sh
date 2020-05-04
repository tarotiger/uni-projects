#!/bin/dash 

# test05 for legit-commit -a option 
# by z5259931

export PATH="$PATH:."

legit-commit -a -m shouldnotwork
legit-init
touch a b c 
legit-add a b 
rm a
legit-commit -m commit-0
rm b 
legit-commit -a -m commit-1 
touch a b 
legit-commit -a -m shouldnotwork 
echo hello >b
legit-commit -a -m commit-2
legit-log 
