#!/bin/dash 

# test for legit-status 
# by z5259931  

# tests include: 
# add a file then make a change 
# add a file then delete it then rm 

export PATH="$PATH:."

legit-status 
legit-init
legit-status 
legit-status shouldnotwork
touch a b c 
legit-add a
legit-commit -m commit-0
# testing if status works normally 
legit-status 
legit-add b c
# testing for addition of b c to status 
legit-status 
echo change >b
# testing that b status remains unchanged
legit-status 
rm c
legit-rm c
# testing that c is now removed completely from status 
legit-status 
legit-commit -m commit-1 
# testing that c is no longer in the commit 
legit-status 
