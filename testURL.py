# -*- coding: utf-8 -*-
import requests
import json
import xml.sax
import xml.sax.handler

#url="https://www.baidu.com/s"
#headers={'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36", 'Accept-Charset': 'UTF-8'}
#post_data={'username':"qujun","passwd":"xixi"}
#parameters={'wd':"abc"}
##提交get请求
#P_get=requests.get(url,params=parameters)
#print(P_get)
##提交post请求
#P_post=requests.post(url,headers=headers,data=post_data)
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


def getFunction(url):
    param = ('admin','geoserver')
    get = requests.get(url, auth=param)
    result = json.loads(get.text)       # 使用json库将json的str类型转换为字典，方便提取内容
    return result
    
    
def getWorkspaceInfo():
    url = 'http://localhost:8081/geoserver/rest/workspaces/acme'
    result = getFunction(url)
    print(result['workspace']['name'])
    
    

def getAllWorkspace():
    url = 'http://localhost:8081/geoserver/rest/workspaces'
    result = getFunction(url)
    allWorkspace = result['workspaces']['workspace']
    print(type(allWorkspace))
    for w in allWorkspace:
        print(w['name'])

#    print(result['workspace']['name'])
        
def getFeaturetypeInfo():
    url = 'http://localhost:8081/geoserver/rest/workspaces/road_wms/datastores/tiger_roads/featuretypes/tiger_roads.xml'  
    param = ('admin','geoserver')
    get = requests.get(url, auth=param)
    print(get.text)          
    # 使用minidom解析器打开 XML 文档
    xh = XMLHandler()  
    xml.sax.parseString(get.text, xh)  
    ret = xh.getDict()  
    print(ret[''])
    
    
    
if __name__ == "__main__":
#    getWorkspaceInfo()    
#    getAllWorkspace()
    getFeaturetypeInfo()
