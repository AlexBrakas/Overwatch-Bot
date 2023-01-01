from os import listdir
char ="Junkrat"
from random import choice
chr_list=listdir(f"characters_vc/{char}")  
chosen = choice(chr_list)
print(chosen)
        