# -*- coding: UTF-8 -*-
import math
import string
import os

#string s and t, if each letter in t exists in s, then return true
def find_char(s, t):
    print ("src: %s, target: %s" % (s, t))
    for c in t:
        if c not in s:
            #print ("%c not existing in %s" %(c, s))
            return False
    print ("each of %s exists in %s" %(t, s))
    return True

def find_minimum_match(s, t):
    m = []
    found = []
    
    for c in t:
        if c not in m:
            m.append(c)
            
    print ("m: %s" %(m))
    m_lenth = len(m)
    s_lenth = len(s)
    print ("source string lenth: %s" % (s_lenth))
    
    for low in range (s_lenth):
        high = low        
        #window must be within range(lenth)
        while  high < s_lenth + 1:
            win = high - low
            print ("current window:%d - %d, lenth: %d, min_win must be: %d" %(low, high, win, m_lenth))
            if win < m_lenth:
                high += 1
                continue
            else:
                ret = find_char(s[low:high], m)
                if ret == True:
                    print ("found sub-string:%s"% (s[low:high]))
                    if len(found) == 0:
                        found = s[low:high]
                    elif len(found) > len(s[low:high]):
                        found = s[low:high]
                        
            high += 1
    print ("final matched: %s" %(found) )
    return found
src = "ADOBECODEBANC"
target = "ABCA"
#find_minimum_match(src, target)


def distance(x1, y1, x2, y2):
    dist = math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    return dist

#计算2点之间最近距离
def find_min_distance (points):
    min = 0
    for s in points:
        print ("src: ", s)
        for d in points:
            print ("dst: ", d)
            if s != d:
                dist = distance (s[0], s[1], d[0], d[1])
                print ("from %s to %s: %s" %(s, d, dist))
                if  min ==0:
                    min = dist
                if  dist < min:
                    min = dist
                print ("from %s to %s: %f" %(s, d, min))
                    
    print ("minimum distannce: %.2f" % min)     
    return min

spots = [(10, -3), (2,5), (3,-9), (-5, -9), (-3, 10)]
#find_min_distance(spots)

#convert ip address to a decimal
def ipAddr_union(ip_addr):
    print ("ip_addr: ", ip_addr)
    li = ip_addr.split('.')
    new_li = []
    print("binary values of dots:", li)   # ['10', '3', '9', '12']
    for i in li:
        numStr = str(bin(int(i)))
        binStr = numStr.split('b')[1]
        # print(binStr)
        while len(binStr)< 8:
            binStr = '0'+binStr
        new_li.append(binStr)
    print(new_li)
    res_str = ''
    for i in new_li:
        res_str += i
    print("combined: ", res_str)   # 00001010000000110000100100001100
    res_int = int(res_str, 2)
    print("decimal: ", res_int)   # 167971084
    return (res_int)
#ipAddr_union('1.1.1.2')
#ipAddr_union('10.3.9.12')

pi = 3.141592653
print('%10.3f' % pi) #字段宽10，精度3
print("pi = %.*f" % (3,pi)) #用*从后面的元组中读取字段宽度或精度
print('%010.3f' % pi) #用0填充空白
print('%-10.3f' % pi) #左对齐
print('%+f' % pi) #显示正负号 
                
def for_loop():
    for letter in 'Python':     # 第一个实例
        print ('当前字母 :', letter)
 
    fruits = ['banana', 'apple',  'mango']
    for fruit in fruits:        # 第二个实例
        print ('当前水果 :', fruit)
    
    fruits = ['banana', 'apple',  'mango']
    for index in range(len(fruits)):
        print ('当前水果 :', fruits[index])
        
    for num in range(10,20):  # 迭代 10 到 20 之间的数字
        for i in range(2,num): # 根据因子迭代
            if num%i == 0:      # 确定第一个因子
                j=num/i          # 计算第二个因子
                print ('%d 等于 %d * %d' % (num,i,j))
                break            # 跳出当前循环
        else:            # 循环的 else 部分
            print (num, '是一个质数')
    
    sum = 0
    i = 1
    while  i <=100:
        sum += i
        i   += 1
    print("sum: ", sum)
    
    
    print ("Good bye!")
    return  True

#for_loop()

#随便输入一串字符串，假定没有空格，没有换行符，没有转义，
#分别统计出其中英文字母、空格、数字和其他字符的个数，
#分别使用char，space，digit，others表示。
def counting_types():
    s = input("输入一串字符串，假定没有空格，没有换行符，没有转义: ")
    
    char = 0
    space = 0
    digit = 0
    others = 0
    for i in s:
        if i in string.ascii_lowercase + string.ascii_uppercase:
            char += 1
        elif i.isspace():
            space += 1
        elif i.isnumeric:
            digit += 1
        else:
            others += 1
    
    print ("string entered: %s" %(s))
    print ("char: %d" %(char))
    print ("space: %d" %(space))
    print ("digit: %d" %(digit))
    print ("others: %d" %(others))

#counting_types()


#给定一个字符串，把里面所有的字母用其后的第5个字母替代，
#若其后第五个字母超出a～z或者A～Z的范围，则使用huawei
#在后面拼接，比如A用F代替，y用w代替，最终输出加密后的字符串。
def encode():
    st="huawei"
    s = input("enter the plain-text: ")
    d = []
    for c in s:
        if c in string.ascii_lowercase + string.ascii_uppercase: 
            i = ord(c)
            i += 5
            if 97 <= ord(c) <= 122:
                if i > 122:
                   d.append(st)
                else:
                   d.append(chr(i))
            elif 65 <= ord(c) <= 90:
                if i > 90:
                    d.append(st)
                else:
                   d.append(chr(i))
        else:
            d.append(c)
    
    encoded = ''.join(d)
    print("encoded: %s" %(encoded))
    
#encode()
    
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
         
    def getData(self):
        return self.val
    
    def getNext(self):
        return self.next
    
    def setData(self, new):
        self.val = new
        
    def setNext(self, new_next):
        self.next = new_next
         
class LinkedList:
    def __init__(self):
        self.head = ListNode(None)
        self.head.setNext(self.head)
    
    def add(self, item):
        temp = ListNode(item)
        temp.setNext(self.head.getNext())
        self.head.setNext(temp)
        print("add node %s to linked table %s" % (item, self))
        
        
    def remove (self, item):
        prev = self.head
        while prev.getNext() != self.head:
            cur = prev.getNext()
            if cur.getData() == item:
                prev.setNext(cur.getNext())
            prev = prev.getNext()
        print("removed node %s from linked table %s" % (item, self))
            
    def search(self, item):
        cur = self.head.getNext()
        while cur != self.head:
            #print ("node type: ", type(cur))
            if cur.getData() == item:
                print("found node: %s" % item)
                return True
            cur = cur.getNext()
        
        print("not found node %s" % item)
        return False
    
    def empty(self):
        return self.head.getNext() == self.head
    
    def size(self):
        count = 0
        cur = self.head.getNext()
        while cur != self.head:
            count += 1
            cur = cur.getNext()
        
        return count
    
    def listAll(self):
        cur = self.head.getNext()
        items = []
        while cur != self.head:
            items.append(cur.getData())
            cur = cur.getNext()
        print("all items: %s" % items)
        
    def reverseAll(self):
        cur = self.head.getNext()
        items = []
        while cur != self.head:
            items.append(cur.getData())
            cur = cur.getNext()
        print("all items: %s" % items)
        items.reverse()
        print("reversed all items: %s" % items)
            
print ("implementation of linked table")
if __name__ == '__main__':
    li = LinkedList()
    print ('li.empty() = %s, li.size() = %s' % (li.empty(), li.size()))
    
    li.add(98)
    print ('added 98, li.size() = %s' % (li.size()))
    li.add(18)
    print ('added 18, li.size() = %s' % (li.size()))
    li.add(38)
    li.listAll()
    li.reverseAll()
    li.search(98)
    li.remove(98)
    li.search(18)
    print ('removed 98, li.size() = %s' % (li.size()))
    li.reverseAll()


#装饰器
def dec(f):
    n = 3
    def wrapper(*args,**kw):
        return f(*args,**kw) * n
    return wrapper

@dec
def foo(n):
    return n * 2

#传值还是传地址，实际是传地址
#所以当a指向的值变化时，b由于获得的是指向a的一个指针，所以结果也会跟a的输出结果一样
a = [1,2,3,4]
b = a
a.append(5)
print ("a=",a)
print ("b=",b)
a += [6] 
print ("a=",a)
print ("b=",b)

# += 的区别
a = a + [7]
print ("a=",a)
print ("b=",b)
#为什么 += 和分开相加之后就不同结果了呢
#当a = a+[1]时，系统所做的是把a + [1]的结果先放到另外一个地址c中，然后再把a指向这个c地址
#但是b还是指向以前a的位置，以前位置的值并没有变化，所以a和b才会输出不一样的结果
#而+=操作，还是在原来a指向的地址上进行操作，所以b也会跟着变化

#总结：python中一个变量给另一个变量进行赋值操作(=)时，传的不是值，而是指针地址

#udpate or add a list/set
a = set('boy')
print ("a=",a)
a.add("python")
print ("a=",a)

#add and update are different
print("add and update are different:")
a = set('boy')
print ("a=",a)
a.update("python")
print ("a=",a)

#Python 函数装饰器
#他们是修改其他函数的功能的函数。他们有助于让我们的代码更简短，也更Pythonic（Python范儿）
def hi(name="yasoob"):
    return "hi " + name
 
print("hi:",hi())
# output: 'hi yasoob'
 
# 我们甚至可以将一个函数赋值给一个变量，比如
greet = hi
# 我们这里没有在使用小括号，因为我们并不是在调用hi函数
# 而是在将它放在greet变量里头。我们尝试运行下这个
 
print("hi:",greet())
# output: 'hi yasoob'
 
# 如果我们删掉旧的hi函数，看看会发生什么！
del hi
#print(hi())
#outputs: NameError
 
#print(greet())
#outputs: 'hi yasoob'

#在 Python 中我们可以在一个函数中定义另一个函数
def hi(name="yasoob"):
    print("now you are inside the hi() function")
 
    def greet():
        return "now you are in the greet() function"
 
    def welcome():
        return "now you are in the welcome() function"
 
    print(greet())
    print(welcome())
    print("now you are back in the hi() function")
 
hi()
#output:now you are inside the hi() function
#       now you are in the greet() function
#       now you are in the welcome() function
#       now you are back in the hi() function
 
# 上面展示了无论何时你调用hi(), greet()和welcome()将会同时被调用。
# 然后greet()和welcome()函数在hi()函数之外是不能访问的，比如：
 
#greet()
#outputs: NameError: name 'greet' is not defined

#我们可以创建嵌套的函数。现在你需要再多学一点，就是函数也能返回函数。
#其实并不需要在一个函数里去执行另一个函数，我们也可以将其作为输出返回出来
def hi(name="yasoob"):
    def greet():
        return "now you are in the greet() function"
 
    def welcome():
        return "now you are in the welcome() function"
 
    if name == "yasoob":
        return greet
    else:
        return welcome
 
a = hi()
print("a:", a)

print("a():" ,a())

#在 if/else 语句中我们返回 greet 和 welcome，而不是 greet() 和 welcome()。
#为什么那样？
#这是因为当你把一对小括号放在后面，这个函数就会执行；
#然而如果你不放括号在它后面，那它可以被到处传递，并且可以赋值给别的变量而不去执行它。

#当我们写下 a = hi()，hi() 会被执行，而由于 name 参数默认是 yasoob，所以函数 greet 被返回了。
#如果我们把语句改为 a = hi(name = "ali")，那么 welcome 函数将被返回。
#我们还可以打印出 hi()()，这会输出 now you are in the greet() function。


#将函数作为参数传给另一个函数
def hi():
    return "hi yasoob!"
 
def doSomethingBeforeHi(func):
    print("I am doing some boring work before executing hi()")
    print(func())
 
doSomethingBeforeHi(hi)
#outputs:I am doing some boring work before executing hi()
#        hi yasoob!

#你的第一个装饰器
def a_new_decorator(a_func):
 
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
 
        a_func()
 
        print("I am doing some boring work after executing a_func()")
 
    return wrapTheFunction
 
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")
 
a_function_requiring_decoration()
#outputs: "I am the function which needs some decoration to remove my foul smell"
 
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
#now a_function_requiring_decoration is wrapped by wrapTheFunction()
 
a_function_requiring_decoration()
#outputs:I am doing some boring work before executing a_func()
#        I am the function which needs some decoration to remove my foul smell
#        I am doing some boring work after executing a_func()

#如何使用 @ 来运行之前的代码：
@a_new_decorator
def a_function_requiring_decoration():
    """Hey you! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")
 
a_function_requiring_decoration()
#outputs: I am doing some boring work before executing a_func()
#         I am the function which needs some decoration to remove my foul smell
#         I am doing some boring work after executing a_func()
 
#the @a_new_decorator is just a short way of saying:
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

#from functools import wraps
 
def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction
 
#@a_new_decorator

def a_function_requiring_decoration():
    """Hey yo! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")
 
print(a_function_requiring_decoration.__name__)


# Output: a_function_requiring_decoration
from functools import wraps
def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction
 
@a_new_decorator
def a_function_requiring_decoration():
    """Hey yo! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")
 
print(a_function_requiring_decoration.__name__)
# Output: a_function_requiring_decoration


#我们接下来学习装饰器的一些常用场景
#蓝本规范
from functools import wraps
def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated
 
@decorator_name
def func():
    return("Function is running")
 
can_run = True
print(func())
# Output: Function is running
 
can_run = False
print(func())
# Output: Function will not run

#@wraps接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能。
#这可以让我们在装饰器里面访问在装饰之前的函数的属性
#https://www.runoob.com/w3cnote/python-func-decorators.html


def dec(f):
    n = 3
    def wrapper(*args,**kw):
        return f(*args,**kw) * n
    return wrapper
 
@dec
def foo(n):
    print("n=%s, n*2 = %s" %(n, n * 2))
    return n * 2

foo(2)
foo(3)
foo(4)

#!/usr/bin/python

dict = {'Name': 'Runoob', 'Age': 27}

print ("Value : %s" %  dict.get('Age'))
print ("Value : %s" %  dict.get('Sex', "Not Available"))

#如果字典里面嵌套有字典，无法通过 get() 直接获取 value:
dict_test = {'Name': 'Runoob', 'num':{'first_num': '66', 'second_num': '70'}, 'age': '15'}
print(dict_test.get('first_num')) # None
print('{:^50}'.format('*'*50))    #格式化输出*
print(dict_test.get('num').get('first_num')) # 66

#不能加 default= 这几个字！
dict={}
dict.get('python') #返回None
#dict.get('python', default=None) #直接报错，这个错误在某些情况没有任何提示！让我找了好久bug
dict.get('python', None)
#dict.get('python', default='HHHH'）#直接报错
print ("Value : %s" %  dict.get('python', None))
dict.get('python', 'HHHH')          #返回HHHH
print ("Value : %s" %  dict.get('python', 'HHHH'))
