# -*- coding: utf-8 -*-
from geoserver.catalog import Catalog
import geoserver.util
from geoserver.support import JDBCVirtualTable, JDBCVirtualTableGeometry, JDBCVirtualTableParam

"""
    geoserver发布地图服务的一般流程
    1.创建工作空间
    2.创建数据存储
    3.发布
"""


def getLayer():
    cat = Catalog("http://localhost:8081/geoserver/rest")
    all_layers = cat.get_layers()
    for layer in all_layers:
        print(layer.name)


def stopLayer(layerName):
    layer = cat.get_layer(layerName)
    layer.enabled = False
    cat.save(layer)
    cat.reload()

"""
创建数据存储
1.提供数据存储的名称
2.提供数据
3.工作空间（可选）
"""
def createStore(cat, name, dataPath, workspaceName=None):
    workspace = None
    if workspaceName:        
        workspace = cat.get_workspace(workspaceName)

    shapefile = geoserver.util.shapefile_and_friends(dataPath)   
    cat.create_featurestore(name, shapefile, workspace, charset="UTF-8")
    cat.reload()
    print("%s store create successfully") % name


def createLayer():   
    cat = Catalog('http://localhost:8081/geoserver/rest/', 'admin', 'geoserver')
    store = cat.get_store('test')
    geom = JDBCVirtualTableGeometry('newgeom','LineString','4326')
    ft_name = 'my_jdbc_vt_test'
    epsg_code = 'EPSG:4326'
    sql = 'select ST_MakeLine(wkb_geometry ORDER BY waypoint) As newgeom, assetid, runtime from waypoints group by assetid,runtime'
    keyColumn = None
    parameters = None
    
    jdbc_vt = JDBCVirtualTable(ft_name, sql, 'false', geom, keyColumn, parameters)
    ft = cat.publish_featuretype(ft_name, store, epsg_code, jdbc_virtual_table=jdbc_vt)

def enableLayer(cat):
    layer = cat.get_layer("road_wms:test")
    layer.enabled=True
    cat.save(layer)
    cat.reload()


    """
    创建工作区， 需要输入name， 以及uri
    """
def createWorkspace(cat, name, uri):
    if cat.create_workspace(name, uri):
        print("%s workspace create successfully") % name



def publish_featuretype(cat, featureName):
    native_crs = "EPSG:4326"
    store = cat.get_store('myStore')
    featureType = cat.publish_featuretype(featureName, store, native_crs)
    print(featureType)


def create_wmslayer(workspaceName, storeName, name):
     workspace = cat.get_workspace(workspaceName)
     store = cat.get_store(storeName)
     result = cat.create_wmslayer(workspace, store, name)
     print(result)
     
     
def add_data_to_store(storeName, name, dataPath, workspaceName):
    workspace = None
    if workspaceName:        
        workspace = cat.get_workspace(workspaceName)
    store = cat.get_store(storeName)
    shapefile = geoserver.util.shapefile_and_friends(dataPath)   
    cat.add_data_to_store(store, name, shapefile, workspace, charset="UTF-8")


def create_datastore(name, workspaceName):
    workspace = None
    if workspaceName:        
        workspace = cat.get_workspace(workspaceName)
    cat.create_datastore(name, workspace)


if __name__ == "__main__":
     cat = Catalog("http://localhost:8081/geoserver/rest", "admin", "geoserver")  
#    getLayer()

#    createLayer()
#     enableLayer(cat)
#     createWorkspace(cat, "djxc", "www.djxc.com")
#     createStore(cat, "myStore", "Data/region", "djxc")
#     publish_featuretype(cat, "xcfeature")
#     create_wmslayer("djxc", "myStore", "testWMS")
#     stopLayer("cite:test")
     add_data_to_store("myStore", "djFeature", "Data/region", "djxc")
#     create_datastore("myStore", "djxc")
     
     