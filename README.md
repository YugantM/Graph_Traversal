# Graph_Traversal



This repo contains the folders with PKGBUILDs.



The python tool travels through the folders and reads the PKGBUILD files. It extracts the dependecies from them.

Meanwhile, it generates dataframe named main_frame which is an adjacency matrix cotaining 1 and 0 as cell values.



**main_frame**

Index = list of packages in the system

Columns = list of packages in the system

Cell value: 1 represents relation between two packages, 0 means no relation between two packages.



**Topological sorting**

A python framework ***toposort*** is used to sort the graph in topological order.

It also helps to check the cyclic dependecies.



#### *Notes:*

The parser can be modified to extract different types of variables from the PKGBUILDs.

Future work: identifying the changes in packages.