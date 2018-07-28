# -*- coding: utf-8 -*-
import requests
import xml.sax
import xml.sax.handler
import json
from geoStore import geoStore

class XMLHandler(xml.sax.handler.ContentHandler):  
    def __init__(self):  
        self.buffer = ""                    
        self.mapping = {}                  
  
    def startElement(self, name, attributes):  
        self.buffer = ""                    
  
    def characters(self, data):  
        self.buffer += data                      
  
    def endElement(self, name):  
        self.mapping[name] = self.buffer           
  
    def getDict(self):  
        return self.mapping  

        
    """获取某个工作空间下的，某个数据存储中的某个feature的信息
        需要提供工作空间名称，数据存储名称以及要素名称
    """
def getFeaturetypeInfo():
    url = 'http://localhost:8081/geoserver/rest/workspaces/road_wms/datastores/tiger_roads/featuretypes/tiger_roads.xml'  
    param = ('admin','geoserver')
    get = requests.get(url, auth=param)
    print(get.text)          
    # 使用minidom解析器打开 XML 文档
    xh = XMLHandler()  
    xml.sax.parseString(get.text, xh)  
    ret = xh.getDict()  
    print(ret)
    
    """获得某个数据存储中的所有要素
        需要提供工作空间名称以及数据存储名称    
    """
def getAllFeaturetype(workspaceName, storeName):    
    url = 'http://localhost:8081/geoserver/rest/workspaces/%s/datastores/%s/featuretypes'  % (workspaceName, storeName)
    param = ('admin','geoserver')
    headers = {'Content-type': 'application/json'}
    get = requests.get(url, auth=param, headers=headers)
    print(get.text)          
    # 使用minidom解析器打开 XML 文档
#    xh = XMLHandler()  
#    xml.sax.parseString(get.text, xh)  
#    ret = xh.getDict()  
#    print(ret)
#    


def createFeaturetype(workspaceName, storeName):   
    url = 'http://localhost:8081/geoserver/rest/workspaces/%s/datastores/%s/featuretypes'  % (workspaceName, storeName)
    param = ('admin','geoserver')
    headers = {'Content-type': 'application/xml'}
    file = open('xml/createFeaturetype.xml','rb')
    payload = file.read()
    resp = requests.post(url, auth=param, data=payload, headers=headers)
    print(resp)          
    if resp.status_code == 201:        
        print('featuretype create successfully')
    else: print('featuretype create failed')   


# 向工作区上传数据，上传成功会自动新建一个数据存储
def uploadShp():
    myUrl = 'http://localhost:8081/geoserver/rest/workspaces/acme/datastores/roads/file.shp'
    file = open('region.zip','rb')
    payload = file.read()
    headers = {'Content-type': 'application/zip'}
    resp = requests.put(myUrl, auth=('admin','geoserver'),data=payload, headers=headers)
    print(resp.text)
    if resp.status_code == 201:        
        print('file upload successfully')
    else: print('file upload failed')    

    
def publishPGtable(name):
    myUrl = ' http://localhost:8081/geoserver/rest/workspaces/acme/datastores/nyc/featuretypes'
    #    file = open('requestBody.xml','r')
    #    payload = file.read()
    data1 = '<featureType><name>%s</name></featureType>' %name
    headers = {'Content-type': 'text/xml'}
    resp = requests.post(myUrl, auth=('admin','geoserver'),data=data1, headers=headers)
    print(resp.text)
    if resp.status_code == 201:        
        print(name + ' publish successfully')
    else: print(name + ' publish failed')   




"""创建一张表，在pg数据库上"""
def createTable(): 
    myUrl = 'http://localhost:8081/geoserver/rest/workspaces/acme/datastores/nyc/featuretypes'
    file = open('createTable.xml','r')
    payload = file.read()   
    headers = {'Content-type': 'text/xml'}
    resp = requests.post(myUrl, auth=('admin','geoserver'),data=payload, headers=headers)
    print(resp.text)
    if resp.status_code == 201:        
        print('table create successfully')
    else: print('table create failed')   


def getAllLayers():
    url = 'http://localhost:8081/geoserver/rest/layers'
    param = ('admin','geoserver')
    headers = {'Content-type': 'application/json'}
    get = requests.get(url, auth=param, headers=headers)
    result = json.loads(get.text) 
    layers = result['layers']['layer']
#    print(layers)
    for layer in layers:
        print(layer['name'])

def getAllWMSStore(workspaceName):
    url = 'http://localhost:8081/geoserver/rest/workspaces/%s/wmsstores'  % workspaceName
    param = ('admin','geoserver')
    headers = {'Content-type': 'application/json'}
    get = requests.get(url, auth=param, headers=headers)
    print(get.text) 
        
    
def createCoverageStore():
    myUrl = 'http://localhost:8081/geoserver/rest/workspaces/acme/coveragestores'
    file = open('xml/coverageStore.xml','r')
    payload = file.read()   
    headers = {'Content-type': 'application/xml'}
    resp = requests.post(myUrl, auth=('admin','geoserver'),data=payload, headers=headers)
    print(resp)
    print(resp.text)
    if resp.status_code == 201:        
        print('coverageStore create successfully')
    else: print('coverageStore create failed') 
    
if __name__ == "__main__":
#    createWorkspace('acme')
#    getFeaturetypeInfo()
#    uploadShp()
#    getStoreInfo('acme', 'nyc')
    
#    gw = geoWorkspace()
#    gw.getAllWorkspace()
#    gw.getWorkspaceInfo('road_wms')
#    gw.getAllWorkspace()

    #    addPGStore()
    
#    gs = geoStore()
#    gs.getAllStore('acme')
#    gs.createStore('acme', )
#    publishPGtable('sd')
##    createTable()
#    getAllFeaturetype('acme', 'nyc')
#    getAllLayers()
#    createFeaturetype('acme', 'nyc')
#    getAllWMSStore('acme')
    createCoverageStore()
    