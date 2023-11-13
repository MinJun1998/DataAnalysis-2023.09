from flask import Blueprint, render_template, request, current_app
import json, os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests, base64
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

chatbot_bp = Blueprint('chatbot_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':0, 'ma':0, 'cb':1, 'sc':0}


@chatbot_bp.route('/counsel', methods=['GET','POST'])
def counsel():
    if request.method == 'GET':
        return render_template('chatbot/counsel.html', menu=menu)
    else:
        user_input = request.form['userInput']
        embedding = model.encode(user_input)
        wdf['유사도'] = wdf.embedding.map(lambda x: cosine_similarity([embedding],[x]).squeeze())
        answer = wdf.loc[wdf.유사도.idxmax()]
        result = {
            'category':answer.구분, 'user':user_input, 'chatbot':answer.챗봇, 'similarity':answer.유사도
        }
        return json.dumps(result)

@chatbot_bp.route('/bard', methods=['GET','POST'])
def bard():
    pass
    
@chatbot_bp.route('/genImg', methods=['GET','POST'])
def gen_img():
    pass

@chatbot_bp.route('/yolo', methods=['GET','POST'])
def yolo():
    if request.method == 'GET':
        return render_template('chatbot/yolo_form.html', menu=menu)
    else:
        file_image = request.files['image']
        img_file = os.path.join(current_app.static_folder, f'upload/{file_image.filename}')
        file_image.save(img_file)
        img_type = img_file.split('.')[-1]
        if img_type == 'jfif':
            img_type == 'jpg'
            
        with open(os.path.join(current_app.static_folder, 'keys/etriAiKey.txt')) as f:
            accessKey = f.read()
        with open(img_file, 'rb') as f:
            img_content = base64.b64encode(f.read()).decode("utf8")
        openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey}
        requestJson = { "argument": { "type": img_type, "file": img_content } }
        result = requests.post(
            openApiURL, headers=headers, data=json.dumps(requestJson)
        ).json()
        obj_list = result['return_object']['data']
        
        img = Image.open(img_file)
        draw = ImageDraw.Draw(img)
        size = img.width + img.height
        font_size = 16 if size < 1600 else 32 if size < 3200 else 48
        line_width = 1 if size < 1600 else 2 if size < 3200 else 3
        font = ImageFont.truetype('malgun.ttf', font_size)
        for obj in obj_list:
            name = obj['class']
            x, y = int(obj['x']), int(obj['y'])
            w, h = int(obj['width']), int(obj['height'])
            draw.rectangle(((x,y), (x+w,y+h)), outline=(255,0,0), width=3)
            draw.text((x+10, y+10), name, font=font, fill=(255,0,0))
        
        savefile = os.path.join(current_app.static_folder, 'result/yolo.png')
        plt.imshow(img)
        plt.axis('off')
        plt.savefig(savefile, format='png')
        mtime = os.stat(savefile).st_mtime

        return render_template('chatbot/yolo_res.html', menu=menu, mtime=mtime)