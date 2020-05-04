#!/bin/dash

# test04 for legit-show
# by z5259931

# tests include:
# legit-show before any commits 
# legit-show non-existent files 
# legit-show invalid input 

export PATH="$PATH:."

legit-show
legit-init
legit-show 
echo hello >a
legit-add a 
legit-commit -m commit-1
legit-show 1:a
legit-show thisshouldgiveerror
legit-show 0:a 
echo world >>a
legit-add a 
legit-show :a 
legit-commit -m commit-2
legit-show :a
legit-show 1:a
