from flask import Blueprint, render_template, request, current_app
import json, os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests, base64
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import util.chatbot_util as cu

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
        return render_template('chatbot/yolo.html', menu=menu)
    else:
        color = request.form['color']
        linewidth = int(request.form['linewidth'])
        fontsize = int(request.form['fontsize'])
        file_image = request.files['image']
        img_file = os.path.join(current_app.static_folder, f'upload/{file_image.filename}')
        file_image.save(img_file)

        mtime = cu.proc_yolo(current_app.static_folder, img_file, color, linewidth, fontsize)
        return json.dumps(str(mtime))