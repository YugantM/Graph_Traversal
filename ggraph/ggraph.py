#!/usr/bin/env python
import sys
import os
import pandas as pd
import networkx as nx
from toposort import toposort, toposort_flatten
from collections import defaultdict 

# current directory
path = "./"

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


def ggraph():
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
     
    return main_depends       

# number of dependecies count
#for each in range(len(main_frame.index)):
#    print("Module:{0}, Count {1}".format(list(main_frame.index)[each],list(main_frame.iloc[each]).count(1)))

def main():
    if len(sys.argv) == 1:
        print("\n".join(toposort_flatten(ggraph())))

    elif len(sys.argv) == 2:
        lis = toposort_flatten(ggraph())
        if sys.argv[1] in lis:
            print("\n".join(lis[:lis.index(sys.argv[1])]))
            #return (int(sys.argv[1])+int(sys.argv[2]))  
    else:
        print("ERROR:",str(len(sys.argv)-1)," arguments given instead of 1 optional argument")


if __name__ == "__main__":
    main()




