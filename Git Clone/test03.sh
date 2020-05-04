# test03 for legit-log
# by z5259931

# tests include:
# logging before any commits 
# logging after failed commits 

export PATH="$PATH:."

legit-log 
legit-init 
legit-log 
legit-commit -m shouldnotcommit
legit-log 
touch a 
legit-add a 
legit-commit -m commit-0
legit-log 
legit-commit -m shouldnotcommit
legit-log
echo hello >a
legit-add a
legit-commit -m commit-1 
legit-log 
