import os
import sys
from stat import *
from mylist import *
from random import randrange
from mystat import *


# cmp function for list lookups
# cmp node objects 
def node_obj_cmp(node, obj):
    if node.nobj == obj:
        return True
    else:
        return False

# compare object names

def node_objname_cmp(node, name):
    if node.nobjname == name:
        return True
    else:
        return False

def node_objid_cmp(node, id):
    if node.nobjid == id:
        return True
    else:
        return False

def find_me(obj, path, fileobj):
    if obj.objid == fileobj.objid:
        fileobj.path = path
        raise Exception
def dir_files(obj, path, self):
    if obj.dir == 0:
        self.total_files += 1


def dirs(obj, path, self):
    if obj.dir == 1:
        self.dir_total += 1
'''

# def find_path_helper(node, path, obj):
#     if node.nobjname == obj.name:
#         obj.path = path
#         raise StopIteration

def find_path_helper(node, path, obj):
    if obj.nobjname == obj.name:
        obj.path = path
        raise StopIteration'''
# file objects 
# mandatory to have these members.
# name - file name (not the full path)
# objid - file object is thisis the inode no. in the stat
# stat - stat object of the file returned by os.stat api.
# dir 0 (default) implies it is not directory but a regular file.
# dir 1 implies it is a directory.
# 

class myfile():

    # look above for argument descriptions.
    # raise exception if dir is 1 and not a dir
    # raise exception fi dir is 0 and not a regular file.
    # DO NOT CHANGE THIS. 
    # you can add additional members if required.

    def __init__(self, objid, name=None, stat=None, dir=0):

        # leave the following in there.
        if name and '/' in name:
            raise Exception("Bad name in file")
        if dir and stat and not S_ISDIR(stat.st_mode):
            s=f'{name} is not a directory'
            raise Exception(s)
        if not dir and stat and not S_ISREG(stat.st_mode):
            s=f'{name} is not a file'
            raise Exception(s)

        self.name=name
        self.objid = objid
        self.stat=stat
        self.dir=dir
        #self.path = None
        #YOUR CODE
        #raise NotImplementedError

    
    # return the file path from root of the tree to which it belongs.
    # eg., I will create a file object with
    # fobj=myfile(241573) ie. only with objectid.
    # print(fobj.path(tree))
    # where this file is part of the tree.  Note: not this instance
    # of the object but the same objectid.
    # it should print the file path.
    # the objectid is found by "ls -i1" in any of the subdirectory
    # of the kernel-0 folder sent to you.  you can do that even on windows
    # with powershell i believe.
    # this function should print the full path of that objectid starting
    # from the kernel-0 folder.
    # eg., if the file kernel-0/mm/f1.c and its objectid is 241573
    # then fobj.file_path(tree) should print kernel-0/mm/f1.c
    # Note: this has to be recalculated from the tree when this function
    # is called. Tree was the object obtained from convert_to tree function
    # at the end of this file.


    def file_path(self, tree):
        # node = tree.root
        # tree.func_traverse(find_path_helper, self)
        # return self.path
        try:
            tree.func_traverse(find_me, self) # tree.traverse(find_me, self)
        except Exception:
            #print(f'object found')
            return self.path
        return None
        #YOUR CODE
        #raise NotImplementedError

    # return the file size
    # required for the binary tree organization of these file objects.
    # for assignment 6.
    #

    def file_size(self):
        pass
        #YOUR CODE
        raise NotImplementedError

    # this is just a helper. feel free to modify the way you want it to help
    # you.

    def __str__(self):
        return self.name

# directory objects inherit from file, uses 
# all of what file has plus some more interfaces.


class mydir(myfile):

    # DO NOT CHANGE THIS.
    # you can add any members below this.

    def __init__(self, objid, name=None, stat=None ): # chk it
        super().__init__(objid, name, stat, 1)
        self.total_files = 0
        #YOUR CODE
        #raise NotImplementedError

    # find the total no. of files underneath this directory including 
    # the directories (as they are also files) as well. 
    # eg., if you have a folder : kernel-0/mm/f1.c and kernel-0/mm/f2.c
    # dir_total_files of the directory kernel-0 will print : 3. two regular
    # files and one directory file "mm".
    # use case will be :
    # dir=mydir(245173)
    # dir.dir_total_files(tree)
    # where this directory is part of the tree.  Note: not this instance
    # of the object but the same objectid.
    # Note this has to be "calculated" every time the function is called
    # from the passed tree.


    def dir_total_files(self, tree):
        #YOUR CODE
        path = self.file_path(tree).split('/')
        pobj = tree.root
        for i in range(1, len(path)):
            pobj = tree.lookup(pobj, path[i])
        if pobj:
            tree.func_node_traverse(pobj, mydir_files, self)
            return self.total_files
        #raise NotImplementedError
        #pass

    # the below function is similar as above but should print the only the total
    # no. of directories underneath this directory.
    # Note this has to be "calculated" every time the function is called
    # from the passed tree. 

    def dir_total_dirs(self, tree):
        pass
        #YOUR CODE
        #raise NotImplementedError


class mynode():
    # pobj - parent object
    # obj - this object
    # objname - name of this object
    # objid - unique id of this object. for file and dir it is inode numbes.
    # Do not change this.

    def __init__(self, pobj, obj, objname, objid):
        self.child_list = mylist("list")
        self.nobj=obj
        self.nobjname = objname
        self.nobjid=objid
        self.npobj = pobj

class mytree():

# init functionf or root object and name and its object id.
# (object id for these objects are all inode numbers).
# Do not change this.

    def __init__(self, obj, root_name, id):
        self.root=mynode(None, obj, root_name, id)
        self.total_nodes=1

# the following two functions are helper functions for 
# constructing the tree, insertions etc..


# Lookup objname from a parent node, if found return
# node object. 
# If it does not  exist, create a node for that objname
# objid combinations, ensure to add it to the appropriate child
# list.

    def lookup_create(self, pobj:mynode, objname, objid, obj):
        #YOUR CODE
        if pobj == None:
            return self.root
        else:
            print("in else loop")
            print(self.total_nodes)
            for i in pobj.child_list:
                # print(i)
                if i.nobjname == objname:
                    return i
            n = mynode(pobj, obj, objname, objid)
            pobj.child_list.add(n)  ### check
            self.total_nodes += 1
            return n

        #raise NotImplementedError

# Lookup objname from a parent node, if found return
# node object. If not, return None.

    def lookup(self, pobj:mynode, objname):
        #YOUR CODE
        if pobj == None:
            return self.root
        else:

            for i in pobj.child_list:
                if i.nobjname == objname:
                    return i
                return None
        #raise NotImplementedError


# Method on the tree object to traverse and it will call the function
# func with the passed arguments (variable argument args), for 
# every line of the object it will generate as output corresponding 
# to the input file in function convert_input_to_tree().
#
# for the eg. mentioned in the comments of that function
# the function func() will get called for each of the
# lines given there. And that string will be passed as first argument to the
# function.

# func_traverse(tree, test_func, argobj) returned by convert_input_to_tree() will call 
# test_func(fobj, "kernel-0", argobj) where fobj is the mydir obj for kernel-0.
# test_func(fobj, "kernel-0/arch", argobj) where fobj is the mydir obj for kernel-0/arch.
# test_func(fobj, "kernel-0/arch/boot", argobj) where fobj is the mydir obj for kernel-0/arch/boot.
# test_func(fobj, "kernel-0/arch/boot/bootloader.lds", argobj) where fobj is the  myfile obj 
# for kernel-0/arch/boot/bootloader.lds.

# you can test this function by putting the string in some file or std output
# and then compare the entire output with the original input file (sort both to
# avoid any ordering issues).

    def __traverse__(self, node, prefix, func, *args):
        if prefix == "":
            path = node.nobjname
        else:
            path = prefix + '/' + node.nobjname
        func(node.nobj, prefix, *args)
        prefix = path

        for c in node.child_list:
            self.__traverse__(c, prefix, func, *args)
        # return prefix

    def func_traverse(self, func, *args):
        #YOUR CODE
        self.__traverse__(self.root, "", func, *args)
        #raise NotImplementedError
        #pass

# exactly same as above function except that the traversal starts
# from an intermediary mynode() object ie., an interior node.

    def func_node_traverse(self, node, func, *args):
        #YOUR CODE
        self.__traverse__(node, "", func, *args)
        #raise NotImplementedError
        #pass

# some debug stuff may be useful.

    def dump1(self, root):
        print(root.obj)
        print(f'{root.obj} Child: ', end="")
        for i in root.child_list:
            print(f'{i.obj}, ', end="")
        print('\n')
        for i in root.child_list:
            self.dump1(i)

# some debug stuff may be useful.

    def dump(self):
        print(f'Total Nodes: {self.total_nodes}')
        self.dump1(self.root)


# Function takes an input file name 
# and converts that into an object instance of 
# the tree class as defined above.
# you can only use the operations given above to construct the tree.
# no other functions should be added.
# input file will be of the form:
#kernel-0
#kernel-0/arch
#kernel-0/arch/alpha
#kernel-0/arch/alpha/boot
#kernel-0/arch/alpha/boot/bootloader.lds
# the above should be converted to tree with root object being the
# directory object - kernel-0, and there are arch, alpha and boot as
# directory objects below and bootloader.lds as a file object below.
# construct the appropriate hierarchy. The mynode.obj should be 
# either a mydir or myfile object as defined above.

# returns "tree" object.

# hint use readlines, strip, and split if required  and os.stat

def convert_input_to_tree(filename):
    fd = open(filename)
    # create the tree with the rootname
    myline = fd.readline()
    rootname = myline.strip()
    st=mystat(rootname)
    rootdir=mydir(st[ST_INO], rootname, st)
    tree = mytree(rootdir, rootname, st[ST_INO])
    #pass
    # Step 2 : loop through the files to read line by line and create the tree
    myline = fd.readline()
    while(myline):
        myline  = myline.strip()
        dw = myline.split('/')
        pobj = None
        st = mystat(myline)
        if S_ISDIR(st.st_mode):
            obj = mydir(st[ST_INO],dw[-1], st)
        else:
            obj = myfile(st[ST_INO], dw[-1], st)

        for i in range(len(dw) - 1):
            if i==0:
                pobj = tree.root
                continue
            pobj = tree.lookup(pobj, dw[i])
           # assert(pobj)

        obj = tree.lookup_create(pobj, dw[-1], st[ST_INO], obj)
        myline = fd.readline()
    return tree
        #st = mystat(myline)
        #if S_ISDIR(st.st_mode):
         #   pass
    #YOUR CODE
    #raise NotImplementedError

