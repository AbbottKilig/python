from urllib.parse import quote
import urllib.request
import json
import math
import  re
import string

a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率



def getUid(name):
    wd = urllib.parse.quote(data)
    weburl = "http://map.baidu.com/?qt=s&wd=" + wd + "&c=131"
    response = urllib.request.urlopen(weburl)
    alljson = json.loads(response.read().decode('utf-8'))
    uid = alljson['result']['profile_uid']
    print(uid)
    return uid
def getBD09MC(uid):
    dataurl = "http://map.baidu.com/?newmap=1&qt=ext&uid=" + uid + "&c=131&ext_ver=new&l=13"
    response = urllib.request.urlopen(dataurl)
    alljson = json.loads(response.read().decode('utf-8'))
    geo = alljson['content']['geo']
    index = geo.find("|1-")
    lonlat = geo[index + 3:len(geo) - 1]
    strlist = lonlat.split(',')
    mylist = []
    for i in range(len(strlist)//2 - 1):
        x = strlist[2*i]
        y = strlist[2*i+1]
        mylist.append((x,y))
    return mylist

def BD_MCToLL(point):
    weburl = "http://api.map.baidu.com/geoconv/v1/?coords="+point+"&from=6&to=5&ak=CC4e2cbafba46e5409e4f371e443b152"
    response = urllib.request.urlopen(weburl)
    alljson = json.loads(response.read().decode('utf-8'))
    result = alljson['result']
    x = result[0]['x']
    y = result[0]['y']
    return (x,y)

def getBD09LLFromBD09MC(points):
    pointlist = []
    for point in points:
        strings = str(point[0]) + ',' + point[1]
        covertedPoint = BD_MCToLL(strings)
        pointlist.append(covertedPoint)
    return pointlist



def WGS2GCJ(lng,lat):
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return mglng,mglat
def merchatorTolonLat(mercator_x,mercator_y):
    x = mercator_x/20037508.34*180;
    y = mercator_y/20037508.34*180;
    y = 180 / math.pi * (2 * math.atan(math.exp(y * math.pi / 180)) - math.pi / 2);
    return (x,y)
def bd09ToGcj02(bd_lon,bd_lat):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0;
    x = bd_lon - 0.0065;
    y = bd_lat - 0.006;
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi);
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi);
    gg_lng = z * math.cos(theta);
    gg_lat = z * math.sin(theta);
    #print(gg_lng)
    #print(gg_lat)
    return (gg_lng, gg_lat)
def gcj02_to_wgs84(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return (lng * 2 - mglng, lat * 2 - mglat)

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret
def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret
def out_of_china(lng, lat):
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

def BD09ToGCJ02(points):
    pointlist=[]
    for point in points:
        convertedPoint = bd09ToGcj02(point[0],point[1])
        pointlist.append(convertedPoint)
    return  pointlist

def GCJ02ToWGS84(points):
    pointlist = []
    for point in points:
        convertedPoint = gcj02_to_wgs84(point[0],point[1])
        pointlist.append(convertedPoint)
    return pointlist

def writeTofile(filename,list):
    with open(filename+'.txt','w') as file:
        for mytuple in  list:
            #print(mytuple)
            file.write(str(mytuple[0])+","+str(mytuple[1])+"\n")



datas=['三里屯','西二旗','西三旗','回龙观']
for data in datas:
    uid = getUid(data)
    print(data +'---'+uid)
    points = getBD09MC(uid)
    pointlist = getBD09LLFromBD09MC(points)
    pointlist = BD09ToGCJ02(pointlist)
    pointlist = GCJ02ToWGS84(pointlist)
    writeTofile(data,pointlist)

