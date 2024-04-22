import os
import re

# allgapfilenames=open('filenames.gap','w')
# allgapfilenames.write('fnamesall:=[')

# Works for specific directory
# stub='../gap/RegTree'
# stub='../gap/bipartite'
# stub='../gap/nmlegs'
# stub='../gap/nmpartite'
# stub='../gap/hospital'
stub='../gap/Johnson'

count=1

firstdir=True
for dirpath, dirlist, files in os.walk(stub):
    if len(files)>0:
        # to stub and to file name
        tstub=re.sub('../gap/','',dirpath)
        tname=tstub.split('/')[-1]
        # print(tstub,tname,len(files))
        
        filename=os.path.join(tstub,tname)+'.gap'
        # print(count,filename)

#         # Add filename to allgapfilenames
#         if firstdir:
#             firstdir=False
#         else:
#             allgapfilenames.write(',\n')
#         allgapfilenames.write('"{0}"'.format(filename));
                
        # Make new directory if needed - mirrors directory structure in ../gap
        print count, tstub
        if not os.path.exists(tstub):
            print 'Make directory: '+tstub
            os.makedirs(tstub)
            # print('Make directory: ',tstub)
        count+=1
        
        
        # Open new file named filename
        # print(count,filename)
        fnames=open(filename,'w')
        fnames.write('name:="{0}";\n'.format(tname))
        fnames.write('stub:="{0}/";\n'.format(tstub))
        fnames.write('fnames:=[')
            
        firstfile=True

        for file in files:
            if file[-3:]=='gap':                
                if firstfile:
                    firstfile=False
                else:
                    fnames.write(',\n')
                fnames.write('"{0}"'.format(os.path.join(dirpath,file)))

        fnames.write('];;\n')        
        fnames.close()     
            

# allgapfilenames.write('];;')
# allgapfilenames.close()



#         fname=os.path.join(dirpath,file[:-4])
        #         # print(fname
        #         # foutname=os.path.join(tstub,file[:-4])+'.gap'                

        #         # Filenames writing:
        #         # print '"{0}"'.format(foutname)
        #         # if firstfile:
        #         #     firstfile=False
        #         # else:
        #         #     ffilenames.write(',\n')
        #         # ffilenames.write('"{0}"'.format(foutname))



       
        #         count+=1
                
                # # Write generators to file
                # fout=open(foutname,'w')
                # N,generators=readautomorphismgroup(fname)
                # fout.write('N:={0};;\n'.format(N))
                # fout.write('z:=[')

                # first=True
                # for generator in generators:    
                #     if first:
                #         first=False
                #     else:
                #         fout.write(',')
                #     for transposition in generator:        
                #         fout.write('({0},{1})'.format(transposition[0]+1,transposition[1]+1))
    
                # fout.write('];;\n')
                # fout.write('g:=Group(z);')
                # fout.close()

# ffilenames.write('];;')

# fname='CubicVT14-2'

# fout=open('test.gap','w')

# N,generators=readautomorphismgroup(stub+fname)

# fout.write('N:={0};;\n'.format(N))
# fout.write('z:=[')

# first=True
# for generator in generators:    
#     if first:
#         first=False
#     else:
#         fout.write(',')
#     for transposition in generator:        
#         fout.write('({0},{1})'.format(transposition[0]+1,transposition[1]+1))
    
# fout.write('];;\n')
# fout.write('g:=Group(z);')




# stub='../gaut/Cubic/'
# fname='CubicVT14-2'
# fout=open('test.gap','w')

# N,generators=readautomorphismgroup(stub+fname)

# fout.write('N:={0};;\n'.format(N))
# fout.write('z:=[')

# first=True
# for generator in generators:    
#     if first:
#         first=False
#     else:
#         fout.write(',')
#     for transposition in generator:        
#         fout.write('({0},{1})'.format(transposition[0]+1,transposition[1]+1))
    
# fout.write('];;\n')
# fout.write('g:=Group(z);')





#     gstring=''
#     for transposition in generator:
#         gstring=gstring+'({0},{1})'.format(transposition[0]+1,transposition[1]+1)
#     gstring

