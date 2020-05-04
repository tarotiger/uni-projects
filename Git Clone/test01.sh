#!/bin/dash

# test01 for legit-add 
# by z5259931

# tests include: 
# adding multiple files including non existent files 
# adding removed files 

export PATH="$PATH:."

echo "legit-add"
legit-add
echo "legit-init"
legit-init
echo "legit-add" 
legit-add
echo "legit-add 'non-existent file'"
legit-add "non-existent file" 
echo "touch a"
touch a
echo "legit-add a"
legit-add a
echo "legit-add a"
legit-add a 
echo "touch b c d e"
touch b c d e 
echo "legit-add a b 'non-existent file'"
legit-add a b "non-existent file"
echo "legit-add c d e"
legit-add c d e 
echo "rm a"
rm a 
echo "legit-add a"
legit-add a 
