#!/bin/dash

# test06 for legit-rm 
# by z5259931

# tests include:
# call legit-rm before init
# call legit-rm before commits 
# call legit with a unknown -- command 
# call legit-rm after commit 
# modifying a file, adding it, modifying it again and remove from index 
# modifying a file, adding it, modifying it again then call legit-rm  
# modifying a file, adding it, deleting file from wd then call legit-rm 

export PATH="$PATH:."

legit-rm 
legit-init
legit-rm 
touch a b c d
legit-add a b c d
legit-commit -m commit-0
# test for usage error 
legit-rm 
legit-rm d
# test should not allow rm 
legit-rm --cached d 
# test for usage error 
legit-rm --unknowncommand d 
legit-add d 
echo hello >a
legit-add a 
echo world >>a 
# test for error message
legit-rm --cached a 
echo chicken >b
legit-add b
echo bin >>b
# test for error message 
legit-rm b
echo legit >c
legit-add c
rm c 
# should rm without errors 
legit-rm c 
# test to make sure c is deleted 
legit-show :c 
# test to make sure d and c are both deleted 
rm a b c d 
