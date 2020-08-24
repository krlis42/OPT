from flask import Flask,escape,url_for,render_template
from flask_paginate import Pagination, get_page_args
from flask_caching import Cache
from lunar import getCalendar_today
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

cache = Cache()


def main():
    cache.init_app(app)
    with app.app_context():
        cache.clear()



'''
# first test
@app.route('/index')
@app.route('/home')
@app.route('/')
def hello_world():
    return 'Hello,World!'
'''
import json,codecs,os
import random,datetime
path = str(os.getcwd()+'\\')
data = list()

with codecs.open(path + 'poem.json', 'r', 'utf-8') as f:    
    data = json.load(f)

@app.route('/index')
@app.route('/home')
@app.route('/',methods=['GET'])
def index():
    return render_template('home.html',
                            data=data,
                            poem_index=random.randint(1,len(data)),
                            photo_index=random.randint(1,32),
                            #current_time=datetime.date.today()
                            today=getCalendar_today()
                           )


def get_poems(offset=0, per_page=10):
    return data[offset: offset + per_page]
#print(type(data)) # list


'''
{
'title': '江南曲', 
'notes': [], 
'author': '李益', 
'paragraphs': ['嫁得瞿塘贾，朝朝误妾期。', '早知潮有信，嫁与弄潮儿。'],
 'dynasty': '唐代'
 }
 '''

@app.route('/poem')
def poem():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page',
                                           
                                           )
    total = len(data)    
    page_poem = get_poems(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('poem.html',
                           data=page_poem,
                           page=page,
                           imageIndex=str(page),
                           per_page=per_page,
                           pagination=pagination,
                           )



@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码

@app.route('/opt')
def opt():
    return render_template('opt.html')

@app.route('/erica')
def erica():
    return render_template('erica.html')    

@app.route('/kr')
def kr():
    return render_template('kr.html')    

@app.route('/ricecook')
def ricecook():
    return render_template('ricecook.html')  

@app.route('/canton')
def canton():
    return render_template('canton.html')  

@app.route('/trista')
def trista():
    return render_template('trista.html')  


app.config['JSON_AS_ASCII'] = False
from flask import request,Response,jsonify
with codecs.open(path + 'sc.json', 'r', 'utf-8') as f:    
    data2 = json.load(f)

# print(type(data2))
# print(len(data2))

poemlists={}
李白={}
for i in range(len(data2)):
    poemlists[data2[i]['title']] = data2[i]['author']
    if data2[i]['author'] =="李白":
        李白[i] = data2[i]['title']
    else:
        pass
#print(李白)  


@app.route('/authors')
def api_author():
    if 'name' in request.args:
        aa={}
        for i in range(len(data2)):
            if data2[i]['author'] == request.args['name']:
                aa[i] = data2[i]['title']
            else:
                pass
        resp = jsonify(aa)
        resp.status_code = 200  
        resp.headers['Xtotal'] = len(aa)
        return resp
    else:
        return "哪个诗人呢"

@app.route('/lists')
def lists():
    resp = jsonify(poemlists)
    resp.status_code = 200  
    resp.headers['Xtotal'] = len(poemlists)
    return  resp

@app.route('/api1')
def Api1():
    return render_template('api_author.html') 

@app.route('/api2')
def Api2():
    return render_template('api_lists.html') 


if __name__ == '__main__':
    main()
    app.run(debug=True)