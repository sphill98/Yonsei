"""
This code use selenium and PhantomJS.
You have to install PhantomJS on following link.
http://phantomjs.org/download.html
"""

import json
import re

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from constants import IGNORE_YEAR, IGNORE_SEMESTER


def crawl():
    driver = webdriver.PhantomJS()
    driver.get("http://ysweb.yonsei.ac.kr:8888/curri120601/curri_new.jsp#top")

    year = Select(driver.find_element_by_id('HY'))
    semester = Select(driver.find_element_by_id('HG'))
    college = Select(driver.find_element_by_id('OCODE1'))
    department = Select(driver.find_element_by_id('S2'))

    for y in reversed(list(filter(lambda y: y.text not in IGNORE_YEAR, year.options))):
        year.select_by_visible_text(y.text)
        semester = Select(driver.find_element_by_id('HG'))
        for s in reversed(list(filter(lambda s: (y.text, s.text) not in IGNORE_SEMESTER, semester.options))):
            semester.select_by_visible_text(s.text)
            college = Select(driver.find_element_by_id('OCODE1'))

            meta_data = {
                'cnt_of_subject': 0,
            }
            data = list()
            for c in college.options:
                college.select_by_visible_text(c.text)
                department = Select(driver.find_element_by_id('S2'))
                for d in department.options:
                    print('|'.join([y.text, s.text, c.text, d.text]))
                    meta_data_key = '_'.join(['cnt', c.text, d.text])
                    meta_data[meta_data_key] = 0
                    department.select_by_visible_text(d.text)
                    driver.execute_script("searchGb('search',1);")

                    wait = WebDriverWait(driver, 3)
                    wait.until(EC.visibility_of_all_elements_located(
                        (By.ID, "row0jqxgrid")))

                    while True:
                        for i in range(15):
                            row_id = 'row' + str(i) + 'jqxgrid'
                            row = driver.find_element_by_id(row_id)
                            cells = row.find_elements_by_css_selector(
                                '.jqx-grid-cell')

                            empty_cell_cnt = 0
                            no_data = False
                            row_data = [
                                y.text,
                                s.text,
                                c.text,
                                d.text
                            ]
                            for cell in cells:
                                if not cell or not cell.text:
                                    empty_cell_cnt += 1
                                if 'No data to display' in cell.text:
                                    no_data = True
                                row_data.append(cell.text.strip())
                            if empty_cell_cnt >= 18 or no_data:
                                break
                            meta_data['cnt_of_subject'] += 1
                            meta_data[meta_data_key] += 1
                            data.append(row_data)

                        pager = driver.find_element_by_id("pager")
                        state = re.findall('\d+', pager.text)
                        if state[1] == state[2]:
                            break

                        buttons = driver.find_elements_by_css_selector(
                            '.jqx-button')
                        try:
                            buttons[1].click()
                        except StaleElementReferenceException:
                            break

                    print('all_cnt: ', meta_data['cnt_of_subject'],
                          'current_department: ', meta_data[meta_data_key])

            with open('yonsei_lecture-' + y.text + '-' + s.text + '.json', 'w') as outfile:
                json.dump({'metadata': meta_data, 'data': data}, outfile)


def post_process(y, s):
    json_data = []
    new_data = []
    infile_path = 'yonsei_lecture-' + str(y) + '-' + str(s) + '.json'
    outfile_path = 'yonsei_lecture-' + str(y) + '-' + str(s) + '_fixed.json'

    with open(infile_path, 'r') as infile:
        json_data = json.load(infile)

    for row_data in json_data:
        empty_cell_cnt = 0
        for cell_data in row_data:
            if not cell_data:
                empty_cell_cnt += 1
        if empty_cell_cnt >= 18:
            continue
        new_data.append(row_data)

    with open(outfile_path, 'w') as outfile:
        json.dump(new_data, outfile)


crawl()
