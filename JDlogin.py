#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 07/08/18 15:33
# @Author  : Liu Hao Dong
# @Site    : 
# @File    : JDlogin.py
# @Software: PyCharm
import time

login_type = False

# def get_info(filename,username,userpw):
#   with open(filename,'r') as file:
#     info = file.readlines()
#
#     for i in info:
#       dict_info  = eval(i)
#
#       if dict_info['username'] == username and dict_info['passwd'] == userpw:
#         print("正在验证....\n")
#         time.sleep(2)
#         print("欢饮您，%s\n"%username)
#         return 1
#       else:
#         print("用户名或密码错误，请重试\n")
#     else:
#       print("输入的用户名不存在，请注册。\n")
#     return 0
def weixinlogin():
  print("请用微信扫码登录:\n")
  time.sleep(2)
  print("正在验证。。。\n")
  time.sleep(2)
  print("登陆成功\n")


def get_info(filename):
  '''

  :param filename:
  :return: 如果通过了验证就返回１,没有通过j就返回0hhl087,,bj
  '''
  with open(filename,'r') as file:
    info = file.readlines()
    count = 0
    while count<3:
      count += 1
      username = input('请输入用户名\n')
      userpw = input('请输入密码\n')
      for i in info:
        dict_info  = eval(i)
        if dict_info['username'] == username and dict_info['passwd'] == userpw:
          print("正在验证....\n")
          time.sleep(2)
          print("欢饮您，%s\n"%username)
          return 1
      else:
        print("输入的用户名或密码错误。\n")  # 如果找不到用户名和密码，就从这走
  return 0


def login(auth_type):
  # 所有带参数的装饰器，都得用三层来写，
  # 最里面那层做运行处理，倒数第二层接受@后面的函数，
  # 最外层接受参数

  def goin(func):
    def innner():
      global login_type  # 在局部空间里使用全局变量，要先
                         # 在局部空间里面申明一下全局变量，global
      if not login_type:
        if auth_type == 'weixin':
          weixinlogin()
          login_type = True
          func()
        elif auth_type == 'JD':

          flag = get_info('info')
          if flag == 1:
            func()
            login_type = True
          else:
            print("用户名输入次数过多，请稍后输入\n")
        else:
          print("该网页没有指定登录形式\n")

      else:
        func()
    return innner
  return goin

# def login(auth_type):
#
#   def goin(func):
#     def innner():
#       global login_type
#       if not login_type:
#         if auth_type == 'weixin':
#           print("请用微信扫码登录:\n")
#           time.sleep(2)
#           print("正在验证。。。\n")
#           time.sleep(2)
#           print("登陆成功\n")
#           login_type = True
#           func()
#         elif auth_type == 'JD':
#           count = 0
#           while count < 3:
#             count += 1
#             username = str(input('请输入用户名\n'))
#             userpw = str(input('请输入密码\n'))
#             flag = get_info('info',username,userpw)
#             if flag == 1:
#               func()
#               login_type = True
#               break
#             else:
#             print('输入次数已达上限，请稍后重试\n')
#         else:
#           print("该网页没有指定登录形式\n")
#
#       else:
#         func()
#     return innner
#   return goin


@login('weixin')
def home():
  print("欢迎来到首页\n")

@login('JD')
def finance():
  print("欢迎来到京东金融。\n")

@login('JD')
def book():
  print("欢迎来到京东书城\n")



if __name__ == '__main__':


  for i in range(100):
    choose = input('请选择您要访问的页面：1.home 2.finance 3.book\n')
    if choose == '1':
      home()
    elif choose == '2':
      finance()
    elif choose == '3':
      book()
    else:
      print("请在1,2,3中选择\n")

