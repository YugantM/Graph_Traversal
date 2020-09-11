#!/usr/bin/env python
import sys,getopt
import os
import pandas as pd
import networkx as nx
from toposort import toposort, toposort_flatten
from collections import defaultdict 

# current directory
path = "../"

# list of folders of the given path is assigned to the variable folder_list
folder_list = [each for each in list(os.walk(path))[0][1] if "python" in each]

# variable to be identify
variables_to_look = ['depends','makedepends']

# optional function which identifies whether the given line contains a variable or not
def variable_or_not(line):
    
    if "=" in line and len(line.strip().split("=")[0].split(" "))==1:
        return each_line.strip().split("=")[0]
    else:
        return False

def get_depends(pack):
    global main_frame
    #ggraph()
    #print(main_frame)
    return main_frame.index[main_frame[pack] == 1].tolist()

def flat(lis):
    
    temp = []
    
    for each in lis:
        
        if type(each) == str:
            temp.append(each)
        else: 
            for x in each:
                temp.append(x)
        
    return temp


def custom_list(pack):
    global main_frame

    ggraph()
    #os.chdir("..")
    #os.system("ls")
    #print(main_frame)
    #main_frame = main_frame.T
    label = "lavel-"
    levels = {}

    current_level = 0
    levels[label+str(current_level)] = [pack]
    
    bases = []
    
    #for each in list(main_frame.columns):
        
        #if len(get_depends(each)) == 0:
            #bases.append(each)
        
    level_list = get_depends(pack)
    
    if len(level_list) == 0:
        return []

    while len(level_list) !=0 :
        
        
        #print(current_level,"|",level_list,"|",levels)
        #print(levels)
        temp = []
        for each in level_list:

            if each not in flat(list(levels.values())):
                
                if each not in bases:
                    temp.append(each)
                
        #current_level +=1
        
        #print(current_level,temp)
        if len(temp)>0:
            levels[label+str(current_level)] = temp

            
            level_list = flat([get_depends(x) for x in temp if len(get_depends(x)) >= 1])
            
            if len(level_list):
                current_level +=1
        else:
            level_list = []
            
           
    levels['base'] = bases
    
    return flat(list(levels.values()))



def subframe(frame,lis):
    return frame[lis].T[lis].T



def ggraph(f=False):

    global main_frame,main_depends,args
    # start reading the dependencies
    # flag is set to True if the desired variable is there in the line
    flag = False

    # this dictionary will contain keys as package names and values as dependecies
    main_depends = {}

    # iterates through all the items in the folder_list
    for each_folder in folder_list:
        
        if os.path.isfile(path+each_folder+"/PKGBUILD"):
            # opens the file 
            with open(path+each_folder+"/PKGBUILD",'r') as file:
                
                # this variable contains all the lines of the given file
                temp = file.readlines()
                
                # stack is sub-list which will contain all the dependecies of the file
                stack = []
                
                # iterates through each line of the given file
                for each in temp:

                    # checks if the desired varable is at the given line
                    if each.split("=")[0] in variables_to_look:
                        flag = True
                    
                    # if variable is found
                    if flag == True:
                        
                        # appends the line if flag is true
                        stack.append(each.strip().replace("'",""))
                        #print(each.strip().replace("'",""))
                     
                    # if the bracket is being ended 
                    if ')' in each.strip():
                        flag = False
                        
                        # if there is dependencies availabe or not
                        if len(stack) > 0:
                            main_depends[each_folder] = stack
                        else:
                            main_depends[each_folder] = None

        else:
            print(path+each_folder+" does not contain PKGBUILD")
                    
                
    # this loop will clear the string of the main_depends       
    for each in list(main_depends.keys()):
        
        temp = []
        
        # iterates through list for given key
        for x in main_depends[each]:
            temp.append(x.split("=")[-1])
        
        # clears the line and gets the names of the dependencies
        main_depends[each] = set([each for each in " ".join(temp).replace("(","").replace(")","").split(" ") if len(each)>0])

    # all the names of the modules which are in the folders
    main_modules = list(main_depends.keys())

    # all the names of the main modules and its dependecies, general list
    all_modules = list(set([j for i in list(main_depends.values()) for j in i]+main_modules))

    # dataframe with index and columns as list of all the modules
    main_frame = pd.DataFrame(columns=all_modules,index=all_modules).fillna(0)

    # iterates through each cell value of the dataframe
    for ind in list(main_frame.index):
        for col in list(main_frame.columns):
            
            # checks if the given index is in the main module list and index and column names are not same
            if ind in main_modules and col!=ind:
                
                # iterates through the list of dependencies for the given module
                for each in main_depends[ind]:
                    
                    # set the cell value to 1 if there is dependencies between two modules
                    main_frame.loc[ind,each] = 1

    if f==True:

        sub_depends = {}
        temp = []

        #print(main_depends)
        for each in args:
            temp= temp + [each] + custom_list(each)

        for each in temp:
            sub_depends[each] = set(custom_list(each))
        #subframe(main_frame,temp)

        #print(sub_depends)
        return ",".join(list(toposort_flatten(sub_depends))[::-1])

    #os.system("ls")
    return main_depends       



# number of dependecies count
#for each in range(len(main_frame.index)):
#    print("Module:{0}, Count {1}".format(list(main_frame.index)[each],list(main_frame.iloc[each]).count(1)))

def main(argv):
    global main_frame,args

    
    if len(sys.argv) == 1:

        main_frame.to_csv("./main.csv")
        print(toposort_flatten(ggraph())[::-1])
        return list(toposort_flatten(ggraph()))

    elif len(sys.argv) == 2:
        #print("hi")
        lis = toposort_flatten(ggraph())
        if sys.argv[1] in lis:
            print("\n".join(lis[:lis.index(sys.argv[1])]))
            return (int(sys.argv[1])+int(sys.argv[2]))
    #else:
        #print("ERROR:",str(len(sys.argv)-1)," arguments given instead of 1 optional argument")

    opts, args = getopt.getopt(argv,"hs:p:",["help","slicing","package"])

    for opt, arg in opts:
        if opt == '-h':
            print("ggraph -p <PACKAGE_NAME>")
            sys.exit()

        elif opt in ("-s","--slice"):

            args = arg.split(",")
            # removing whitespace from the module names 
            args = [each.strip("") for each in args]
            result = ggraph(True)
            print(result)
            return result

        elif opt in ("-p", "--package"):
            
            #os.system("ls")
            print(",".join(custom_list(arg)))
            return ",".join(custom_list(arg))

        else:

            print('No such options available')


if __name__ == "__main__":
    main(sys.argv[1:])




