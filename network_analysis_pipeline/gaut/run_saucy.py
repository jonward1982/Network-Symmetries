'''
Runs saucy on a single network contained in a source file written in the format readable by saucy:

#nodes #edges #colours
edgenode edgenode
...

The output from saucy is written to two files, one containing the automorphism generators (.gaut) and the other containing the output log (.log). 
'''

import subprocess

# Source file
fname='C4' # File name (without file extension)
dname='test_examples/' # Directory name
sstub='../graphs/format_scy/' # Relative path

# Run saucy code
p=subprocess.Popen(['./saucy_mac','-s',sstub+dname+fname+'.scy'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
output, error = p.communicate()

# Write output to file
fgaut=open(dname+fname+'.gaut','w')
flog=open(dname+fname+'.log','w')
                   
fgaut.write(output.decode("utf-8"))
flog.write(error.decode("utf-8"))

fgaut.close()
flog.close()
