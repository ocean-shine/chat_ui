from flask import Flask, request, jsonify
from flask_cors import CORS
import SparkApi
import os
import threading
import time
import re

app = Flask(__name__)
CORS(app)

# 配置环境变量
os.environ["IFLYTEK_SPARK_URL"] = "wss://xingchen-api.cn-huabei-1.xf-yun.com/v1.1/chat"
os.environ["IFLYTEK_SPARK_APP_ID"] = "fb05eb34"
os.environ["IFLYTEK_SPARK_API_KEY"] = "75ddd2e19d262c0db0c4daf62b9b21c0"
os.environ["IFLYTEK_SPARK_API_SECRET"] = "NzhkOTc0ZWFiYmZlN2I2YzA0MWYwM2Zm"

# 用于配置大模型版本，默认“general/generalv2”
domain = "xspark13b6k"  # v2.0版本
appid = os.getenv("IFLYTEK_SPARK_APP_ID")
api_secret = os.getenv("IFLYTEK_SPARK_API_SECRET")
api_key = os.getenv("IFLYTEK_SPARK_API_KEY")
Spark_url = os.getenv("IFLYTEK_SPARK_URL")

text = []

def getText(role, content):
    jsoncon = {"role": role, "content": content}
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        length += len(content["content"])
    return length

def checklen(text):
    while getlength(text) > 8000:
        del text[0]
    return text

stored_question = ""
stored_answer = ""

@app.route('/chat', methods=['POST'])
def chat():
    global stored_question, stored_answer
    data = request.get_json()
    stored_question = data.get('message')
    
    # 等待答案生成
    while not stored_answer:
        time.sleep(0.1)
    
    response = stored_answer
    stored_answer = ""  # 重置答案
    return jsonify({'answer': response})

def process_questions(stored_question, stored_answer, loop=True):
    # global stored_question, stored_answer
    while True:
        if stored_question:
            prompt = ("？。 上面输入的问题属于下面ABCDE的哪一类，请输出对应的字母。\n"
                      "A: 查询企业的所属城市、营业期限、成立日期、纳税人识别号、法定代表人人、实缴资本、所属行业、匹配状态、所属城市等等一系列和企业信息有关的问题。\n"
                      "B: 招投标中的政策、法律咨询相关问题。包括招标投标的一般规定、招标范围、招标程序、监督处理、领域规范。还有政府采购的一般规定、采购主体、政策功能、采购方式等相关问题。\n"
                      "C: 企业舆情问题,企业舆情通常涉及企业的声誉、市场表现、管理层变动、重大合作、法律纠纷等方面。\n"
                      "D: 查询招标信息。\n"
                      "E: 其他 例如:日常生活中常见的问题，通用的问题，不符合招投标领域的。\n")
            
            Input = stored_question + prompt
            stored_answer = ""
            question = checklen(getText("user", Input))
            SparkApi.answer = ""
            print(stored_question)
            print("星火:", end="")
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
            getText("assistant", SparkApi.answer)
            output = text

            # 提取 'assistant' 的 content 值，并只保留第一个字符
            # assistant_content = next((item['content'] for item in output if item['role'] == 'assistant'), "")
            # stored_answer = assistant_content[0] if assistant_content else ""
            match = re.search(r'[ABCDE]', SparkApi.answer)
            stored_answer = match.group(0) if match else ""
            if stored_answer == "E":
                stored_answer = (" 你的问题描述不够准确，请记得添加关键词。输入的问题应该属于下面ABCD的一类。\n"
                      "A: 查询企业信息。例如:查询企业的所属城市、营业期限、成立日期、纳税人识别号、法定代表人人、实缴资本、所属行业、匹配状态、所属城市等等一系列和企业信息有关的问题。\n"
                      "B: 招投标中的政策、法律咨询相关问题。包括招标投标的一般规定、招标范围、招标程序、监督处理、领域规范。还有政府采购的一般规定、采购主体、政策功能、采购方式等相关问题。\n"
                      "C: 企业舆情问题。\n"
                      "D: 查询招标信息。\n")
            stored_question = ""  # Reset the question after processing
        if loop == False:
            return stored_answer
            break
        time.sleep(1)  # Add a small delay to prevent busy-waiting

if __name__ == '__main__':
    threading.Thread(target=process_questions(stored_question, stored_answer), daemon=True).start()
    app.run(debug=True)
