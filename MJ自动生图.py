import os
import time
import requests
import json

basePath = "C:\\Users\\33051\\Desktop\\Lora"

def queryGenerateStatus(taskId: str):
    # Replace with your valid API endpoint
    url = f"https://your-api-endpoint.com/mj/task/{taskId}/fetch"

    # Define request headers
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        responseJson = json.loads(response.text)
        print(f"别急啊，你要是着急你退出啊：{responseJson['progress']}")

        if responseJson["finishTime"] is None:
            return False
        else:
            return True

# Generate MJ's four-in-one image using prompt
def genRawImg(prompt: str, picName: str, indexOfAction: int):
    # Replace with your valid API endpoint
    url = "https://your-api-endpoint.com/mj/submit/imagine"

    # Define request headers
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    # Define request data
    data = {
        "base64Array": [],
        "notifyHook": "",
        "prompt": prompt,
        "state": ""
    }

    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        responseJson = json.loads(response.text)
        rawImgTaskID = responseJson['result']

        # Wait for image generation to complete
        while True:
            print("别催了，在整了哥")
            if queryGenerateStatus(rawImgTaskID):
                break
            time.sleep(3)
        getTaskTargetImg(rawImgTaskID, 1, picName, indexOfAction)
        getTaskTargetImg(rawImgTaskID, 2, picName, indexOfAction)
        getTaskTargetImg(rawImgTaskID, 3, picName, indexOfAction)
        getTaskTargetImg(rawImgTaskID, 4, picName, indexOfAction)

# Get specific image from the four-in-one image
def getTaskTargetImg(taskId: str, imgIndexOfRaw: int, picName: str, indexOfAction: int):
    # Replace with your valid API endpoint
    url = "https://your-api-endpoint.com/mj/submit/simple-change"

    # Define request headers
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    # Define request data
    data = {
        "content": f"{taskId} U{imgIndexOfRaw}",
        "notifyHook": "",
        "state": ""
    }

    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        responseJson = json.loads(response.text)
        taskID = responseJson['result']

        # Wait for specific image generation to complete
        while True:
            if queryGenerateStatus(taskID):
                break
            time.sleep(3)
        downloadTaskId(taskID, picName, indexOfAction, imgIndexOfRaw)

# Download image by task ID
def downloadTaskId(taskId: str, picName: str, indexOfAction: int, imgIndexOfRaw: int):
    # Replace with your valid API endpoint
    url = f"https://your-api-endpoint.com/mj/task/{taskId}/fetch"

    # Define request headers
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        responseJson = json.loads(response.text)
        ImgResponse = requests.get(responseJson['imageUrl'])
        
        # Check if request was successful
        if ImgResponse.status_code == 200:
            # Save image to specified path
            with open(f'{basePath}\\{picName}_{imgIndexOfRaw}.png', 'wb') as file:
                file.write(ImgResponse.content)
            print("下载成功了，还愣着干嘛，快去文件夹选图")
        else:
            print(f"请求失败，状态码: {ImgResponse.status_code}")

if __name__ == "__main__":
    # Character description and settings
    characterName = "A middle-aged ancient general with a black beard, black hair, and armor"
    characterDesc = ""
    style = ""
    actionArray = [
        "the prompt input here",
    ]
    Directive = " --sref https://s.mj.run/Q-cBvRjJcb8 --ar 1:1 --s 250 --v 6 --sw 100"

    # Ensure the base path exists
    basePath = basePath + "\\" + characterName
    if not os.path.exists(basePath):
        os.makedirs(basePath)

    # Iterate through actions to generate images
    for index, action in enumerate(actionArray):
        prompt = f"{characterName} {characterDesc} {style} {action} {Directive}"
        picName = f"{characterName}_{index+1}"
        genRawImg(prompt, picName, index)

        # 生图所用的提示词
        prompt = f"{characterDesc}, {action},{style},{Directive} "
        print(f"将使用的prompt是", prompt)
        genRawImg(prompt, f"pic{index}", 0)
