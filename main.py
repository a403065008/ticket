import os
from cairosvg import svg2png
from PIL import Image
import time
import requests
import json
from ultralytics import YOLO
from urllib.parse import unquote


def getphoto(path):
    svg_content = path

    with open("output.svg", "w") as f:
        f.write(svg_content)

    svg2png(url="output.svg", write_to="output.png")
    os.remove("output.svg")

    background_color = (255, 255, 255)  # 白色

    # 開啟沒有背景的 PNG 圖片
    image_path = "output.png"
    foreground = Image.open(image_path).convert("RGBA")

    # 創建一張有背景的白色圖片
    background = Image.new("RGBA", foreground.size, background_color)

    # 將沒有背景的 PNG 圖片粘貼到有背景的圖片上
    combined = Image.alpha_composite(background, foreground)

    # 將結果保存為新的 PNG 圖片
    combined.save("data/0.png", "PNG")


def getvalue():
    answer = ""
    model = YOLO("yolov8n.pt")
    model = YOLO("best.pt")  # load a custom model

    # 辨識驗證碼
    results = model.predict(source="data/0.png", show=True)

    # 載入label
    names = model.names
    list = []
    for i in results[0].numpy():
        list.append([i.boxes[0].boxes[0][0], i.boxes[0].boxes[0][5]])

    # 根據X進行排序
    sorted_list = sorted(list, key=lambda x: x[0])
    sorted_second_elements = [item[1] for item in sorted_list]

    for i in sorted_second_elements:
        answer += names[int(i)]
    return answer


def gettoken(cookies_user):
    url_decoded_data = unquote(cookies_user)
    json_data = json.loads(url_decoded_data)
    return json_data.get("access_token", "")


# get unix time
unix_timestamp = int(time.time())
unix_timestamp_milliseconds = int(time.time() * 1000)

# auth_url = f"https://apis.ticketplus.com.tw/user/api/v1/refreshToken?_={unix_timestamp_milliseconds}"
photo_url = f"https://apis.ticketplus.com.tw/captcha/api/v1/generate?_={unix_timestamp_milliseconds}"
order_url = f"https://apis.ticketplus.com.tw/ticket/api/v1/reserve?_={unix_timestamp_milliseconds}"

# 因隱私問題故跳過auth，直接從cookies拿data
cookies_user = ""
access_token = gettoken(cookies_user)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Authorization": f"Bearer {access_token}",
    "Content-Length": "0",
}

data = {"sessionId": "s000000538", "refresh": True}
# get SVG path
response = requests.post(photo_url, json=data, headers=headers)

parsed_data = response.json()
path = parsed_data["data"]
key = parsed_data["key"]

# get SVG
getphoto(path)

# productID range
productId1 = []
for i in range(22, 56):
    productId1.append(f"p0000035{i}")
ans = getvalue()
print("ans：", ans)
swtich = True
while swtich:
    for i in productId1:
        data1 = {
            "products": [{"productId": i, "count": int(2)}],
            "captcha": {"key": str(key), "ans": str(ans)},
            "reserveSeats": True,
            "consecutiveSeats": True,
            "finalizedSeats": True,
        }
        response1 = requests.post(order_url, json=data1, headers=headers)
        result = response1.json()
        print(f"{i}{result} ")
        if result["errCode"] == "00":
            swtich = False
            print("order success")
            break
