import os
import time

import requests
import json

basePath = "C:\\Users\\33051\\Desktop\\Lora"


def queryGenerateStatus(taskId: str):
    url = f"https://mjapi.ai-t.wtvdev.com/mj/task/{taskId}/fetch"

    # 定义请求头
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 发起GET请求
    response = requests.get(url, headers=headers)
    if response.status_code == 200:

        responseJson = json.loads(response.text)

        print(f"别急啊，你要是着急你退出啊：{responseJson['progress']}")

        if responseJson["finishTime"] is None:
            return False
        else:
            return True


# 使用提示词生成MJ的四合一图
def genRawImg(prompt: str, picName: str, indexOfAction: int):
    url = "https://mjapi.ai-t.wtvdev.com/mj/submit/imagine"
    # 定义请求头
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    # 定义请求数据
    data = {
        "base64Array": [],
        "notifyHook": "",
        "prompt": prompt,
        "state": ""
    }

    # 发起POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 打印响应内容
    # print(f'生初始图请求已经发送，提示词为{prompt},Status Code:', response.status_code)
    if response.status_code == 200:
        # print(f"文生图已经发起，直接发起时返回的结果为{response.text}")
        responseJson = json.loads(response.text)
        rawImgTaskID = responseJson['result']
        # print(f"文生图已经发起，raw图所使用的taskID是{rawImgTaskID}")
        # 等待绘图完成
        while True:
            print("别催了，在整了哥")
            if queryGenerateStatus(rawImgTaskID):
                break
            time.sleep(3)
        getTaskTargetImg(rawImgTaskID, 1, picName, indexOfAction)
        getTaskTargetImg(rawImgTaskID, 2, picName, indexOfAction)
        getTaskTargetImg(rawImgTaskID, 3, picName, indexOfAction)
        getTaskTargetImg(rawImgTaskID, 4, picName, indexOfAction)


# 获取某张4合1图指定的某一张
def getTaskTargetImg(taskId: str, imgIndexOfRaw: int, picName: str, indexOfAction: int):
    url = "https://mjapi.ai-t.wtvdev.com/mj/submit/simple-change"
    # 定义请求头
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    # 定义请求数据
    data = {
        "content": f"{taskId} U{imgIndexOfRaw}",
        "notifyHook": "",
        "state": ""
    }
    # 发起POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 打印响应内容
    print('文生图四张图的U1的参数 => Status Code:', json.dumps(data))
    print('查询文生图请求的状态结果 => Status Code:', response.text)
    print("我靠不耐烦了是吧，嫌我话多就退出啊")
    if response.status_code == 200:
        responseJson = json.loads(response.text)
        taskID = responseJson['result']
        # 等待U1完成
        while True:
            if queryGenerateStatus(taskID):
                break
            time.sleep(3)
        downloadTaskId(taskID, picName, indexOfAction, imgIndexOfRaw)


def downloadTaskId(taskId: str, picName: str, indexOfAction: int, imgIndexOfRaw: int):
    url = f"https://mjapi.ai-t.wtvdev.com/mj/task/{taskId}/fetch"

    # 定义请求头
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # 发起GET请求
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        responseJson = json.loads(response.text)
        ImgResponse = requests.get(responseJson['imageUrl'])
        # 检查请求是否成功
        if ImgResponse.status_code == 200:
            # 将图片保存到指定路径并命名为test.png
            with open(f'{basePath}\\{picName}_{imgIndexOfRaw}.png', 'wb') as file:
                file.write(ImgResponse.content)
            print("下载成功了，还愣着干嘛，快去文件夹选图")
        else:
            print(f"请求失败，状态码: {ImgResponse.status_code}")


if __name__ == "__main__":
    # 角色名称
    characterName = "A middle-aged ancient general with a black beard, black hair, and armor"
    # 角色外观特征描述
    characterDesc = ""
    # 画面风格
    style = ""
    # 动作集合
    actionArray = [
        "the prompt input here",
    ]
    # 图片链接及具体指令提示词区
    Directive = " --sref https://s.mj.run/Q-cBvRjJcb8 --ar 1:1 --s 250 --v 6 --sw 100"
    # 图片存储文件夹
    basePath = basePath + "\\" + characterName
    if not os.path.exists(basePath):
        os.makedirs(basePath)

    for index, action in enumerate(actionArray):
        # 生图所用的提示词
        prompt = f"{characterDesc}, {action},{style},{Directive} "
        print(f"将使用的prompt是", prompt)
        genRawImg(prompt, f"pic{index}", 0)
