from flask import Flask, render_template
import util.interpark_util as iu

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>인터파크 베스트 셀러</h1>'

@app.route('/interpark')
def interpark():
    book_list = iu.get_bestseller()
    return render_template('07.interpark.html', book_list=book_list)



if __name__ == '__main__':
    app.run(debug=True)