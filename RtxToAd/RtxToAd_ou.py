#!/usr/bin/env python
#coding:utf-8

import os
import sys
import base64
import xml.etree.ElementTree as ET


tree = ET.parse(r'D:\pycharm\read.xml')

root = tree.getroot()


#find the item to list
item = root.find('Database').find('Sys_User').findall('Item')
UserDetail = root.find('Database').find('RTX_UserDetail').findall('Item')
dept = root.find('Database').find('RTX_Dept').findall('Item')
deptuser = root.find('Database').find('RTX_DeptUser').findall('Item')


#create a empty list to save the users' info
userlist = []
#create tmp list to save the users' tmp info
itemlist = []
userdelist = []
#创建临时list，用来存储部门信息
deptlist = []
deptidlist = []
#创建临时list，用来存储部门用户信息
deptuserlist = []
firstoulist = []
oudelist = []
oudeljlist = []
userzjlist = []


#通过遍历列表，取出etree对象的属性，并存储为list
for itemlisttmp in item:
    itemlist.append(itemlisttmp.attrib)

for userdelisttmp in UserDetail:
    userdelist.append(userdelisttmp.attrib)
    
#通过遍历列表，取出etree对象的属性，存储到list，用来创建ou
for deptlisttmp in dept:
    deptlist.append(deptlisttmp.attrib)
    
for deptuserlisttmp in deptuser:
    deptuserlist.append(deptuserlisttmp.attrib)
    
#遍历list，取出上面存储的dic，并根据dic的key进行字典合并，最后存储到userlist。  
for itemdic in itemlist:
    for userdedic in userdelist:
        if itemdic.get('ID') == userdedic.get('ID'):
            dictuser = dict(itemdic.items() + userdedic.items())
            userlist.append(dictuser)

#先把一级ou写进list
for dept in deptlist:
    if dept.get('PDeptID') == '0':
        deptname = dept.get('DeptName')
        deptid = dept.get('DeptID')
        base64dept = 'ou='+deptname+',dc=boqii-inc,dc=com'
        firstoulist.append({'DeptID':deptid,'ou':deptname,'dn':base64dept})

#创建一个字典，并把部门的id作为key，然后部门信息作为values
temp = {}
for v in deptlist:
    #print v.get('DeptID')
    temp[v.get('DeptID')] = v   
 
def GetParentList(deptId):
#定义一个空列表
    deptList = []
    i = 20
    #把部门id赋值给tDeptId
    tDeptId = deptId
    while i>0:
        i-=1
        #根据部门id获取到部门的信息
        deptInfo = temp.get(tDeptId)
        if deptInfo is None:
            break
        deptList.append(deptInfo.get('DeptName'))
        tDeptId = deptInfo.get('PDeptID')
        if tDeptId is None:
            break
        if int(tDeptId)<=0:
            break
    return deptList

#temp4 = [v for v in deptlist if int(v.get('DeptID'))==0]
#遍历deptlist获取‘PDeptID’的值，然后存放为集合
deptParentIdList = set([int(v.get('PDeptID')) for v in deptlist])
#遍历deptilist获取DeptID不等于PDeptID的值，然后存放为列表
temp5 = [v for v in deptlist if int(v.get('DeptID')) not in deptParentIdList]
result = []
for v in temp5:
    result.append(GetParentList(v.get('DeptID')))
   
  

#result1 = ['dsadd ou %s,dc=boqii-inc,dc=com'%(','.join(['ou=%s'%(t,) for t in v]),) for v in result]
for v in result:
    v.reverse()
    t = []
    for a in v:
        t.append(a)
        t.reverse()
        print 'dsadd ou %s,dc=boqii-inc,dc=com'%(','.join(['ou=%s'%(x) for x in t]))
        t.reverse()



      
