#!/bin/dash 

# test00 for initialising legit repository 
# by z5259931

# tests include:
# testing usage 
# creating init repo when already existing 

export PATH="$PATH:."

legit-init 
legit-init "this shouldn't work" 
legit-init 
