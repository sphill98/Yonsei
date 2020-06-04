
# -*- coding: utf-8 -*-

import json

import requests
from bs4 import BeautifulSoup

''' all data is string '''
''' if you don't want to save string, you have to change code '''


class Subject():
    def __init__(self, hyhg, domain, hakno, bb, sbb):
        self.hyhg = hyhg
        self.domain = domain
        self.hakno = hakno
        self.bb = bb
        self.sbb = sbb
        self.person_list = []

    '''' Ex) major_info : 0 (N)    major maximum(2-major include) '''

    def set_info(self, name, credit, professor, time, place, maximum, applied_num, major_info, maximum1, maximum2,
                 maximum3, maximum4, exchange_possible):
        self.name = name
        self.credit = credit
        self.professor = professor
        self.time = time
        self.place = place
        self.maximum = maximum
        self.applied_num = applied_num
        self.major_info = major_info
        self.maximum1 = maximum1
        self.maximum2 = maximum2
        self.maximum3 = maximum3
        self.maximum4 = maximum4
        self.sechange_possible = exchange_possible

    def add_person(self, rank, mileage, major, num_subject, graduate, first_apply, option1, option2, grade, success):
        self.person_list.append(
            Person(rank, mileage, major, num_subject, graduate, first_apply, option1, option2, grade, success))
        return


class Person():
    ''' Ex) major : N (N)    major or multi major '''
    '''                       (this subject has fixed major student) '''
    ''' option1 : 총 이수 학점 / 졸업 이수 학점 '''
    ''' option2 : 직전학기 이수학점 / 학기당 수강학점 '''

    def __init__(self, rank, mileage, major, num_subject, graduate, first_apply, option1, option2, grade, success):
        self.rank = rank
        self.mileage = mileage
        self.major = major
        self.num_subject = num_subject
        self.graduate = graduate
        self.first_apply = first_apply
        self.option1 = option1
        self.option2 = option2
        self.grade = grade
        self.success = success


def mileage_crawl_2015_2(hyhg, domain, hakno, bb, sbb):
    subject = Subject(hyhg, domain, hakno, bb, sbb)

    url = 'http://ysweb.yonsei.ac.kr:8888/curri120601/curri_pop_mileage_20152.jsp'
    data = {'yshs_hyhg': hyhg,
            'yshs_domain': domain,
            'yshs_hakno': hakno,
            'yshs_bb': bb,
            'yshs_sbb': sbb}

    req = requests.post(url, data=data)

    ''' if cannot find all list, switch to html.parser '''
    ''' = BeautifulSoup(req.text, "html.parser") '''

    soup = BeautifulSoup(req.text, 'lxml')

    table_list = soup.find_all('table')

    try:
        subject_info = table_list[1].find_all('tr')[3].find_all('td')
        subject.set_info(subject_info[1].text,
                         subject_info[2].text,
                         subject_info[3].text,
                         subject_info[4].text,
                         subject_info[5].text,
                         subject_info[6].text,
                         subject_info[7].text,
                         subject_info[8].text,
                         subject_info[9].text,
                         subject_info[10].text,
                         subject_info[11].text,
                         subject_info[12].text,
                         subject_info[13].text)
        person_info = table_list[2].find_all('tr')[2:]

        for person_iter in person_info:
            info = person_iter.find_all('td')
            subject.add_person(info[0].text,
                               info[1].text,
                               info[2].text,
                               info[3].text,
                               info[4].text,
                               info[5].text,
                               info[6].text,
                               info[7].text,
                               info[8].text,
                               info[9].text)

        return subject
    except IndexError as e:
        ''' this subject do not have mileage info '''
        return -1


def mileage_crawl_2016_1_to_2017_2(hyhg, domain, hakno, bb, sbb):
    subject = Subject(hyhg, domain, hakno, bb, sbb)

    url = 'http://ysweb.yonsei.ac.kr:8888/curri120601/curri_pop_mileage_result01.jsp'
    data = {'yshs_hyhg': hyhg,
            'yshs_domain': domain,
            'yshs_hakno': hakno,
            'yshs_bb': bb,
            'yshs_sbb': sbb}

    req = requests.post(url, data=data)

    ''' if lxml cannot find all list, switch to html.parser '''
    ''' soup = BeautifulSoup(req.text, 'html.parser') '''
    soup = BeautifulSoup(req.text, 'lxml')

    table_list = soup.find_all('table')

    try:
        subject_info = table_list[1].find_all('tr')[3].find_all('td')
        subject.set_info(subject_info[1].text,
                         subject_info[2].text,
                         subject_info[3].text,
                         subject_info[4].text,
                         subject_info[5].text,
                         subject_info[6].text,
                         subject_info[7].text,
                         subject_info[8].text,
                         subject_info[9].text,
                         subject_info[10].text,
                         subject_info[11].text,
                         subject_info[12].text,
                         subject_info[13].text)

        person_info = table_list[2].find_all('tr')[2:]

        for person_iter in person_info:
            info = person_iter.find_all('td')
            subject.add_person(info[0].text,
                               info[1].text,
                               info[2].text,
                               info[3].text,
                               info[4].text,
                               info[5].text,
                               info[6].text,
                               info[7].text,
                               info[8].text,
                               info[9].text)
        return subject
    except IndexError as e:
        ''' this subject do not have mileage info '''
        return -1


def make_output(ys, input_name, output_name, func):
    ''' file read '''
    ''' need year, semester, domain(?), hakno, bb, sbb '''
    with open(input_name, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        data = json_data['data']

        result = []
        for iter_data in data:
            print(iter_data)
            if iter_data[8] == 'No data to display':
                continue
            if iter_data[10] == 'TEST000-01-00':
                continue
            iter_data[10] = iter_data[10].strip()

            domain = "H1"
            hak = iter_data[10].split('-')
            hakno = hak[0]
            bb = hak[1]
            sbb = hak[2][:2]

            subject = []
            subject.append(func(ys, domain, hakno, bb, sbb))

            for sub in subject:
                if sub == -1:
                    print(iter_data)
                    print(iter_data[12] + 'do not have mileage data')
                    continue
                iter_data[0] = sub.hyhg[:4]
                iter_data[1] = sub.hyhg[-1] + '학기'
                iter_data[17] = sub.professor
                iter_data[18] = sub.time
                iter_data[19] = sub.place

                mileage_list = []
                for per in sub.person_list:
                    mileage_list.append(
                        [per.rank, per.mileage, per.major, per.num_subject, per.graduate, per.first_apply, per.option1,
                         per.option2, per.grade, per.success])
                iter_data.append(mileage_list)

                iter_data.append(sub.maximum)
                iter_data.append(sub.applied_num)
                iter_data.append(sub.major_info)
                iter_data.append(sub.maximum1)
                iter_data.append(sub.maximum2)
                iter_data.append(sub.maximum3)
                iter_data.append(sub.maximum4)
            result.append(iter_data)

        with open(output_name, 'w', encoding='utf-8') as output_file:
            json.dump(result, output_file, ensure_ascii=False)


if __name__ == "__main__":
    # make_output('20152', 'yonsei_lecture-2015-2학기.json', 'yonsei_mileage-2015-2학기.json', mileage_crawl_2015_2)
    # make_output('20161', 'yonsei_lecture-2016-1학기.json', 'yonsei_mileage-2016-1학기.json', mileage_crawl_2016_1_to_2017_2)
    # make_output('20162', 'yonsei_lecture-2016-2학기.json', 'yonsei_mileage-2016-2학기.json', mileage_crawl_2016_1_to_2017_2)
    # make_output('20171', 'yonsei_lecture-2017-1학기.json', 'yonsei_mileage-2017-1학기.json', mileage_crawl_2016_1_to_2017_2)
    # make_output('20172', 'yonsei_lecture-2017-2학기.json', 'yonsei_mileage-2017-2학기.json', mileage_crawl_2016_1_to_2017_2)
    make_output('20181', 'yonsei_lecture-2018-1학기.json', 'yonsei_mileage-2018-1학기.json', mileage_crawl_2016_1_to_2017_2)
