import os
import sys

# as discussed in the class and subsequent discussions 
# have an ADT for this and you can use this to create
# whatever you want.
# you are welcome to implement this in a way you want and use it.
# I am giving you a template where a single linked list
# can be used for multiple objects .. 
# to share code as much as possible in a single ADT.
# l1 = mylist(list) --> behaves like a list
# l2 = mylist(stack) --> supports stack and other operations(like push, pop
# etc.)  are disallowed.
# l3 = mylist(queue) --> same here. (like enqueue, dequeue etc.)

# you are welcome to use your own ADT whatever way.

class myelem():
    def __init__(self, obj):
        self.next=self
        self.prev=self
        self.obj=obj

class mylist():
    list_type=['stack', 'list', 'queue']

    # init function do not change this.

    def __init__(self, type):
        self.header=myelem(self)
        self.size=0
        if type not in self.list_type:
            raise Exception("List type incorrect")
        self.type=type
        self.tail=self.header

    # cmp function is sent some time for users of
    # the lookup to return the right object. See usage
    # below. See same_
    # see comment in mycrm.py above server_same and vm_same.. functions.
    # the cmp method is used if it is not None to check for object
    # equality. 
    # for each element in list:
    #        if (cmp(val, element) is true:
    # return object

    def lookup(self, val, cmp=None):
        temp = self.header.next
        while temp != self.header:
            if cmp != None:
                if cmp(temp.obj, val):
                    return temp.obj

            elif cmp == None:
                if temp.obj == val:
                    return temp.obj

            temp = temp.next
        return None

    
    # returns true if list is not empty
    # if it is empty, returns False.

    def not_empty(self):
        if self.size==0:
            return False
        else:
            return True

    def first(self):
        return self.header.next.obj

    def last(self):
        return self.tail.obj

    # adds the element to 
    def add(self, obj):
        if self.type != 'list':
            raise Exception("Add op supported only for list")
        new_node = myelem(obj)
        if self.size == 0:
            new_node.prev = self.header
            new_node.next = self.header
            self.header.next = new_node
            self.header.prev = new_node
            self.tail = new_node
            self.size += 1
        else:
            temp = self.header.next
            new_node.prev = self.header
            new_node.next = temp
            temp.prev = new_node
            self.header.next = new_node
            self.size += 1


    def push(self, obj):
        if self.type != 'stack':
            raise Exception("push op supported only for stack")
        #YOUR CODE
        new_node = myelem(obj)
        # print("pushed node =",new_node.obj,"size=",myl.size)
        if self.size == 0:
            new_node.prev = self.header
            self.header.next = new_node
            new_node.next = self.header
            self.header.prev = new_node
            self.tail = new_node
            self.size += 1
        else:
            new_node.prev = self.header
            new_node.next = self.header.next
            self.header.next.prev = new_node
            self.header.next = new_node
            self.size += 1
        #raise NotImplementedError
    
    def pop(self):
        if self.type != 'stack':
            raise Exception("pop op supported only for stack")
        #YOUR CODE
        element = self.header.next
        if self.size == 0:
            return None

        elif self.size == 1:
            self.tail = self.header
            self.header.prev = self.header
            self.header.next = self.header
            self.size -= 1
        else:
            temp = self.header.next
            self.header.next = temp.next
            temp.next.prev = self.header
            self.size -= 1
        return element.obj

    #raise NotImplementedError

    def peek(self):
        if self.type != 'stack':
            raise Exception("peek op supported only for stack")
        #YOUR CODE
        return self.header.next.obj
        #raise NotImplementedError

    def enqueue(self, obj):
        if self.type != 'queue':
            raise Exception("Enqueue op supported only for queue")
        #YOUR CODE
        new_node = myelem(obj)
        # print("new node added",new_node.obj)
        if self.size == 0:
            new_node.prev = self.header
            self.header.next = new_node
            new_node.next = self.header
            self.header.prev = new_node
            self.tail = new_node
            self.size += 1
        else:

            self.tail.next = new_node
            new_node.prev =self.tail
            new_node.next = self.header
            self.header.prev = new_node
            self.tail = new_node
            self.size += 1

    def dequeue(self):
        if self.type != 'queue':
            raise Exception("Dequeue op supported only for queue")
        element = self.header.next
        if self.size == 0:
            return None
        elif self.size == 1:
            self.tail = self.header
            self.header.prev = self.header
            self.header.next = self.header
            self.size -= 1
        else:
            temp = self.header.next
            self.header.next = temp.next
            temp.next.prev = self.header
            self.size -= 1
        return element.obj

   #delete objects for all
    def delete(self, obj):
        temp = self.header.next
        if self.size == 1 and self.tail.obj == obj:
            self.tail = self.header
            self.header.prev = self.header
            self.header.next = self.header
            self.size -= 1
        elif self.tail.obj == obj:
            temp = self.tail.prev
            temp.next = self.header
            self.header.prev = temp
            self.tail = temp
            self.size -= 1
        elif temp.obj == obj:
            self.header.next = temp.next
            temp.next.prev = self.header
            self.size -= 1
        else:
            found = 0
            while temp.next != self.header:
                if temp.obj == obj:
                    found = 1
                    break
                temp = temp.next
            if found == 1:
                temp.prev.next = temp.next
                temp.next.prev = temp.prev
                self.size -= 1


    # iterator objects for all.
    def __iter__(self):
        self.first=self.header.next
        return self
    def __next__(self):
        if self.first == self.header:
            raise StopIteration
        elif self.first!=self.header:
            element=self.first.obj
            print(element)
            self.first=self.first.next
            return element
    def __str__(self):
        s=''
        h=self.header
        e=self.header.next
        s=f'List size: {self.size}'
        s += '\n'
        while e != h:
            s += f'{e.obj}'
            if (e.next != h):
                s += '\n'
            e = e.next
        s += '\n'
        if self.tail != self.header:
            s += f'Tail: {self.tail.obj}'
        s += '\n'
        return s
             

def main():
    pass

if __name__ == "__main__":
    main()
