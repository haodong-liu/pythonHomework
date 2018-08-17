#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 15/08/18 22:14
# @Author  : Liu Hao Dong
# @Site    :
# @File    : pythonCalculator.py
# @Software: PyCharm
"""
开发一个简单的python计算器

实现加减乘除及拓号优先级解析
用户输入 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )等类似公式后，
必须自己解析里面的(),+,-,*,/符号和公式(不能调用eval等类似功能偷懒实现)，运算后得出结果，
结果必须与真实的计算器所得出的结果一致
"""
import re

def calculate(cal_string):
  """
  调用该函数，在参数中传入要计算的计算式，就可以完成计算
  :param cal_string: 最初需要计算的表达式
  :return:
  """
  try:
    this_cal_string = cal_string
    
    while is_bracket_in(this_cal_string):
      this_cal_string = del_blank(this_cal_string)
      print('总计算式为',this_cal_string)
      
      calcul_unit, calable_unit = find_cal_unit(this_cal_string)
      print('当前的处理集合是{0}{1}'.format(calcul_unit,calable_unit))
      
      if len(calable_unit) == len(calcul_unit):
        for i in range(len(calcul_unit)):
          unit = calable_unit[i]
          result = calculate_a_unit(unit)
          this_cal_string = sub_cal_unit_to_num(result,calcul_unit[i],this_cal_string)
          
      else:
        print('处理出来的计算单元数不一致')
        return False

    else:
      return float(calculate_a_unit(this_cal_string))
  except Exception:
    print("""
    *****************
    崩溃啊啊啊啊啊啊
    请检查输入的符号是否有误
    *****************
    """)
def calculate_a_unit(unit):
  """
  该函数用于计算整个计算式中的每一个可计算单元，并返回该计算单元的结果
  :param unit: 这是一个字符串，里面可能很长
  :return: 返回一个处理单元的数字,以字符串格式
  """
  while all_num(unit):
    unit = del_blank(unit)
    print('计算式分项为', unit)
    if '*' in unit or '/' in unit:  # 如果字符串里有乘除，就处理乘除

      # 获取只有一个操作符的字符串
      ms_match_obj = re.search('(?P<first>(-\d+)|(\d+)|(\d+\.{1}\d+)|(-\d+\.{1}\d+))'
                               '(?P<operator>[*/])'
                               '(?P<second>(\d+\.{1}\d+)|(-\d+\.{1}\d+)|(-\d+)|(\d+))', unit)

      char_md_cal_unit = ms_match_obj.group()
      first_num = ms_match_obj.group('first')
      operator = ms_match_obj.group('operator')
      second_num = ms_match_obj.group('second')

      if '*' == operator:
        mul_result = float(first_num) * float(second_num)
        mul_result = is_operator(float(first_num),operator,float(second_num),mul_result)
        unit = sub_cal_unit_to_num(mul_result, char_md_cal_unit ,unit)
        print(first_num, operator, second_num, '=', mul_result)

      else:
        try:
          div_result = float(first_num) / float(second_num)
          div_result = is_operator(float(first_num), operator, float(second_num), div_result)
          unit = sub_cal_unit_to_num(div_result, char_md_cal_unit, unit)
          print(first_num, operator, second_num, '=', div_result)

        except ZeroDivisionError:
          print('除数不能为0')
          return False

    else:
      as_match_obj = re.search('(?P<first>(-\d+)|(\d+)|(\d+\.\d+)|(-\d+\.\d+))'
                               '(?P<operator>[+\-])'
                               '(?P<second>(\d+\.{1}\d+)|(-\d+\.{1}\d+)|(-\d+)|(\d+))', unit)

      char_as_cal_unit = as_match_obj.group()
      first_num = as_match_obj.group('first')
      operator = as_match_obj.group('operator')
      second_num = as_match_obj.group('second')

      if '+'  == operator:
        add_result = float(first_num) + float(second_num)
        unit = sub_cal_unit_to_num(add_result, char_as_cal_unit, unit)
        print(first_num, operator, second_num, '=', add_result)

      elif first_num != '-' and second_num != '-':
        sub_result = float(first_num) - float(second_num)
        unit = sub_cal_unit_to_num(sub_result, char_as_cal_unit, unit)
        print(first_num, operator, second_num, '=', sub_result)

  else:
    return unit

def all_num(cal_string):
  """
  如果是纯数字返回false，或者里面的-号只剩下一个，就返回False。用作while的终止条件
  如果还有计算符，返回True，让while继续处理
  :param cal_string:
  :return:
  """
  if not re.findall('[+\-*/()]',cal_string):
    return False

  else:
    if (not re.findall('.\+',cal_string) and not re.findall('.-',cal_string)) \
      and (cal_string.count('-') == 1 or cal_string.count('+') == 1) \
      and not re.findall('[*/()]',cal_string):
      return False
    else:
      return True

def sub_cal_unit_to_num(num, cal_unit, cal_string):
  return cal_string.replace(cal_unit,str(num))


def del_blank(cal_string):
  """
  将原式输入字符串中的空格去除，并处理里面存在的连续的操作符
  """
  new_cal_string = cal_string.replace(' ', '')
  new_cal_string = re.sub('--|\+\+', '+', new_cal_string)
  new_cal_string = re.sub('-\+|\+-', '-', new_cal_string)
  new_cal_string = re.sub('\*\+', '*', new_cal_string)
  new_cal_string = re.sub('/\+', '/', new_cal_string)
  return new_cal_string

def is_brackets_align(cal_string):
  """
  通过括号的数量，判断括号是否完全课匹配 同时不能出现')('这样的错误输入
  :param cal_string:
  :return:
  """
  left_brkt_num = cal_string.count('(')
  right_brkt_num = cal_string.count(')')
  if left_brkt_num != right_brkt_num or ')('  in cal_string:
    return False
  else:
    return True

def char_in_string(cal_string):
  """
  如果计算式里有其他字符，返回错误
  :param cal_string:
  :return:
  """
  if not re.findall('[^+\-*/()0-9]',cal_string):
    return False
  else:
    return True

def find_cal_unit(cal_string):
  """
  将匹配到的计算单元的括号去除，同时返回两个列表
  :param cal_string:
  :return: a list of calculable unit and a list of unit with brackets
  """
  calcul_unit = re.findall('\([^()]+\)', cal_string)
  calable_unit = [re.sub('[()]', '', unit) for unit in calcul_unit]
  return calcul_unit,calable_unit



def is_bracket_in(cal_string):
  """
  判断是否有口号在里面，并且判断是否括号数量匹配就返回
  :param cal_string:
  :return:
  """
  if ('(' in cal_string or ')' in cal_string) and is_brackets_align(cal_string):
    return True
  else:
    return False

def is_operator(first,operator,second, result):
  """
  解决两个负数，相除或者相乘，正号消失，造成计算结果和前面的数字连在一起的情况
  比如 9-10/-2  先计算了-10/-2 结果为5 ，若是直接替换，则原式变成 95 正确的应该是9+5
  该方法强制加上一个‘+’号，也会导致其他问题，将在del_blank函数中解决
  :param first: 第一个数字
  :param operator:  操作符
  :param second: 第二个数字
  :param result: 计算出来的结果
  :return: 字符串
  """
  if first<0 and second<0 and (operator == '*' or operator == '/'):
    return '+' + str(result)
  else:
    return result















