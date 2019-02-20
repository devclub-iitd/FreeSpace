from tabula import read_pdf
import pandas as pd
# from collections import OrderedDict

#room_occupancy =  read_pdf("Room_Occupancy_Chart.pdf", guess= False, pages='1-5') #dataframe created
room_occupancy =  read_pdf("http://roombooking.iitd.ac.in/allot/files/Room_Occupancy_Chart.pdf", guess=False, pages='1-5') #dataframe created
filter1 =room_occupancy.loc[(room_occupancy["Room"] != "Room") & (room_occupancy["Room"].str.contains("LH"))] #All required data got
rooms =filter1["Room"].tolist()

'''
A Slot: Mon and Thurs -> 8:00  to 9:30
B Slot: Mon and Thurs -> 9:30  to 11:00
C Slot: Tue, Wed, Fri -> 8:00  to 9:00
D Slot: Tue, Wed, Fri -> 9:00  to 10:00
E Slot: Tue, Wed, Fri -> 10:00 to 11:00
F Slot: Tue, Thurs, Fri -> 11:00 to 12:00
H Slot: Mon, Wed -> 11:00 to 12:00, Thurs -> 12:00 to 1:00
J Slot: Mon, Tue, Fri -> 12:00 to 1:00
K Slot: Tue, Fri -> 5:00 to 6:00, Wed -> 12:00 to 1:00
L Slot: Tue, Fri -> 6:00 to 7:00
M Slot: Mon, Thurs -> 5:00 to 6:30
'''
def dec_to_time(i):
    if i%1 == 0.5:
        return(str(int(i//1))+ ":30")
    else:
        return(str(int(i//1))+ ":00")

intvlist = [8 + x*(19.5 - 8)/23 for x in range(23)] #columns
intvllist2 = []
for i in intvlist:
    intvllist2.append(dec_to_time(i))

fd={}
for i in range(0,5): #each day
    d ={}
    for k in range(len(rooms)):
        l = {}
        for j in range(len(intvlist)):
            l[intvlist[j]]=0
        d[rooms[k]] = l
    fd[i] = d

slot_map = {1:[[0,3],[8.0,8.5,9.0]],2:[[0,3],[9.5,10.0,10.5]],3:[[1,2,4],[8.0,8.5]],4:[[1,2,4],[9.0,9.5]],5:[[1,2,4],[10.0,10.5]],6:[[1,3,4],[11.0,11.5]],7:[[0,2],[11.0,11.5],[3],[12.0,12.5]],8:[[0,1,4],[12.0,12.5]],9:[[1,4],[17.0,17.5],[2],[12.0,12.5]],10:[[1,4],[18.0,18.5]],11:[[0,3],[17.0,17.5,18.0]]}

daywise_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday"}

def slot(cs,room_dic,room,slot_dic,class_going_on):
    slot_timings = slot_dic[cs]
    slot_days = slot_timings[0]
    slot_times = slot_timings[1]
    for i in slot_days:
        for j in slot_times:
            room_dic[i][room][float(j)] = class_going_on
    if len(slot_timings)>2:
        slot_days = slot_timings[2]
        slot_times = slot_timings[3]
        for i in slot_days:
            for j in slot_times:
                room_dic[i][room][float(j)] = class_going_on

dict_2= {} #rows are timings and columns are days so each key will be timings & value will be a list
#with each index corresponding to the day and the data inside will be string
for i in intvllist2:
    dict_2[i] = ["","","","",""]

for index,row in filter1.iterrows():  
    curr_room = row[0]
    for j in range(1,12):
        if (type(row[j])!= float): #notNaN
            slot(j, fd, curr_room, slot_map, row[j])
        else: #Add this curr room to a table with time as row and days as columns
            got_slot = slot_map[j] #nested list of days,timings. This slot is empty for the room
            days_for_this_slot_1 = got_slot[0]
            timings_for_this_slot_1 = got_slot[1]
            for i in days_for_this_slot_1:
                for j in timings_for_this_slot_1:
                    # if j in dict_2: #list already initialized with epthy strings
                    dict_2[dec_to_time(j)][i] += curr_room+","
                    # else:
                    #     dict_2[j] = ["","","","",""]
            if len(got_slot) > 2:
                days_for_this_slot_2 = got_slot[2]
                timings_for_this_slot_2 = got_slot[3]
                for i in days_for_this_slot_1:
                    for j in timings_for_this_slot_1:
                        dict_2[ dec_to_time(j)][i] += curr_room+","


timewise_df = pd.DataFrame.from_dict(dict_2,orient='index',columns=["Monday","Tuesday","Wednesday","Thursday","Friday"])
old_width = pd.get_option('display.max_colwidth')
pd.set_option('display.max_colwidth', -1)
timewise_df.to_html("timewise.html")
pd.set_option('display.max_colwidth', old_width)

                    

final_dict = {} # Day: corresponding dataframe

for i in range(5):
    day_dict ={} #room : list of bools in time series
    key = daywise_dict[i]
    room_list = fd[i]
    
    for curr_room in rooms:
        l = []
        timings = room_list[curr_room] #will return a dictionary
        for time in intvlist:
            bool_value = timings[time]
            l.append(bool_value)
        day_dict[curr_room] = l
    #day dict is now a dictionary of type room:list
    temp_df = pd.DataFrame.from_dict(day_dict,orient = 'index',columns = intvllist2)
    temp_df.to_html(key+".html")
    # temp_df.to_json(key+".json")
    final_dict[key] = temp_df



