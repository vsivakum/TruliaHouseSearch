from __future__ import unicode_literals
import lxml
from lxml import html
from bs4 import BeautifulSoup as Soup
import urllib
import requests
import io
import sys
import math
import subprocess
import codecs
import xml.etree.ElementTree as ET
ClosetoMAX="yes"
GoodElementarySchoolDistrict="yes"
GoodMiddleSchoolDistrict="yes"
GoodHighSchoolDistrict="yes"
FullBathOnMainLevel="yes"
DenOnMainLevel="yes"
FullBedOnMainLevel="yes"
EndUnit="no"
TownHome="yes"
Condo="no"
SingleFamilyHome="no"
Ranch="no"
ClosetoProvidenceStVincent="no"
ClosetoRamya="no"
ClosetoFriends="no"
min_price=280000
max_price=380000
def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return output 
def TruliaSearch():
  output_file = codecs.open("C:\Python27\outlist1pt2hi.txt",'w','utf-8')
  station_list = []  
  trimet_lat_list = []
  trimet_long_list = []
  with open('C:\Python27\MAX_stations_latlongs.txt','r') as f1:
    for line in f1:
      l1= line.strip()
      if l1 and '#' not in line:  #want to skip blank lines and lines with #
        station = l1.split(',')[0] 
        trimet_lat = l1.split(',')[1] 
        trimet_long = l1.split(',')[2]
        station_list.append(station)
        trimet_lat_list.append(trimet_lat)      
        trimet_long_list.append(trimet_long)
  elemschool_list = []  
  elem_lat_list = []
  elem_long_list = []		
  with open('C:\Python27\ElementarySchools_latlongs.txt','r') as f2:
    for line in f2:
      l2= line.strip()
      if l2 and '#' not in line:  #want to skip blank lines and lines with #
        elemschool = l2.split(',')[0] 
        elem_lat = l2.split(',')[1] 
        elem_long = l2.split(',')[2]
        elemschool_list.append(elemschool)
        elem_lat_list.append(elem_lat)      
        elem_long_list.append(elem_long) 
  StVincent_list = []
  StVincent_lat_list = []
  StVincent_long_list = []  
  with open('C:\Python27\ProvidenceStVincent_latlongs.txt','r') as f3:
    for line in f3:
      l3= line.strip()
      if l3 and '#' not in line:  #want to skip blank lines and lines with #
        StVincent = l3.split(',')[0] 
        StVincent_lat = l3.split(',')[1] 
        StVincent_long = l3.split(',')[2]
        StVincent_list.append(StVincent)
        StVincent_lat_list.append(StVincent_lat)      
        StVincent_long_list.append(StVincent_long)
  RamyaAshok_list = []
  RamyaAshok_lat_list = []
  RamyaAshok_long_list = []  
  with open('C:\Python27\RamyaAshok_latlongs.txt','r') as f4:
    for line in f4:
      l4= line.strip()
      if l4 and '#' not in line:  #want to skip blank lines and lines with #
        RamyaAshok = l4.split(',')[0] 
        RamyaAshok_lat = l4.split(',')[1] 
        RamyaAshok_long = l4.split(',')[2]
        RamyaAshok_list.append(RamyaAshok)
        RamyaAshok_lat_list.append(RamyaAshok_lat)      
        RamyaAshok_long_list.append(RamyaAshok_long) 				
  start_price=min_price
  end_price=min_price
  numtownhomes=0
  numsinglefamilyhomes=0
  numcondos=0
  numunknown=0
  numtotal=0
  for k in range(0,len(station_list)): 
    start_price = min_price
    trimet_lat=trimet_lat_list[k]
    trimet_long=trimet_long_list[k]  
    station = station_list[k]
    min_trimet_lat=float(trimet_lat)-1.8/69
    min_trimet_long=float(trimet_long)-1.8/52
    max_trimet_lat=float(trimet_lat)+1.8/69
    max_trimet_long=float(trimet_long)+1.8/52  
    for j in range(0,20):
      end_price=start_price+5000
      if start_price>max_price-5000:continue
      page1 = requests.get("http://www.trulia.com/for_sale/"+str(min_trimet_lat)+","+str(max_trimet_lat)+","+str(min_trimet_long)+","+str(max_trimet_long)+"_xy/"+str(start_price)+"-"+str(end_price)+"_price")
      print ("http://www.trulia.com/for_sale/"+str(min_trimet_lat)+","+str(max_trimet_lat)+","+str(min_trimet_long)+","+str(max_trimet_long)+"_xy/"+str(start_price)+"-"+str(end_price)+"_price\n")
      tree1 = html.fromstring(page1.text)
      urlsraw = tree1.xpath('//a/@href')
      Numresults = tree1.xpath('//*[@id="listContent"]/div[1]/div/span/text()')
      print str(Numresults[0])
      urls=uniq(urlsraw)
      start_price=start_price+5000
      print "Trimet:"+str(station)
      if str(Numresults[0])=='\n        0 Results      ':continue	  
      for i in range(0,len(urls)):
        if "/property" not in urls[i]:continue
        if "map" in urls[i]:continue
        bonuspt=0
        page = requests.get("http://www.trulia.com"+urls[i])
        tree = html.fromstring(page.text)
        propdesc = tree.xpath('//*[@id="corepropertydescription"]/text()')
        proptype = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[1]/text()')
        price_old = tree.xpath('//*[@id="original_lead_form"]/div[1]/div[1]/div[1]/h1/span/span/text()')
        #soup1 = Soup(urllib.urlopen("http://www.trulia.com"+urls[i]).read(),lxml)	
        soup1 = Soup(page.text)	
        price_mas = soup1.find('span',attrs={"class":"pls","itemprop":"price"})
        price = str(price_mas).replace('<span class=\"pls\" itemprop=\"price\">\n','').replace('\n','').replace('</span>','').replace(' ','').replace('$','').replace('+','').replace(',','')
        houseaddress = tree.xpath('//*[@id="propertyDetails"]/div[2]/div/div[1]/div[2]/h1/span[1]/text()')
        if ' Bedroom' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[7]/text()')):
          Numbedrooms = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[7]/text()')
        if ' Bedroom' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[6]/text()')):
          Numbedrooms = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[6]/text()')
        if ' Bedroom' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[5]/text()')):
          Numbedrooms = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[5]/text()')
        if ' Bedroom' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[4]/text()')):
          Numbedrooms = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[4]/text()')
        if ' Bedroom' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[3]/text()')):
          Numbedrooms = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[3]/text()')
        if ' Bedroom' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[2]/text()')):
          Numbedrooms = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[2]/text()')
        if ' Bedroom' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[1]/text()')):
          Numbedrooms = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[1]/text()')
        if 'Built in ' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[7]/text()')):
          Builtyear = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[7]/text()')
        if 'Built in ' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[6]/text()')):
          Builtyear = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[6]/text()')
        if 'Built in ' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[5]/text()')):
          Builtyear = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[5]/text()')
        if 'Built in ' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[4]/text()')):
          Builtyear = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[4]/text()')
        if 'Built in ' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[3]/text()')):
          Builtyear = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[3]/text()')
        if 'Built in ' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[2]/text()')):
          Builtyear = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[2]/text()')	
        if 'Built in ' in str(tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[1]/text()')):
          Builtyear = tree.xpath('//*[@id="propertyDetails"]/div[2]/ul/li[1]/text()')		  
        text_file = open("C:\Python27\houseaddress.txt", "w")
        text_file.write(''.join(houseaddress).replace("'[","").replace("}'",""))
        text_file.close()
        with codecs.open('C:\Python27\houseaddress.txt','r',encoding='utf-8') as f:
          for line in f:
            l1= line.strip()
            if l1 and '#' not in line:  #want to skip blank lines and lines with #
              houseaddress = l1.split(',')[0] 
        print str(houseaddress),",",str(houseaddress).replace("'[","").replace("}'","")
        #print str(price).replace(',','').replace('$','').replace('+','')
        #str(price).replace(',','').replace('$','')
        print str(Numbedrooms[0]).replace(' Bedrooms','').replace(' Bedroom','')+' bed'
        try:
          print 'Built in '+str(Builtyear[0]).replace('Built in ','')
        except UnboundLocalError:
		  print "No built year listed"  
        try:
          if int(price)<start_price-5000:continue
          if 'Condo' in str(proptype[0]):
            if int(price)>end_price-50000:continue
          if int(price)>end_price:continue
        except ValueError:
		  print "Invalid Price"        
        if int(str(Numbedrooms[0]).replace(' Bedrooms','').replace(' Bedroom',''))<2:continue
        try:		
          if int(str(Builtyear[0]).replace('Built in ',''))<1990:continue
        except UnboundLocalError:
          print "No built year listed"  
        city_list = [' Hillsboro OR',' Beaverton OR',' Portland OR']
        for city in city_list:
          if k<13: 
            if city in (' Beaverton OR',' Portland OR'):
              print str(city)+" "+str(k)+" Ignore "+str(city)
              continue
          elif k>-1 and k<17:
            if city in (' Hillsboro OR',' Portland OR'):
              print str(city)+" "+str(k)+" Ignore "+str(city)
              continue
          elif k>16:
            if city in (' Hillsboro OR',' Beaverton OR'):
              print str(city)+" "+str(k)+" Ignore "+str(city)
              continue		  
          else: print "Computing distance"
          print("https://maps.googleapis.com/maps/api/geocode/xml?address="+str(houseaddress)+str(city)+"&key=AIzaSyCbJWqfymfHr2J6iivAanHF1Cm58N6yy5w")
          geocodepage = requests.get("https://maps.googleapis.com/maps/api/geocode/xml?address="+str(houseaddress)+str(city)+"&key=AIzaSyCbJWqfymfHr2J6iivAanHF1Cm58N6yy5w")
          text_file = codecs.open("C:\Python27\geocodepage.xml", "w")
          text_file.write(str(geocodepage.text))
          text_file.close()
          geocodetree = html.fromstring(geocodepage.text.encode('utf-8'))
          text_file1 = open("C:\Python27\geocodetree.xml", "w")
          text_file1.write(str(geocodetree))
          text_file1.close()
          text_file1 = open("C:\Python27\geocodepage.xml", "r")
          text_file1.close()		
          soupresult = Soup(open("C:\Python27\geocodepage.xml").read(),'lxml')
          houselats = str(soupresult.find('lat')).replace("<lat>","").replace("</lat>","")
          type = str(soupresult.find('type')).replace("<type>","").replace("</type>","")
          houselongs = str(soupresult.find('lng')).replace("<lng>","").replace("</lng>","")
          text_file.close()
          parser = ET.XMLParser(encoding="windows-1252")
          if str(type)!="street_address":continue
          if math.floor(float(str(houselats)))<45: continue
          if math.floor(float(str(houselats)))>45: continue		
          if math.ceil(float(str(houselongs)))<-122: continue
          if math.ceil(float(str(houselongs)))>-122: continue
          print "houselat:"+str(houselats)
          print "houselong:"+str(houselongs)
          text_file = open("C:\Python27\houselatlong.txt", "w")
          text_file.write(str(houselats)+","+str(houselongs))
          text_file.close()		
        with codecs.open('C:\Python27\houselatlong.txt','r',encoding='utf-8') as f:
          for line in f:
            l1= line.strip()
            if l1 and '#' not in line:  #want to skip blank lines and lines with #
              houselat = l1.split(',')[0]
            if l1 and '#' not in line:  #want to skip blank lines and lines with #			  
              houselong = l1.split(',')[1]
        for m in range(0,len(elemschool_list)):
          reflat=elem_lat_list[m]
          reflong=elem_long_list[m]
          elemschool=elemschool_list[m]
          dist = math.sqrt(math.pow(math.fabs(float(houselat)-float(reflat))*69,2)+math.pow(math.fabs(float(houselong)-float(reflong))*52,2))
          print "Distance from "+str(elemschool)+" elementary:"+str(dist)+" miles"
          if float(dist) <=0.5: bonuspt=bonuspt+1
        for n in range(0,len(StVincent_list)):
          reflat=StVincent_lat_list[n]
          reflong=StVincent_long_list[n]
          StVincent=StVincent_list[n]
          dist = math.sqrt(math.pow(math.fabs(float(houselat)-float(reflat))*69,2)+math.pow(math.fabs(float(houselong)-float(reflong))*52,2))         
          print "Distance from "+str(StVincent)+" hospital:"+str(dist)+" miles"
          if float(dist) <=0.5: bonuspt=bonuspt+1	
        for p in range(0,len(RamyaAshok_list)):
          reflat=RamyaAshok_lat_list[p]
          reflong=RamyaAshok_long_list[p]
          RamyaAshok=RamyaAshok_list[p]
          dist = math.sqrt(math.pow(math.fabs(float(houselat)-float(reflat))*69,2)+math.pow(math.fabs(float(houselong)-float(reflong))*52,2))         
          print "Distance from "+str(RamyaAshok)+"'s house:"+str(dist)+" miles"
          if float(dist) <=0.5: bonuspt=bonuspt+1			  
        numtotal=numtotal+1
        if "Single-Family Home" in proptype: numsinglefamilyhomes=numsinglefamilyhomes+1
        if "Townhome" in proptype:numtownhomes=numtownhomes+1
        if "Condo" in proptype:numcondos=numcondos+1
        if "Ranch" in proptype:numranches=numranches+1
        if "Unspecified property type" in proptype:numunknown=numunknown+1
        try:
          print ('PropertyDesc: '+ str(propdesc[0]).strip(),", "+str(proptype[0])+", "+str(price)+" Bonus points:"+str(bonuspt)+":"+str(Numbedrooms[0]).replace(' Bedrooms','').replace(' Bedroom','')+' bed:'+'Built in '+str(Builtyear[0]).replace('Built in ','')+": http://www.trulia.com"+urls[i])		
          output_file.write(str("http://www.trulia.com"+urls[i]).replace('-',' ').replace('OR','OR  redfin + "# of Main Bathrooms"'))
          output_file.write('\n')
        except:
          print "issue with price or year built"		  
    print "Station#"+str(k)+":"+str(station)
  print "Single family homes: ",numsinglefamilyhomes,"Townhomes: ",numtownhomes,"Condos: ",numcondos,"Unknown: ",numunknown,"Total: ",numtotal
  output_file.close()
TruliaSearch()
