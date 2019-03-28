
# coding: utf-8

# In[38]:


from bs4 import BeautifulSoup
import requests
import pprint
import re
import datetime
import pandas as pd
import os
import shutil
import sys
NO_OF_WEEKS_TO_SCRAPE=2

if (len(sys.argv) == 3):
    NO_OF_WEEKS_TO_SCRAPE=int(sys.argv[2])


# In[39]:


room_df_dict = {}


# In[3]:


cookie={
    "PHPSESSID":(sys.argv[1])
}
url="http://roombooking.iitd.ac.in/book/" #add br(i) to this

req_header = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://roombooking.iitd.ac.in',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://roombooking.iitd.ac.in/book/book_room',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

capacity = '1' #minimum capacity allows show of all rooms
rci = '0' #room category id
uniq_room_list = [] # The list of all rooms
# The table shown starts from max((input_date - 3),(today+1))
#So intervals must be tomorrow;tomorrow+7+3;...
date_list = []
n = datetime.datetime.now()
for i in range(NO_OF_WEEKS_TO_SCRAPE):
    n = datetime.datetime.now()+datetime.timedelta(days=(i*7+4))
    date_list.append(str(n.year)+"-"+str(n.month)+"-"+str(n.day))  

br1 = "book_room"
br2 = "show_rooms?capacity="+capacity+"&room_category_id="+rci


# In[4]:


w = requests.get(url+br2,cookies=cookie,headers=req_header,data={'capacity':capacity,'room_category_id':rci})
room_list = w.text
match = r"LH [0-9]{3}"
pattern = re.compile(match)
dup_room_list = pattern.findall(room_list)
for i in dup_room_list:
    if i not in uniq_room_list:
        uniq_room_list.append(i)


# In[5]:


data = {'capacity':capacity, 'room_category_id':rci, 'room_no':'','date':''}


# In[6]:


def data_cleaner(needed_table):
    l=needed_table.find_all('tr')
    for k in l:
        m = k.find_all('td')
        if (m == []):
            m = k.find_all('th')
        else:
            for z in m:
                if (z.a['class'][0] == "alloted"):
                    cont = z.a['title']
                    z.a.append(cont[:6])
                    del z.a["title"]
                elif (z.a['class'][0] == "available"):
                    z.a.append("Free")
                    del z.a["id"]
                else:
                    z.a.append("Not Allowed")
                    del z.a["title"]
                    del z.a["id"]
    return needed_table


# In[42]:


with requests.Session() as s:
    for i in date_list: #Take a date
        for j in uniq_room_list: #Take a room
            data['room_no']=j
            data['date']=i
            r = requests.post(url=(url+br1),cookies=cookie,headers=req_header,data=data)
            soup = BeautifulSoup(r.content, features="lxml")
            
            all_tables = soup.find_all('table')
            actual_table = all_tables[1]
            cleaned = data_cleaner(actual_table)
            to_str_cleaned = str(cleaned)
            df = pd.read_html(to_str_cleaned)[0]
            dic = df.to_dict('list')
            if (j not in room_df_dict):
                room_df_dict[j]=dic
            else:
                room_df_dict[j].update(dic)

    


# In[44]:


def getTimeList(room_df_dict):
    return room_df_dict[list(room_df_dict.keys())[0]]['Time']


# In[45]:


def getRoomList(room_df_dict):
    l= list(room_df_dict.keys())
    l = [x.lstrip("LH") for x in l]
    l.sort()
    l = ["LH"+x for x in l]
        
    return l


# In[46]:


def getDayList(room_df_dict):
    return list((room_df_dict[list(room_df_dict.keys())[0]]).keys())[1:]


# In[47]:


#room_df_dict is of the format Room:{Day1/Time:[Course1,Course2,...],Day2/Time:[...]}
#The function must return Day:{Room:[Course1,Course2,...]}
def freeRoomsPerDay(room_df_dict):
    dic_to_return= {}
    rooms_list=getRoomList(room_df_dict)
    days_list=getDayList(room_df_dict)
    for currDay in days_list:
        dic_ele={}
        for currRoom in rooms_list:
            courses_list=room_df_dict[currRoom][currDay]
            dic_ele[currRoom]=courses_list
        dic_to_return[currDay]=dic_ele
    return dic_to_return    


# In[54]:


def dirStructureSet(room_df_dict):
    
    try:
        os.mkdir("dayWiseTables")
    except FileExistsError:
        pass
    finally:
        try:
            os.mkdir("smallTables")
        except FileExistsError:
            pass
        finally:
            for i in getDayList(room_df_dict):
                pattern = re.compile(r'[0-9]{4}-[0-9]{1,2}-([0-9]{1,2})\((.*)\)')
                m = pattern.findall(i)
                try:
                    os.mkdir("smallTables/"+(m[0][0]).lstrip("0")+(m[0][1]))
                except FileExistsError:
                    shutil.rmtree("smallTables/"+(m[0][0]).lstrip("0")+(m[0][1]))
                    os.mkdir("smallTables/"+(m[0][0]).lstrip("0")+(m[0][1]))


# In[55]:


def createDFfromDictLarge(new_room_df_dict,old_room_df_dict,folder):
    for i in list(new_room_df_dict.keys()):
        currDay=new_room_df_dict[i]
        df_from_dict=pd.DataFrame.from_dict(currDay,orient='index',columns=getTimeList(old_room_df_dict))
        pattern = re.compile(r'[0-9]{4}-[0-9]{1,2}-([0-9]{1,2})\((.*)\)')
        m = pattern.findall(i)
        df_from_dict.to_html(folder+"/"+(m[0][0]).lstrip("0")+(m[0][1])+".html")


# In[56]:


def createDFfromDictSmall(new_room_df_dict,folder):
    for i in list(new_room_df_dict.keys()):
        currDay=new_room_df_dict[i]
        for j in list(currDay.keys()):
            currTime=currDay[j]
            pattern = re.compile(r'[0-9]{4}-[0-9]{1,2}-([0-9]{1,2})\((.*)\)')
            m = pattern.findall(i)
            df_from_dict=pd.DataFrame.from_dict({i:currTime},orient='columns')
            df_from_dict.to_html(folder+"/"+(m[0][0]).lstrip("0")+(m[0][1])+"/"+(j).lstrip("0")+".html")


# In[57]:


# Of the format Day:{Time:[Free_room1,Free_room2,...]}
def roomsPerHour(room_df_dict):
    dic_to_return={}
    rooms_list=getRoomList(room_df_dict)
    days_list=getDayList(room_df_dict)
    time_list=getTimeList(room_df_dict)
    for j in days_list:
        ele ={}
        for i in time_list:
            ele[i]=[]
        dic_to_return[j]=ele
#     print (room_df_dict)
    for currDay in days_list:
        for currRoom in rooms_list:
            for i in range(len(time_list)):
                currTime=time_list[i]
                if (room_df_dict[currRoom][currDay][i] == 'Free'):
                    dic_to_return[currDay][currTime].append(currRoom)
    return dic_to_return


# In[58]:


tl=getTimeList(room_df_dict)
d1=freeRoomsPerDay(room_df_dict)
d2=roomsPerHour(room_df_dict)
dirStructureSet(room_df_dict)
createDFfromDictLarge(d1,room_df_dict,"dayWiseTables")
createDFfromDictSmall(d2,"smallTables")
