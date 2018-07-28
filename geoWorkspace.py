# -*- coding: utf-8 -*-
import requests
import json

class geoWorkspace:
    def __init__(self):
        print('geoWorkspace')          

    def getFunction(self, url):
        param = ('admin','geoserver')
        get = requests.get(url, auth=param)
        result = json.loads(get.text)       # 使用json库将json的str类型转换为字典，方便提取内容
        return result
        
    # 获得某个工作空间的详细信息，得到的是一个字典
    def getWorkspaceInfo(self, WorlkspaceName):
        url = 'http://localhost:8081/geoserver/rest/workspaces/' + WorlkspaceName
        result = self.getFunction(url)
        print(result['workspace'])
        
        
    #   获取所有的工作空间,得到的是一个list
    def getAllWorkspace(self):
        url = 'http://localhost:8081/geoserver/rest/workspaces'
        result = self.getFunction(url)
        allWorkspace = result['workspaces']['workspace']
        for w in allWorkspace:
            print(w['name'])
    
    def createWorkspace(self, name):
        myUrl = 'http://localhost:8081/geoserver/rest/workspaces'
    #    file = open('requestBody.xml','r')
    #    payload = file.read()
        data1 = '<workspace><name>%s</name></workspace>' %name
        headers = {'Content-type': 'text/xml'}
        resp = requests.post(myUrl, auth=('admin','geoserver'),data=data1, headers=headers)
        print(resp.text)
        if resp.status_code == 201:        
            print(name + ' workspace create successfully')
        else: print(name + ' workspace create failed')        
        