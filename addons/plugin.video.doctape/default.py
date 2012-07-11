#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmcaddon,base64,json,os,re,math
from urllib import urlopen, quote

pluginhandle = int(sys.argv[1])
settings = xbmcaddon.Addon(id='plugin.video.doctape')
translation = settings.getLocalizedString

if settings.getSetting("hd_videos") == "1":
    playHD = True
else:
    playHD = False

url = 'https://my.doctape.com'

def secondsToTimeMarks(secs):
    secs = int(secs)
    h = math.floor(secs / (60 * 60))
    divm = secs % (60 * 60)
    m = math.floor(divm / 60)
    divs = divm % 60
    s = math.floor(divs)
    return str(int(h)).zfill(2) + ":" + str(int(m)).zfill(2) + ":" + str(int(s)).zfill(2)


def addList(name,data):
    jsondata = json.loads(data[8])
    name = re.sub(r'\.[^\.]+$', '', name)
    ok=True
    
    if jsondata['definition'] == 'hd':
        backgroundFile = url+'/doc/'+data[6]+'/poster_1280.jpg'+session
        if playHD:
            videoFile = url+'/doc/'+data[6]+'/video_1280.mp4'+session
        else:
            videoFile = url+'/doc/'+data[6]+'/video_640.mp4'+session      
    else:
        backgroundFile = url+'/doc/'+data[6]+'/poster_640.jpg'+session
        videoFile = url+'/doc/'+data[6]+'/video_640.mp4'+session

    iconFile = url+'/doc/'+data[6]+'/poster_640.jpg'+session
    
    if jsondata['duration'] == "0":
        duration = "N/A"
    else:
        duration = secondsToTimeMarks(jsondata['duration'])

    u=videoFile
    
    liz=xbmcgui.ListItem(name, iconImage=iconFile, thumbnailImage=iconFile)
    liz.setInfo( type="video", infoLabels={ "Duration": duration } )
    liz.setProperty('IsPlayable', 'true')
    liz.setProperty('Fanart_Image', backgroundFile)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    return ok


def listVideos(docs):
    for i in docs:
        if i[7] == 'video':
            try:
                addList(i[2],i)
            except ValueError:
                print "ERR: " + i[2]
    xbmcplugin.endOfDirectory(pluginhandle)


def getVideos():
    request = urllib2.Request(url+'/doc'+session)
    opener = urllib2.build_opener()
    f = opener.open(request)
    j = json.load(f,'utf-8')
    f.close()
    docs =  j['aaData']
    
    # sort docs by timestampt
    docs = sorted(docs, key=lambda k: k[5])
    docs.reverse()
    return docs


def getSession():
    if settings.getSetting("token"):
        authUrl = '/auth?dtsession=' + settings.getSetting("token")
    else:
        authUrl = '/auth'   
    data = {
        'email': settings.getSetting('user_email'),
        'password': settings.getSetting('user_password')
    }
    data = urllib.urlencode(data)
    req = urllib2.Request(url+authUrl, data)
    response = urllib2.urlopen(req)
    cookie = response.info().getheader('Set-Cookie')
    session = urllib.quote( cookie.split(';')[0][3:] )
    settings.setSetting("token", session)
    return '?dtsession=' + session


def start():
    global session, videodocs
    if not settings.getSetting("firstrun") or settings.getSetting("user_email") == "" or settings.getSetting("user_password") == "":
        settings.setSetting("firstrun", '1')
        settings.openSettings()
        xbmc.executebuiltin("Container.Refresh")
    else:
        session = getSession()
        listVideos(getVideos())

start()