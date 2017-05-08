#coding=utf-8
import pandas as pd
import json
import types

def prodeal(path):
    data = pd.read_excel(path, encoding='gbk')
    data1 = data.loc[data['from']==1]
    length = data1.shape[0]
    data2 = data1.reset_index()
    return length, data2

def tojson(data,shape):
    back=[]
    for i in range(0, shape):
        tmp = data.ix[i]
        obj = {}
        obj['usersay'] = tmp['usersay']
        if type(tmp['intent']) is types.FloatType:
            print tmp['index']+2,'intent未标注'
            continue
        else:
            obj['intent'] = tmp['intent'].split(',')
        if type(tmp['intents']) is types.UnicodeType:
            obj['intents'] = tmp['intents'].split(',')
        if type(tmp['entities']) is types.UnicodeType:
            obj['entities'] = tmp['entities'].split(',')
        if type(tmp['entities data']) is types.UnicodeType:
            elements = tmp['entities data'].split('\\t')
            di = {}
            for element in elements:
                if len(element.split(':'))<2:
                    str1=tmp['index']+2
                    print str1,"intents错误",tmp['entities data']
                    continue
                else:
                    di.__setitem__(element.split(':')[0].strip(), element.split(':')[1])
            obj['entities_data'] = di
        if type(tmp['entities.1']) is types.UnicodeType:
            obj['entities1'] = tmp['entities.1'].split(',')
        back.append(json.dumps(obj))
    return back

excel_flie_path = r'/Users/zhaowenjun/Desktop/22.xlsx'
length, data = prodeal(excel_flie_path)
jsonlist = tojson(data,length)
for ajson in jsonlist:
    print ajson+'\n'