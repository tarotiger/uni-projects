#!/bin/dash 

# test for legit-checkout 
# by z5259931

# tests include:
# checkout before init 
# check usage error 
# checkout before first commit 
# checkout to a non-existent branch
# checkout, delete file, then checkout again 
# commit in branch where file is deleted 
# checkout back to original branch and file should be restored 

export PATH="$PATH:."

legit-checkout 
legit-init
legit-checkout 
touch a b 
legit-add a b
legit-commit -m commit-0 
legit-branch usageerror
legit-branch b1 
rm b 
legit-checkout b1
legit-status 
legit-checkout master 
legit-status 
legit-checkout b1
legit-commit -a -m commit-1 
legit-status
legit-checkout master 
legit-status  
