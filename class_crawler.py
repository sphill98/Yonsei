# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:01:16 2020

@author: sphil
"""

'''
수강편람을 크롤링하는 코드입니다.
실행 후 본인의 전공코드 알파벳 세글자(모두 대문자), 학년도, 학기를 차례로 입력하면 됩니다.
'''

import re
import requests
from bs4 import BeautifulSoup

major = input("Enter your major code : ")
yr = input("Enter this year: ")
sem = input("Enter your semester : ")
curr_lst = []
banned_word = ['찾기', '학년도', '학기', '글로벌인재대학', '글로벌인재학부', '사회학',
               '이과대학', '사회과학대학', '행정학','수학', '상대','절대',
               '커뮤니케이션대학원','화학','사학', '문과대학','중어중문학','영어영문학','대기과학과', '경제학부', '물리학','경영대학','경영학과', '경제학과', '상경대학'] #결과가 이상하다면 여기에 이상한 단어를 추가하면 됩니다.
f = open(major+".txt", 'w')

for hakno in range(2000,4999): #여기는 학정번호를 입력하시면 됩니다. 범위를 입력하면 됩니다. 2000부터 4899까지 찾고 싶다면 2000,4900
    for bb in range(1,3): #여기는 분반번호를 입력하시면 됩니다. 마찬가지로 범위를 입력하면 됩니다. 2분반까지 있다면 1,3
        class_lst = []
        url = "http://ysweb.yonsei.ac.kr:8888/curri120601/curri_pop2.jsp?&hakno="+major+str(hakno)+"&bb=0"+str(bb)+"&sbb=00&domain=H1&startyy="+yr+"&hakgi="+sem+"&ohak=0301"
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        td_class = soup.find_all('td')
        for s in td_class:
            s_str = str(s)
            lst1=re.compile('[가-힣]+').findall(s_str)
            lst2=re.compile('[A-Z]?[A-Z]?[(]?[가-힣]+[-]?[A-Z]?[(]?[0-9][,]?[0-9]?[0-9]?[,]?[0-9]?[0-9]?[)]?').findall(s_str)
            if len(lst1)==0 and len(lst2)==0:
                class_lst = class_lst
            elif len(lst1)!=0:
                if len(lst1)==len(lst2):
                    time = ""
                    for i in range(len(lst2)):
                        if i == 0:
                            time = time+lst2[i]
                        else:
                            time = time+','+lst2[i]
                    class_lst.append(time)
                else:
                    for bw in lst1:
                        if bw not in banned_word:
                            class_lst.append(bw)
        if len(class_lst) != 0:
            f.write(str(hakno))
            for i in class_lst:
                f.write(i+" ")
            f.write("\n")
f.close()
