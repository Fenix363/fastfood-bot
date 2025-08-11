""" for while"""
from itertools import count

# fruits = ['apple', 'banana', 'cherry']
# for fruit in fruits:
#     print(fruit)

#----------------------------------------------------

#misol 1
# for i in range(1,11):
#     print(i,end=" ")

#misol 2
# for i in range(0,21,2):
#     print(i,end=" ")

#misol 3
# for i in range(1,31,2):
#     print(i,end=" ")

#misol 4
# text="UZBEKISTON"
# for i in text:
#     print(i,end=" ")

#misol 5
# for _ in range(5):
#     print("Python o'rganish ajoyib")

#misol 6
# for i in range(10,0,-1):
#     print(i,end=" ")

#misol 7
# for i in "Hello, World":
#     print(i,end=" ")

#misol 8
# text=input("So'z kiriting: ")
# count=0
# for i in text:
#     count+=1
#
# print(f"so'z uzunligi: {count} ta")

#misol 9
# num=[10,15,25,68,66]
# for i in num:
#     print(i*2)

#misol 10
# text="Python"
# for i in text[::-1]:
#     print(i,end=" ")

#------------Medium-------------------

#misol 1
# for i in range(1,100):
#     if i%3==0:
#         print(i)

#misol 2
# a=0
# b=1
# for i in range(10):
#     print(a,end=" ")
#     temp=a+b
#     a=b
#     b=temp

#misol 3
# text=input("soz kiriting: ")
# print(text)
# for i in text:
#     if i=='A' or i=='a' or i=='O' or i=='o' or i=='I' or i=='i' or i=='U' or i=='u' or i=='E' or i=='e':
#         print(i,end=" ")

#misol 4
# text=input("So'z kiriting: ")
# sanoq=0
# for i in text:
#     if i==i.upper():
#         sanoq+=1
#
# print(f"Katta hariflar: {sanoq} ta")


#------------------------------while----------------------------------

#misol 1
# i=1
# while i<=5:
#     print(i,end=" ")
#     i+=1

#misol 2
# while True:
#     son=int(input("Manfiy son kiriting:"))
#     if son<0:
#         pass
#     else:
#         break

#misol 3
# i=1
# while i<=5:
#     print("Python")
#     i+=1

#misol 4
# i=1
# while i<=10:
#     i += 1
#     if i%2==0:
#         print(i,end=" ")

#misol 5
# while True:
#     num=int(input("son kiriting:"))
#     print(f"{num}^2={num**2}")

#misol 6
# print("stop yozangiz dastur tugaydi:")
# while True:
#     text=input("soz kiriting:")
#     if text=="stop":
#         break
#     else:
#         print(text)

#misol 7
# text="python"
# i=0
# while i<len(text):
#     print(text[i])
#     i+=1

#misol 8
# text="salom"
# i=1
# while i==1:
#     print(text[::-1])
#     i-=1

#misol 9
# i=0
# res=0
# while i<=10:
#     print(res)
#     res=res+i
#     i+=1

#misol 10
# print("exit dasturni toxtatadi")
# while True:
#     text=input("Ism kiriting:")
#     if text=="exit":
#         break

"""-----------------MEDIUM---------------"""
#misol 1
# num=int(input("son kiriting:"))
# i=0
# while i<=num:
#     print(i)
#     i+=1

#misol 2
# i=1
# while i<100:
#     i+=1
#     if i%2!=0:
#         print(i)


