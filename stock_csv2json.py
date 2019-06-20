import json
import os
import uuid

import pandas as pd
import tushare as ts


def __init_graph_categories():
    """
    将基础数据合并为图数据
    :return:
    """
    # 加载地区数据，工业指数，概念

    industry_fullname = os.path.join(os.environ['STOCK_DATA'], 'data_hive', 'basic_data', 'industry.csv')
    industry_series = pd.Series.from_csv(industry_fullname)
    industry_list = industry_series.tolist()
    concept_fullname = os.path.join(os.environ['STOCK_DATA'], 'data_hive', 'property_data', 'concept.csv')
    concept_dataframe = pd.read_csv(concept_fullname)
    concept_list = concept_dataframe['name'].tolist()

    dic_categories = dict()

    for concept in concept_list:
        dic_categories[concept] = concept
    for industry in industry_list:
        dic_categories[industry] = industry
    return dic_categories


def create_graph_data_job():
    dic_categories = {'Stock': '股票', 'Area': '地区', 'Industry': '工业分类', 'Market': '市场'}
    basic_fullname = os.path.join('stock_temp.csv')
    nodes = []
    edges = []
    basic_dataframe = pd.read_csv(basic_fullname)

    dic_area_id = __get_area_nodes(basic_dataframe, nodes)
    dic_industry_id = __get_industry_nodes(basic_dataframe, nodes)
    dic_market_id = __get_market_nodes(basic_dataframe, nodes)
    __get_stock_nodes(basic_dataframe, nodes)

    __get_stock_edges_with_area(basic_dataframe, dic_area_id, edges)
    __get_stock_edges_with_industry(basic_dataframe, dic_industry_id, edges)
    __get_stock_edges_with_market(basic_dataframe, dic_market_id, edges)

    dic = dict()
    dic['categories'] = dic_categories
    dic['data'] = dict()
    dic['data']['nodes'] = nodes
    dic['data']['edges'] = edges
    if os.path.exists('stock_graph.json'):
        os.remove('stock_graph.json')
    with open('stock_graph.json', 'w') as f:
        json.dump(dic, f, ensure_ascii=False)


def __get_area_nodes(basic_dataframe, nodes):
    dict_area_id = dict()
    for name, group in basic_dataframe.groupby('area'):
        dic_node = dict()
        dic_node['label'] = name
        dic_node['value'] = group.shape[0]
        dic_node['id'] = int(uuid.uuid1())
        dic_node['categories'] = ['Area']
        dic_node['info'] = ''
        dict_area_id[name] = dic_node['id']
        nodes.append(dic_node)
    return dict_area_id


def __get_industry_nodes(basic_dataframe, nodes):
    dict_industry_id = dict()
    for name, group in basic_dataframe.groupby('industry'):
        dic_node = dict()
        dic_node['label'] = name
        dic_node['value'] = group.shape[0]
        dic_node['id'] = int(uuid.uuid1())
        dic_node['categories'] = ['Industry']
        dic_node['info'] = ''
        dict_industry_id[name] = dic_node['id']
        nodes.append(dic_node)
    return dict_industry_id


def __get_market_nodes(basic_dataframe, nodes):
    dict_market_id = dict()
    for name, group in basic_dataframe.groupby('market'):
        dic_node = dict()
        dic_node['label'] = name
        dic_node['value'] = group.shape[0]
        dic_node['id'] = int(uuid.uuid1())
        dic_node['categories'] = ['Market']
        dic_node['info'] = ''
        dict_market_id[name] = dic_node['id']
        nodes.append(dic_node)
    return dict_market_id


def __get_stock_nodes(basic_dataframe, nodes):
    for i in range(basic_dataframe.shape[0]):
        dic_node = dict()
        dic_node['label'] = basic_dataframe.iloc[i]['name']
        dic_node['value'] = 1
        dic_node['id'] = basic_dataframe.iloc[i]['ts_code']
        dic_node['info'] = ''
        dic_node['categories'] = ['Stock']
        nodes.append(dic_node)


def __get_stock_edges_with_area(basic_dataframe, dic_area_id, edges):
    for i in range(basic_dataframe.shape[0]):
        edge = dict()
        edge['id'] = int(uuid.uuid1())
        edge['label'] = 'Area'
        edge['from'] = basic_dataframe.iloc[i]['ts_code']
        edge['to'] = dic_area_id[basic_dataframe.iloc[i]['area']]
        edges.append(edge)


def __get_stock_edges_with_industry(basic_dataframe, dic_area_id, edges):
    for i in range(basic_dataframe.shape[0]):
        edge = dict()
        edge['id'] = int(uuid.uuid1())
        edge['label'] = 'Industry'
        edge['from'] = basic_dataframe.iloc[i]['ts_code']
        edge['to'] = dic_area_id[basic_dataframe.iloc[i]['industry']]
        edges.append(edge)


def __get_stock_edges_with_market(basic_dataframe, dic_area_id, edges):
    for i in range(basic_dataframe.shape[0]):
        edge = dict()
        edge['id'] = int(uuid.uuid1())
        edge['label'] = 'Market'
        edge['from'] = basic_dataframe.iloc[i]['ts_code']
        edge['to'] = dic_area_id[basic_dataframe.iloc[i]['market']]
        edges.append(edge)


ts.set_token('your token')
pro = ts.pro_api()
df = pro.stock_basic(exchange_id='', list_status='L', fields='ts_code,symbol, name,area,industry,fullname, enname, market,exchange, curr_type, list_status, list_date, delist_date,is_hs')
df.to_csv('stock_data.csv')

if __name__ == '__main__':
    create_graph_data_job()
