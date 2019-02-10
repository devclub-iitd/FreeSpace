from tabula import read_pdf
import pandas as pd

room_occupancy =  read_pdf("Room_Occupancy_Chart.pdf",guess=False,pages='1-5') #dataframe created
filter1 = room_occupancy.loc[(room_occupancy["Room"] != "Room") & (room_occupancy["Room"].str.contains("LH"))] #All required data got
rooms =  filter1["Room"].tolist() 

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

intvlist = [8 + x*(19.5 - 8)/23 for x in range(23)] #columns

fd={}
for i in range(0,5): #each day
    d ={}
    for k in range(len(rooms)):
        l = {}
        for j in range(len(intvlist)):
            l[intvlist[j]]=0
        d[rooms[k]] = l
    fd[i] = d

slot_map = {1:[[0,3],[8,8.5,9]],2:[[0,3],[9.5,10,10.5]],3:[[1,2,4],[8,8.5]],4:[[1,2,4],[9,9.5]],5:[[1,2,4],[10,10.5]],6:[[1,3,4],[11,11.5]],7:[[0,2],[11,11.5],[3],[12,12.5]],8:[[0,1,4],[12,12.5]],9:[[1,4],[5,5.5],[2],[12,12.5]],10:[[1,4],[6,6.5]],11:[[0,3],[5,5.5,6]]}

def slotA(dic,room):
    for i in [0,3]: #days
        for j in [8,8.5,9]: 
            dic[i][room][j] = 1

def slot(cs,room_dic,room,slot_dic):
    slot_timings = slot_dic[cs]
    slot_days = slot_timings[0]
    slot_times = slot_timings[1]
    for i in slot_days:
        for j in slot_times:
            room_dic[i][room][j] = 1
    if len(slot_timings)>2:
        slot_days = slot_timings[2]
        slot_times = slot_timings[3]
        for i in slot_days:
            for j in slot_times:
                room_dic[i][room][j] = 1


for index,row in filter1.iterrows():  
    curr_room = row[0]
    for j in range(1,12):
        if (type(row[j])!= float): #notNaN
            slot(j,fd,curr_room,slot_map)
                    
daywise_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday"}

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
    temp_df = pd.DataFrame.from_dict(day_dict,orient = 'index',columns = intvlist)
    final_dict[key] = temp_df
