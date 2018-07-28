# -*- coding: utf-8 -*-
import requests
import json



class geoStore:
    def __init__(self):
        print('geoStore')  
        
    def getStoreInfo(self, workspaceName, storeName):
        url = 'http://localhost:8081/geoserver/rest/workspaces/%s/datastores/%s.xml' %(workspaceName, storeName)
        param = ('admin','geoserver')
        get = requests.get(url, auth=param)
        print(get.text)        
    
    
    def addPGStore(self):
        myUrl = 'http://localhost:8081/geoserver/rest/workspaces/acme/datastores/'
        file = open('pgdata.xml','rb')
        payload = file.read()
        headers = {'Content-type': 'text/xml'}
        resp = requests.post(myUrl, auth=('admin','geoserver'),data=payload, headers=headers)
        print(resp.text)
        if resp.status_code == 201:        
            print('add PGdata successfully')
        else: print('add PGdata failed')  
        
        # 得到某个工作空间所有的数据存储
    def getAllStore(self, workspaceName):
        url = 'http://localhost:8081/geoserver/rest/workspaces/%s/datastores/' % workspaceName
        param = ('admin','geoserver')
        get = requests.get(url, auth=param)
        result = json.loads(get.text)       # 使用json库将json的str类型转换为字典，方便提取内容
        print(result['dataStores']['dataStore'])     
        
    def createStore(self, workspaceName):
        myUrl = 'http://localhost:8081/geoserver/rest/workspaces/%s/datastores' % workspaceName
        file = open('dataStore.xml','r')
        payload = file.read()
        headers = {'Content-type': 'text/xml','Accept': 'text/xml'}
        resp = requests.post(myUrl, auth=('admin','geoserver'),data=payload, headers=headers)   
        print(resp.text)
        if resp.status_code == 201:        
            print('datastore create successfully')
        else: print('datastore create  failed') 
