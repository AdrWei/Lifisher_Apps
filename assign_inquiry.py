import os
import json
import requests
from datetime import datetime
import random

# 从环境变量中加载配置
LIFISHER_CODES = json.loads(os.getenv("LIFISHER_CODES"))
LIFISHER_TOKEN = json.loads(os.getenv("LIFISHER_TOKEN"))
LIFISHER_VARIABLES = json.loads(os.getenv("LIFISHER_VARIABLES"))
LIFISHER_STAFF_CODES = json.loads(os.getenv("LIFISHER_STAFF_CODES"))

# 提取配置值
USERNAME = LIFISHER_CODES["USERNAME"]
PASSWORD = LIFISHER_CODES["PASSWORD"]
APPKEY = LIFISHER_CODES["APPKEY"]

# 重组 TOKEN
TOKEN = "".join([LIFISHER_TOKEN["Token_1"], LIFISHER_TOKEN["Token_2"], LIFISHER_TOKEN["Token_3"], LIFISHER_TOKEN["Token_4"]])

# 常量定义
LOGIN_URL = LIFISHER_VARIABLES["LOGIN_URL"]
INQUIRY_LIST_URL = LIFISHER_VARIABLES["INQUIRY_LIST_URL"]
ASSIGN_URL = LIFISHER_VARIABLES["ASSIGN_URL"]
DOMAIN = LIFISHER_VARIABLES["DOMAIN"]
REFERER = LIFISHER_VARIABLES["REFERER"]
SITE_ID = LIFISHER_VARIABLES["SITE_ID"]

# 1. 登录平台，获取 token 和 cookies
def login():
    response = requests.post(
        LOGIN_URL,
        json={"username": USERNAME, "password": PASSWORD},
        headers={"User-Agent": "Mozilla/5.0"},
        verify=False
    )
    response.raise_for_status()
    return response.json()["token"], response.cookies

# 2. 获取最新询盘列表
def get_inquiry_list(token, cookies):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "appkey": APPKEY,
        "token": token,
        "domain": DOMAIN,
        "Referer": REFERER,
        "timestamp": str(int(datetime.now().timestamp() * 1000)),
        "X-Trace-Id": "bb898ceed2b5f5e4"
    }
    params = {
        "return_source": 1,
        "is_junk": 0,
        "site_id": SITE_ID,
        "page_size": 200,
        "page_number": 1,
        "status": 0,
        "sort": "create_time desc"
    }
    response = requests.get(
        INQUIRY_LIST_URL,
        headers=headers,
        params=params,
        cookies=cookies,
        verify=False
    )
    response.raise_for_status()
    return response.json()["data"]["list"]

# 3. 分配询盘
def assign_inquiries(inquiry_list, token, cookies):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "appkey": APPKEY,
        "token": token,
        "domain": DOMAIN,
        "Referer": REFERER,
        "timestamp": str(int(datetime.now().timestamp() * 1000)),
        "X-Trace-Id": "bb898ceed2b5f5e4"
    }
    for inquiry in inquiry_list:
        assign_to = random.choice(LIFISHER_STAFF_CODES)
        body = {
            "id": inquiry["id"],
            "client_account_id": assign_to,
            "site_id": SITE_ID
        }
        response = requests.post(
            ASSIGN_URL,
            headers=headers,
            json=body,
            cookies=cookies,
            verify=False
        )
        response.raise_for_status()

# 主函数
def main():
    try:
        # 登录
        token, cookies = login()
        
        # 获取询盘列表
        inquiry_list = get_inquiry_list(token, cookies)
        print("获取的询盘列表：", inquiry_list)
        
        # 分配询盘
        assign_inquiries(inquiry_list, token, cookies)
        print("询盘分配完成！")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    main()
