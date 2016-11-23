import re

def clean_parenthesis(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

def clean_space_after_points(text):
    result_point = re.sub(r'\.([a-zA-Z])', r'. \1', text)
    result_two_points = re.sub(r'\:([a-zA-Z])', r': \1', result_point)
    return result_two_points