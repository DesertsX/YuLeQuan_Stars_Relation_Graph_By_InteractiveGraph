# coding: utf-8
# @Time    : 2019-04-24 21:00
# @Author  : DesertsX
# @Site    : 
# @File    : graph_view.py

from flask import Blueprint, request, render_template

graph = Blueprint('graph', __name__)

# http://127.0.0.1:5000/graph/relation?stock1=%E5%B9%B3%E5%AE%89%E9%93%B6%E8%A1%8C&stock2=%E6%8B%9B%E5%95%86%E9%93%B6%E8%A1%8C
@graph.route('/graph/relation', methods=['GET'])
def get_relation():
    stock1 = request.args.get('stock1')
    stock2 = request.args.get('stock2')
    return render_template('stock_relation.html', stock1=stock1, stock2=stock2)

# http://127.0.0.1:5000/apachecn
@graph.route('/apachecn')
def apachecn():
    return render_template('apachecn.html')


# http://127.0.0.1:5000/yulequan-relations-graph
@graph.route('/yulequan-relations-graph') # 不要写成 /graph/yulequan-relations-graph 否则加载头像图片时无法显示
def ylq():
    return render_template('yulequan-relations-graph.html')
