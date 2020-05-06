# rename the png output from Photoshop Layer Comps to Files
# to the format the calculator uses

from pathlib import Path

for n in Path.cwd().glob('*.png'):
    new_name = n.name[:4] + n.name[10:]
    n.rename(new_name)
