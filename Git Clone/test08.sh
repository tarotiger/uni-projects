#!/bin/dash 

# test for legit-branch 
# by z5259931

# test include:
# creating a branch before init
# creating a branch after init but before first commit 
# creating a branch called master 
# creating a branch with purely numeric characters 
# checking branch called master exists after first commit 
# deleting master branch 
# deleting a non existent branch 

export PATH="$PATH:."

legit-branch
legit-init
legit-branch 
touch a
legit-add a
legit-commit -m commit-0
legit-branch 
legit-branch master 
legit-branch 1
legit-branch b1 
legit-branch -d master 
legit-branch -d 1 
legit-branch -d b1 
legit-branch 
legit-commit -m commit-1
legit-branch 
