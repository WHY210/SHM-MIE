from flask import Flask, render_template, request, jsonify, send_from_directory,
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import json
from math import radians, sin, cos, sqrt, atan2

### API Key ###

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Create OpenAI client with the API key
client = OpenAI(api_key=openai_api_key)



def GPT_answer(content):

    ### API request ###
    
    try:
        # 使用OpenAI模型生成人類可讀的回應
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "不用先重述資料內容，直接以繁體中文告訴用戶此次地震對於安全上具體好理解的詳細分析，具體位置（縣市或方位）、嚴重性、差不多影響的過往地震，不要講幹話，也不要建議我多了解查看。"},
                {"role": "user", "content": content}
            ],
            max_tokens=250  # 根據需要調整生成的文本長度
        )

        response = completion.choices[0].message.content
        print(f"openAI response type: {type(completion.choices)}")
     
        return response
    
    except OpenAIError as e:
            return json.dumps({"error": str(e)})
    
def haversine(lat1, lon1, lat2, lon2):
    # 將經緯度轉換為弧度
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # 地球半徑為6371公里

    return distance

def parse_earthquake_data(content):
    lines = content.split('\n')[:9]
    earthquake_line = lines[0]

    # 取得地震的經緯度 
    time_index = earthquake_line.find('T', 5)
    lat_index = earthquake_line.find('N')
    lon_index = earthquake_line.find('E', 15) 
    dep_index = earthquake_line.find('Z') 
    mag_index = earthquake_line.find('M', 15) 
    
    time = str(earthquake_line[time_index + 1:lon_index].strip())
    lat = float(earthquake_line[lat_index + 1:].split()[0])
    lon = float(earthquake_line[lon_index + 1:].split()[0])
    dep = float(earthquake_line[dep_index + 1:].split()[0])
    mag = float(earthquake_line[mag_index + 1:].split()[0])

    return time, lat, lon, dep, mag

### Flask ###

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
def model():
    return send_from_directory(app.static_folder, 'model.js')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file provided"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and file.filename.endswith('.txt'):
        # 讀取文本文件內容
        try:
            content = file.stream.read().decode('utf-8')
            print(f"load .txt Content type: {type(content)}")
        except Exception as e:
            return jsonify({"error load.txt": str(e)})
        
        time, lat, lon, dep, mag = parse_earthquake_data(content)
        distance = haversine(24.803, 120.995, lat, lon)

        info = {
            "地震時間": time,
            "震央經度": lon,
            "震央緯度": lat,
            "震央深度": dep,
            "規模": mag,
            "震央距離": f"{distance:.2f} 公里"
        }
        
        
        # 用OpenAI的API生成回答
        response = GPT_answer(json.dumps(info))
        info["GPT回答"] = response
        
        print(f"Response: {response}")
        print(info)

        # post to display
        try:
            return render_template('display.html', content=info)
        except Exception as e:
            return jsonify({"error display": str(e)})
        
    else:
        return "Invalid file format. Please upload a .txt file."

if __name__ == '__main__':
    # 啟動 Flask
    app.run()
