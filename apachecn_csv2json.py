import os
import json
import uuid
import numpy as np
import pandas as pd


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def get_categories(df):
    dic_categories = {}
    dic_categories['person'] = ('人物', '有关')
    dic_categories['area'] = ('地点', '位于')
    dic_categories['project'] = ('项目', '参与')
    return dic_categories


def get_cate(dic_categories):
    dic_cate = dict()
    for k, v in dic_categories.items():
        dic_cate[k] = v[0]
    return dic_cate


def get_nodes(df, nodes, dic_categories):
    kg_dict = dict()
    for k, (v1, v2) in dic_categories.items():
        dic_categories_id = dict()
        for name, group in df.groupby(k):
            dic_node = dict()
            dic_node['label'] = name  # key集合中，对应分类名称
            dic_node['value'] = group.shape[0]  # 出现次数
            if k == "person":
                dic_node['id'] = group["id"].tolist()[0]
                dic_node['image'] = group["image"].tolist()[0]
            else:
                dic_node['id'] = int(uuid.uuid1())
            dic_node['categories'] = [k]
            dic_node['info'] = group["info"].tolist()[0]
            dic_categories_id[name] = dic_node['id']
            nodes.append(dic_node)
        if k != "person":
            kg_dict[k] = dic_categories_id
    return kg_dict


def get_edges(df, kg_dict, edges, dic_categories):
    for k, v in kg_dict.items():
        # for i in range(df.shape[0]):
        #     edge = dict()
        #     edge['id'] = int(uuid.uuid1())
        #     edge['label'] = dic_categories[k][1]
        #     edge['from'] = df.iloc[i]['id']
        #     edge['to'] = v[df.iloc[i][k]]
        #     edges.append(edge)
        for name, group in df.groupby([k, "person"]):
            edge = dict()
            edge['id'] = int(uuid.uuid1())
            edge['label'] = dic_categories[k][1]
            edge['from'] = group["id"].tolist()[0]
            edge['to'] = v[group[k].tolist()[0]]
            edges.append(edge)


def get_translator():
    translator = {
        "nodes": """function (node) {
            //set description
            if (node.description === undefined) {
                var description = "<p align=center>";
                if (node.image !== undefined) {
                description += "<img src='" + node.image + "' width=150/><br>";
                }
                description += "<b>" + node.label + "</b>" + "[" + node.id + "]";
                description += "</p>";
                if (node.info !== undefined) {
                description += "<p align=left>" + node.info + "</p>";
                } else {
                if (node.title !== undefined)
                    description += "<p align=left>" + node.title + "</p>";
                }
                node.description = description;
            }
        }"""
    }
    return translator


def create_graph(filename):
    """
    将基础数据合并为图数据
    :return:
    """
    df = pd.read_csv(filename)
    nodes = []
    edges = []
    dic_categories = get_categories(df)
    dic_cate = get_cate(dic_categories)
    kg_dict = get_nodes(df, nodes, dic_categories)
    get_edges(df, kg_dict, edges, dic_categories)

    # print("\n\n\n>>> ", dic_categories)
    # print("\n\n\n>>> ", dic_cate)
    # print("\n\n\n>>> ", nodes)
    # print("\n\n\n>>> ", kg_dict)
    # print("\n\n\n>>> ", edges)

    # 生成图 json 文件
    dic = dict()
    dic['categories'] = dic_cate
    dic['translator'] = get_translator()
    dic['data'] = dict()
    dic['data']['nodes'] = nodes
    dic['data']['edges'] = edges
    result_filename = 'webapp/static/apachecn_graph.json'
    if os.path.exists(result_filename):
        os.remove(result_filename)
    with open(result_filename, 'w') as f:
        # ensure_ascii 解决乱码问题
        json.dump(dic, f, cls=NpEncoder, indent=4, separators=(',', ':'), ensure_ascii=False)


if __name__ == "__main__":
    filename = 'apachecn_data.csv'
    # 初始化 图
    create_graph(filename)
