import json
datapath='D:\创新院\知识图谱\模型\Ace2005KG\data\event_data.json'
f=open(datapath,'r',encoding="utf-8")
data=json.load(f)
f.close()
Eventdata=[]
for line in data:
    if line['golden-event-mentions']:
        for  event in line['golden-event-mentions']:
            Eventdata.append(event)
# with open("D:\创新院\知识图谱\模型\Ace2005KG\data\Event.json",'w') as f:
#     json.dump(Eventdata,f)

with open("D:\创新院\知识图谱\模型\Ace2005KG\data\sample.json",'w') as f:
    json.dump([Eventdata[0]],f)

# relation_type = []
# for event in Eventdata:
#     arguments=event['arguments']
#     for argument in arguments:
#         if argument['role'] not in relation_type:
#             relation_type.append(argument['role'])
#
# nodes_type = ['event']
# for event in Eventdata:
#     arguments=event['arguments']
#     for argument in arguments:
#         if argument['entity-type'] not in nodes_type:
#             nodes_type.append(argument['entity-type'])