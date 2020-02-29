#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node

class ACE2005Graph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/Event.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="需要修改",  # 数据库user name，如果没有更改过，应该是neo4j
            password="需要修改")

        relations_type = []# role
        nodes_type = ['event']# 'event' and entity_type
        Event_set = []
        f=open(self.data_path,"r",encoding="utf-8")
        file_data=json.load(f)
        f.close()

        for event in file_data:
            Event_set.append(event)
            arguments = event['arguments']
            for argument in arguments:
                if argument['role'] not in relations_type:
                    relations_type.append(argument['role'])
                if argument['entity-type'] not in nodes_type:
                    nodes_type.append(argument['entity-type'])
        self.Event_set = Event_set
        self.relations_type = relations_type
        self.nodes_type = nodes_type


    '''读取文件'''
    def read_nodes_relations(self):
        # 实体节点 event+argument
        nodes={}
        for nodetype in self.nodes_type:
            nodes[nodetype] = []
        nodes['event'] = self.Event_set

        # 实体关系
        relations={}
        for relationtype in self.relations_type:
            relations[relationtype]=[]
        count = 0

        for data in self.Event_set:
            # event_id = data['id']#事件id
            arguments = data['arguments']
            for argument in arguments:
                # argument_id = argument['id']
                role = argument['role']
                entity_type = argument['entity-type']
                # 节点
                if argument not in nodes[entity_type]:
                    nodes[entity_type].append(argument)
                # 关系
                if (data,argument) not in relations[role]:
                    relations[role].append((data,argument))

        return nodes,relations


    '''建立节点'''
    def create_node(self, nodes):
        total_num  = 0
        for key in nodes:
            count = 0
            if key != "event":#非事件节点
                for node_ in nodes[key]:
                    label = node_['entity-type']
                    node_name = node_['text']
                    node = Node(label, name=node_name, entityID= node_['id'])
                    self.g.create(node)
                    count += 1
                    if count % 100==0:
                        print(key, count, len(nodes[key]))
            else:
                for event in nodes[key]:
                    node = Node("Event", eventID=event['id'], event_type=event['event_type'], trigger = event['trigger']['text'])
                    self.g.create(node)
                    count += 1
                    if count % 100 == 0:
                        print(key, count, len(nodes[key]))
            total_num = total_num + count
        return total_num


    '''创建知识图谱实体节点类型schema'''
    def create_graph(self):
        nodes,relations = self.read_nodes_relations()
        nodes_num = self.create_node(nodes)
        relations_num = self.create_relationship(relations)
        print("Total Nodes:",nodes_num)
        print("Total Relations:", relations_num)
        return


    '''创建实体关联边'''
    def create_relationship(self, relations):
        total_num = 0
        print('创建实体关联边')
        for key in relations:
            count = 0
            for relation_ in relations[key]:
                p =  relation_[0]#event_id
                q  =  relation_[1]#role
                query = "match(p:%s),(q:`%s`) where p.eventID='%s'and q.entityID='%s' create (p)-[rel:`%s`{name:'%s'}]->(q)" % (
                    'Event', q['entity-type'], p['id'], q['id'], "EventRole-"+q['role'], q['role'])
                try:
                    self.g.run(query)
                    count += 1
                    if count % 100 == 0:
                        print('EventRole-'+key, count, len(relations[key]))
                except Exception as e:
                    print(e)
                    print(query)
                    return -1
            total_num = total_num + count
        return total_num



if __name__ == '__main__':
    handler = ACE2005Graph()
    handler.create_graph()

