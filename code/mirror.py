#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os
import urllib2
import sys
from BeautifulSoup import BeautifulSoup
from wand.image import Image


def ConvertImage(oldfilename):
	with Image(filename=oldfilename+'.jpg') as img:
	    img.format = 'png'
	    img.save(filename=oldfilename+'.png')


def download_photo(img_url, filename):
    #file_path = "%s%s" % (DOWNLOADED_IMAGE_PATH, filename)
    #downloaded_image = file(file_path, "wb")
    downloaded_image = file(filename, "wb")

    req = urllib2.Request(img_url, headers={'User-Agent' : "Magic Browser"}) 
    image_on_web = urllib2.urlopen(req)
    while True:
        buf = image_on_web.read(65536)
        if len(buf) == 0:
            break
        downloaded_image.write(buf)
    downloaded_image.close()
    image_on_web.close()

    return 1

def parseing(url,id,ResultList):
	pDict={}
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	con = urllib2.urlopen( req )
	html = con.read()
	#print html

	soup = BeautifulSoup(html)

	images = soup.findAll('img', {'class':'img-responsive screengrab'})
	#for image in images:
	#	print image.get('src')
	image_url = 'https://worldofvnc.net/' + images[0].get('src')
	download_photo(image_url,str(id)+'.jpg')
  	ConvertImage(str(id))
	pDict.update({'image_url':image_url})
	pDict.update({'local_image_name':str(id)+'.png'})

	

	listdata= soup.findAll('li', {'class':'list-group-item'})
	for x in listdata:
		#print x.b.contents[0], x.contents[1]
		pDict.update({x.b.contents[0]:x.contents[1]})

	ResultList.append(pDict)
	#dataDict.update({'VPN_ID':str(id), 'VPN_Content':pDict})
	#print "inner data" 
	#print ResultList


  	return ResultList



if __name__ == "__main__":

	#total data is 3567 now 
	ResultList=[]
	for ID in range(1,3567+1):
		print "paring %s...." % ID
		url='https://worldofvnc.net/browse.php?id=' + str(ID)
		ResultList = parseing(url,ID,ResultList)
		#print "outer data"
		#print ResultList
	print 'final'	
	print ResultList

	sys.exit(0)


