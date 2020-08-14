import xml.etree.ElementTree as elemTree
import re

"""
GRAD_DIV_NM:    대학 구분
TERM_DIV:       학기
CORS_DIV:       과목 구분 코드(로 추정)
LAB_HR:         실습 시간
DEPT_CD:        대상학부 구분 코드(로 추정됨)
CREDIT:         학점
SCH_YR:         대상 학년
LECT_DIV:       강의 구분 코드
CORS_NM:        과목 이름
PROF_NM:        교수 이름
PROF_ID:        교수 코드
DEPT_NM:        대상 학부
THE_HR:         강의 시간
SYL_YN:         이러닝 여부(로 추정됨)
LECT_DIV_NM:    강의 구분
CLS_CNT:        수강 정원
CORS_CD:        과목 코드
CLS_NO:         분반
LECT_NO:        강의 코드
CORS_DIV_NM:    이수구분
CLS_HR:         시수
LECT_CNT:       수강 인원
DN_DIV_NM:      주간/야간(으로 추정됨)
LECT_RM:        강의실
LECT_TM:        강의시간
GRAD_DIV:       대학 구분 코드
YR:             년도
"""

DEFINED_ID = {
    "YEAR": "YR",
    "graduation_col": "GRAD_DIV_NM",  # 학부 필터링을 위함
    "prefessor_col": "PROF_NH",
    # 10: 1학기 11: 여름학기 20: 2학기 21: 겨울학기
    "semestor_col": "TERM_DIV",
    "code_col": "CORS_CD",
    "name_col": "CORS_NM",
    "grades_col": "CREDIT",
    "class_number_col": "CLS_NO",
    "professor_col": "PROF_NM",
    "regular_number_col": "CLS_CNT",
    "department_col": "DEPT_NM",
    "target_col": "SCH_YR",
    "class_time_col": "LECT_TM",
}

WEEK_NUMBER = {"월": 1, "화": 2, "수": 3, "목": 4, "금": 5, "토": 6, "일": 7}


def course_parser(xml_data):
    course_array = []
    xml_tree = elemTree.fromstring(xml_data)
    xml_root_regex = r"^{(.+)}Root"
    xml_namespace = '{' + re.findall(xml_root_regex, xml_tree.tag)[0] + '}'
    rows = xml_tree.iterfind(f'.//{xml_namespace}Row')
    class_time_regex = r"([월화수목금토일])(\d{2}[AB])~(\d{2}[AB])"
    for row in rows:
        parsed_class_time = []
        class_time_element = row.find(f'.//{xml_namespace}Col[@id="{DEFINED_ID["class_time_col"]}"]')
        class_time = class_time_element.text if class_time_element is not None else ''
        for time in re.finditer(class_time_regex, class_time):
            find_result = time.groups()
            time_array = list(range(
                int(find_result[1][0:2]) * 2 + (0 if find_result[1][2] == 'A' else 1),
                int(find_result[2][0:2]) * 2 + (0 if find_result[2][2] == 'A' else 1) + 1))
            for index in range(len(time_array)):
                time_array[index] = WEEK_NUMBER[find_result[0]] * 100 + time_array[index]
            parsed_class_time = parsed_class_time + time_array
        graduation = row.find(f'.//*[@id="{DEFINED_ID["graduation_col"]}"]')
        if graduation.text != "학부":
            continue
        department = row.find(f'.//*[@id="{DEFINED_ID["department_col"]}"]')
        if department.text in ["강소기업경영학과", "기계설계공학과", "기전융합공학과"]:
            continue
        name = row.find(f'.//*[@id="{DEFINED_ID["name_col"]}"]')
        code = row.find(f'.//*[@id="{DEFINED_ID["code_col"]}"]')
        grades = row.find(f'.//*[@id="{DEFINED_ID["grades_col"]}"]')
        class_number = row.find(f'.//*[@id="{DEFINED_ID["class_number_col"]}"]')
        professor = row.find(f'.//*[@id="{DEFINED_ID["professor_col"]}"]')
        regular_number = row.find(f'.//*[@id="{DEFINED_ID["regular_number_col"]}"]')
        target = row.find(f'.//*[@id="{DEFINED_ID["target_col"]}"]')
        course = {
            "name": name.text,
            "code": code.text,
            "grades": grades.text,
            "class_number": class_number.text,
            "professor": professor.text if professor else None,
            "regular_number": regular_number.text if regular_number else None,
            "department": department.text,
            "target": target.text if target else '0',
            "class_time": parsed_class_time
        }
        print(course)
        course_array.append(course)
    return course_array
