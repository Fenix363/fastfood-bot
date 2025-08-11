"""------------------------FOR---------------------------"""
"""-----------------------BASIC--------------------------"""
"""MISOL 1"""
# for i in range(1,10+1):
#     print(i)

"""MISOL 2"""
# for i in range(1,21):
#     if i%2==0:
#         print(i)

"""MISOL 3"""
# text="Python"
# for i in text:
#     print(i)

"""MISOL 4"""
# for i in range(1,6):
#     print("Salom dasturchi")

"""MISOL 5"""
# for i in range(1,51):
#     if i%2!=0:
#         print(i)

"""MISOL 6"""
# text="Salom"
# siz=len(text)
# for i in range(siz-1,-1,-1):
#     print(text[i])

"""MISOL 7"""


"""MISOL 8"""
# for i in range(1,11):
#     print(i,end=",")

"""MISOL 9"""
# text="Python"
# for i in text:
#     if i=="o":
#         print(i)

"""MISOL 10"""
# text=input("5 ta ism kiriting:").split()
# siz=len(text)
# for i in range(0,siz):
#     print(text[i])

"""MISOL 11"""
# RES=0
# for i in range(1,101):
#     RES+=i
# print(RES)

"""MISOL 12"""
# text="Hello,World!"
# size=len(text)
# for i in range(0,size):
#     print(f"Index_{i}:Harif_{text[i]}")

"""MISOL 13"""

"""MISOL 14"""
# text="Python"
# size=len(text)
# for i in range(0,size):
#     print(text[i].upper())

"""MISOL 15"""
# num = input("son kiriting;").split()
# res= int(num[0])
# for i in range(0,len(num)):
#     if int(num[i])>res:
#         res=int(num[i])
#
# print("Eng katta son:",res)

"""MISOL 16"""
# text = "Python"
# for i in range(0,len(text)):
#     if text[i]==text[i].upper():
#         print(text[i],end=",")

""" MISOL 17"""
# text="python"
# for i in range(len(text)-1,-1,-1):
#     print(text[i],end="")

"""MISOL 18"""

"""MISO 19"""
# text = "python"
# for i in range(0,len(text)):
#     print(ord(text[i]),end=",")

"""MISOL 20"""
# text = input("Son kiriting:").split()
# for i in range(0,len(text)):
#     if int(text[i])>0:
#         print(text[i],end=",")

"""------------------MEDIUM------------------"""
"""MSIOL 1"""
# text = input("10 ta son kiriting:").split()
# print("juft sonlar:")
# for i in range(0,len(text)):
#     if int(text[i])%2==0:
#         print(text[i])

"""MISOL 2"""
# text = "Salom,Python"
# res=0
# for i in range(0,len(text)):
#     if text[i].isalpha():
#          res+=1
#
# print("hariflar soni:",res)

"""MISOL 3"""
# for i in range(1,101):
#     if i%3==0 and i%5==0:
#         print(i,end=",")

"""MISOL 4"""
# text = "Python"
# res=""
# for i in range(0,len(text)):
#     res+=text[i]+text[i]
#
# print(res)

"""-------------Hard---------------"""
"""---misol 1---"""
# for i in range(1,1001):
#     sanoq = 0
#     for j in range(1,1001):
#         if i%j==0:
#             sanoq+=1
#     if sanoq==2:
#        print(i)

"""---misol 2---"""
# text=input("so'z kiriting:")
# for i in text:
#     print(ord(i),end=",")

"""---misol 3---"""
# num=[1,2,3,4,5,6,7,8]
# size=len(num)
# for i in range(size,0,-1):
#     print(i,end=",")

"""---misol 4---"""
# text=input("Matin kiriting:")
# res=""
# for i in range(len(text)):
#     if text[i]==' ':
#         res+=' '
#         continue
#     if i==0 or text[i-1]==' ':
#         res+=text[i].upper()
#     else:
#         res+=text[i]
#print(res)

"""---misol 5---"""
# import random
# text="Python"
# harf=list(text)
# res=''
# for i in text:
#     i=random.randint(0,len(harf)-1)
#     res+=harf[i]
#     harf.pop(i)
# print(res)

"""---misol 6---"""







"""---misol 7---"""
# text=input("Matin kiriting:")
# res=''
# for i in text:
#     if i.isdigit():
#         res+=i
# print(res)
"""---misol 8---"""
# meva1=["olma","anor","banan","ananas"]
# meva2=["orik","anor","hurma","olma"]
# meva3=[]
# for i in meva1:
#     if i in meva2:
#         meva3.append(i)
# print(meva3)
"""---misol 9---"""
# num=int(input("son kiriting:"))
# for i in range(1,num+1):
#     if str(i)==str(i)[::-1]:
#         print(i)

"""---misol 10---"""
# num=input("son kiriting:")
# num=num[::-1]
# print(num)

"""---misol 11---"""
# text=input("Matin kiriting:")
# res=""
# for i in text:
#     if i=='A' or i=='a' or i=='O' or i=='o' or i=='U' or i=='u' or i=='I' or i=='i' or i=='E' or i=='e':
#         continue
#     else:
#         res+=i
#
# print(res)

"""---misol 12---"""
# num=[156,564,598,600]
# num2=max(num)
# print(num2)

"""---misol 13---"""
# num=input("son kiriting:")
# res=0
# for i in num:
#     res+=int(i)
# print(f"sonlar yigindisi: {res}")

"""---misol 14---"""
# text="Python"
# res=''
# for i in text:
#     res+=i+i
#
# print(res)

"""---misol 15---"""







"""---misol 16---"""
# text=input("Matin kiriting:")
# sanoq=0
# for i in text:
#     if i==' ':
#         sanoq+=1
#
# print("Probelar soni: ",sanoq)
"""---misol 17---"""







"""---misol 18---"""
# import string
# text=input("Matin kiriting: ")
# belgi=[]
# for i in text:
#     if i in string.punctuation:
#         belgi+=i
# print(belgi)
"""---misol 19---"""
# res=0
# for i in range(1,101):
#     if i%2==0:
#         res+=i
#
# print(res)
"""---misol 20---"""
# matn=input("Matin kiriting: ").split()
# tartiblash=sorted(matn,key=len)
# print(tartiblash)

"""-----------------------------------------------------------------------"""
"""-----------------------------WHILE--------------------------------------------------"""
"""-----------------------------HARD---------------------------------------------------"""

"""---misol 1---"""
"""---misol 2---"""
"""---misol 3---"""
"""---misol 4---"""
"""---misol 5---"""
"""---misol 6---"""
"""---misol 7---"""
# i = 1
# while i <= 1000:
#     sanoq = 0
#     j = 1
#     while j <= 1000:
#         if i % j == 0:
#             sanoq += 1
#         j += 1
#     if sanoq == 2:
#         print(i)
#     i += 1
"""---misol 8---"""

"""---misol 9---"""
# kod=input("ASCII soni kiriting:").split()
# i=0
# while i<len(kod):
#     print(chr(int(kod[i])),end="")
#     i+=1
"""---misol 10---"""

"""---misol 11---"""
# text=input("Enter:")
# size=len(text)-1
# sanoq=0
# while size>=0:
#     if text[size]==text[size].upper():
#         sanoq+=1
#     size-=1
# print(sanoq)
"""---misol 12---"""
#ohiriga
"""---misol 13---"""
#bilmiman
"""---misol 14---"""
# text=input("Matin kiriting:")
# print(text[::-1])
"""---misol 15---"""


"""---misol 16---"""
# a = int(input("Birinchi sonni kiriting: "))
# b = int(input("Ikkinchi sonni kiriting: "))
#
# while b != 0:
#     a, b = b, a % b
#
# print("EKUB =", a)
"""---misol 17---"""
# while True:
#     text=input("Matin kiriting:")
#     if "exit" in text:
#         break
"""---misol 18---"""
# text=input("Matin kiriting:")
# res=text.upper()
# print(res)
"""---misol 19---"""
# text= input("Matin kiriting:")
# size=len(text)-1
# res=""
# while size>=0:
#     res+=text[size]
#     size-=1
#
# print(res)
"""---misol 20---"""
# son=int(input("son kiriting:"))
# new=bin(son)[2:]
# print (f"{new}")






