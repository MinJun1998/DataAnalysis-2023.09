import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import os


x = np.random.normal(1,2,200)
y = np.random.uniform(-2,4,200)
plt.scatter(x, y)
plt.show()


app = Flask(__name__)

@app.route('/scatter', methods=['GET', 'POST'])
def scatter():
    if request.method == 'GET':
        return render_template('99.scatter.html')
    else:
        img_file = os.path.join(app.root_path, 'static/img/scatter.png')
        return render_template('99.scatter_res.html')
        
if __name__ == '__main__':
    app.run(debug=True)
    