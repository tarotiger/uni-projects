#!/bin/dash

# test02 for legit-commit 
# by z5259931

export PATH="$PATH:."

# attempts to commit a file that has been removed from the working directory 
echo "legit-commit -m 'should not commit'"
legit-commit -m "should not commit"
echo "legit-init"
legit-init
echo "echo 1 >a"
echo 1 >a
echo "legit-add a"
legit-add a
echo "rm a"
rm a 
echo "legit-add a"
legit-add a 
echo "legit-commit -m message1"
legit-commit -m message1
echo "touch a"
touch a
echo "legit-commit -m message1"
legit-commit -m message1
echo "legit-add a"
legit-add a
echo "legit-commit -m message2"
legit-commit -m message1
