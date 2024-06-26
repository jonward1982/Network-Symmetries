'''
Batch runs of saucy on networks within a given directory with relative path given by stub. The graphs should be in the format readable by saucy:

#nodes #edges #colours
edgenode edgenode
...                                                                                                                

The output from saucy is written to two files, one containing the automorphism generators (.gaut) and the other containing the output log (.log).

'''

import os
import subprocess
import time
start_time = time.time()

# Directory name and path
dname='test_examples/'
dstub='../graphs/format_scy/'
stub=dstub+dname


count=1
# Loop
for dirpath, dirnames, files in os.walk(stub):
    if 'conversion_code' not in dirpath:
        if len(dname)>0 and not os.path.exists(dname):
            print(f'Make directory: {dname}')
            os.makedirs(dname)        
        if len(dirnames)==0:     
            for fname in files:
                fnamestub=fname.replace('.scy','')
                if fname[0]!='.' and not os.path.isfile(os.path.join(dname,fnamestub)+'.gaut'):                    
                    fgaut=open(os.path.join(dname,fnamestub)+'.gaut','w')
                    flog=open(os.path.join(dname,fnamestub)+'.log','w')
                    print('{0:6}\t Processing: {1:20}\t Runtime: {2:e}'.format(count,fnamestub,time.time() - start_time))
                    p=subprocess.Popen(['saucy','-s',os.path.join(dirpath,fname)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    output, error = p.communicate()
                    fgaut.write(output.decode("utf-8"))
                    flog.write(error.decode("utf-8"))
                    fgaut.close()
                    flog.close()
                
                    count+=1

                elif fname[0]!='.':
                    print('{0:6}\t Existing file: {1:20}\t Runtime: {2:e}'.format(count,fnamestub,time.time() - start_time))
                    
                    
print("--- Total time: {0} seconds ---".format(time.time() - start_time))
