from app import process_questions
import app

import os
import json
import time

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件的父目录
parent_directory = os.path.dirname(os.path.dirname(current_file_path))

test_a_path = f"{parent_directory}/variation/a.json"
test_b_path = f"{parent_directory}/variation/b.json"
test_c_path = f"{parent_directory}/variation/c.json"
test_d_path = f"{parent_directory}/variation/d.json"




with open(test_a_path, 'r') as f:
    a_lists = json.load(f)
with open(test_b_path, 'r') as f:
    b_lists = json.load(f)
with open(test_c_path, 'r') as f:
    c_lists = json.load(f)
with open(test_d_path, 'r') as f:
    d_lists = json.load(f)


def corrent_func(lists, char):
    sum = 0
    count =0
    stored_question = app.stored_question
    stored_answer = app.stored_answer
    for list in lists:
        stored_question = list[0]
        stored_answer = process_questions(stored_question, stored_answer, loop=False)
        time.sleep(2)
        if stored_answer == char:
            sum += 1
        count +=1
        print(f"{char}_corrent:", sum, "\n")
        print(f"{char}_count:", count, "\n")
        
    return sum

# sum_a = corrent_func(a_lists[:20], "A")
# time.sleep(30)
# sum_b = corrent_func(b_lists[:20], "B")
# time.sleep(30)
sum_c = corrent_func(c_lists[:20], "C")
# time.sleep(30)
# sum_d = corrent_func(d_lists[:20], "D")
# print(" correct number of class A questions --- %d ---  per 100 \n ", sum_a)
# print(" correct number of class B questions --- %d ---  per 100 \n ", sum_b)
print(" correct number of class C questions --- %d ---  per 100 \n ", sum_c)
# print(" correct number of class D questions --- %d ---  per 100 \n ", sum_d)

None

