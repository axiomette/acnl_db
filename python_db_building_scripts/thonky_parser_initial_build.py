import urllib2
from bs4 import BeautifulSoup


page = "http://www.thonky.com/animal-crossing-new-leaf/list-of-furniture"
insertStatement1 = "UPDATE furniture SET img="
insertStatement2 = " WHERE name=";
insertStatement = insertStatement + " hha1, hha2, hha3, color1, color2, origin, ptval) VALUES ("

response = urllib2.urlopen(page)
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

numItems = len(soup.table)
numEntries = len(soup.tr.next_sibling.next_sibling)

tag = soup.tr
cntr = 1
cntr2 = 0

fout = open("nookipedia_hha_imgs.sql", "wb")

while cntr < numItems:
    ftype = "decorative"
    if tag.td:
        # set temp for easy incrementing
        temp = tag.td
        
        #tag.td.string = name of item
        name = temp.string
        if( (name.find("Lamp")>0) or (name.find("Lantern")>0) or (name.find("Candle")>0) or (name=="Blue Dresser") or (name.find("Light")>0) or (name=="Eiffel Tower") or (name=="Golden Man") or (name=="Golden Woman") or (name=="Sconce") or (name.find("light")>0)):
           ftype = "lighting"
        elif( (name.find("Bed")>0) or (name=="Hammock") or (name=="Lab Bench") or (name=="Weight Bench") or (name.find("Corner")>0) or (name=="High-Jump Mat") ):
            ftype = "bedding"
        elif( (name.find("Chair")>0) or ((name.find("Bench")>0) and not (name=="Lab Bench") and not (name=="Weight Bench")) or (name.find("Sofa")>0)):
            ftype = "seating"
        elif( (name.find("Clock")>0) ):
            ftype = "time keeper"
        elif( (name.find("Wardrobe")>0) or ((name.find("Dresser")>0) and not name=="Blue Dresser")or (name.find("Armoire")>0) or (name.find("Bureau")>0) or (name.find("Vanity")>0) or (name.find("Cabinet")>0) or (name.find("Refrigerator")>0) or name=="Storage Case" or (name.find("Locker")>0)):
            ftype = "storage"

        # increment temp
        temp = temp.next_sibling
        # set buy variable
        buy = temp.string

        #increment temp
        temp = temp.next_sibling
        # set sell variable
        sell = temp.string

        #increment temp
        temp = temp.next_sibling        
        #set color 1
        c1 = temp.string
        if c1 == "none" or c1 == "unknown":
            c1 = "NULL"
        
        #increment temp
        temp = temp.next_sibling        
        #set color 2
        c2 = temp.string
        if c2 == "none" or c2 == "unknown":
            c2 = "NULL"
        
        #increment temp
        temp = temp.next_sibling
        #set hha theme
        hha1 = temp.string
        hha2 = "NULL"
        hha3 = "NULL"
        if hha1 == "none" or hha1 == "unknown":
            hha1 = "NULL"
        elif hha1.find(', ') > 0:
            numInstances = hha1.count(', ')
            if numInstances == 2:
                hha1, hha2, hha3 = hha1.split(', ')
            elif numInstances:
                hha1, hha2 = hha1.split(', ')

        #increment temp twice - the next one is style and idgaf
        temp = temp.next_sibling.next_sibling
        # set origin
        origin = temp.string

        string = insertStatement + '"%s", "%s", %d, %d, "%s", "%s", "%s", "%s", "%s", "%s", 151);' %(name, ftype, int(buy), int(sell), hha1, hha2, hha3, c1, c2, origin)
        
        fout.write(string + '\r\n')
       
       #cntr2 = 0
       #while cntr2 < numEntries:
        #   fout.write(temp.string)
         #  temp = temp.next_sibling
          # cntr2 = cntr2 + 1
          
    tag = tag.next_sibling.next_sibling
    cntr = cntr + 2

fout.close()
