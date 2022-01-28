# You have to calculate a device's 'uptime %', as the % of time, since a given date until now, during which it was
# online

from asyncio import events
from datetime import datetime, timedelta
from enum import Enum
from time import time
from typing import List


class Status(str, Enum):
    UP = 'UP'
    DOWN = 'DOWN'


class StatusChange:
    def __init__(self, new_status: Status, timestamp: datetime):
        self.new_status = new_status
        self.timestamp = timestamp

#                         #
#   FIRST IMPLEMENTATION  #
#                         #   

# def calculate_uptime(current_status: Status, status_changes: List[StatusChange], since: datetime) -> float:
#     # You can do the following assumptions about data:
#     # - statuses alternate correctly; you won't have two UPs or DOWNs in sequence
#     # - timestamps are sorted from the oldest to the newest
#     # - timestamps are all > 'since' and < datetime.now()

#     # edge cases: 0 % and 100%
#     if current_status == Status.UP and status_changes==[]:
#         return 100.0
#     elif current_status ==Status.DOWN and status_changes==[]:
#         return 0.0
#     else:
#         #check if current status matches last change - this if can be avoided
#         if status_changes != []:
#             assert current_status==status_changes[-1].new_status, "Last state change does not match current status!"

#         #Total elapsed time
#         totTime=(datetime.now()-since).total_seconds()

#         #initialize two empty seconds counters, to be filled with the alternating intervals
#         even=0
#         odd=0
#         current=since #initialize left extreme of interval

#         for i, stat in enumerate(status_changes):
#             if i%2==0:
#                 even+=(stat.timestamp-current).total_seconds()#/3600 #add time interval
#                 current=stat.timestamp                              #update left extreme
#                 lastUpdate='even'    
#             else:
#                 odd+=(stat.timestamp-current).total_seconds()#/3600 #add time interval
#                 current=stat.timestamp                             #update left extreme 
#                 lastUpdate='odd'
#         #ADD last interval 
#         if lastUpdate == 'even':
#             odd+=(datetime.now()-current).total_seconds()#/3600
#         elif lastUpdate =='odd':
#             even += (datetime.now() - current).total_seconds()#/3600

#         #Assign even and odd to up or down    ##it can probably be shortened
#         if current_status==Status.UP and lastUpdate=='even':
#             #uptime=odd
#             uptime=100*odd/totTime
#             return round(uptime, 2)   #rounding for the assertions below
#         elif current_status==Status.UP and lastUpdate=='odd':
#             #uptime=even
#             uptime=100*even/totTime
#             return round(uptime, 2)
#         elif current_status==Status.DOWN and lastUpdate=='even':
#             #downtime=odd
#             downtime=100*odd/totTime
#             return round(100.0 - downtime, 2)
#         else: # down and odd
#             #downtime==even
#             downtime=100*even/totTime
#             return round(100.0 - downtime, 2)



#                         #
#      REFACTORING        #
#                         #
def calculate_uptime(current_status: Status, status_changes: List[StatusChange], since: datetime) -> float:
    # You can do the following assumptions about data:
    # - statuses alternate correctly; you won't have two UPs or DOWNs in sequence
    # - timestamps are sorted from the oldest to the newest
    # - timestamps are all > 'since' and < datetime.now()
    #    
    #edge cases: 100% and 0% uptime
    if len(status_changes)==0:
        if current_status == Status.UP:
            return 100.0
        else:
            return 0.0
    #total elapsed time        
    totTime=(datetime.now()-since).total_seconds()
    #error check
    assert current_status==status_changes[-1].new_status, "Last state change does not match current status!"
    #initialize sum of time intervals
    intervalSum=0
    current=since #initialize left extreme of interval
    #set parity of intervals needed 
    parity = len(status_changes)%2 #0 for even, 1 for odd
    #add intervals to intervalSum
    for i, stat in enumerate(status_changes):
        if i%2 == parity: #takes even i if parity==odd else takes odd i
            intervalSum+=(stat.timestamp-current).total_seconds() #add time interval
        current=stat.timestamp                             #update left extreme 
    #add last interval to sum
    intervalSum+=(datetime.now()-current).total_seconds()
    #return uptime - chose interval w.r.t. current status
    if current_status==Status.UP:        
        return round(100*intervalSum/totTime, 2)
    else:
        return round(100*(totTime-intervalSum)/totTime, 2)


#          #
# EXAMPLES # 
#          # 
#
#|------------------------| represents the 24 hours time interval betwen SINCE and now
# each dash represents one hour, U and D are the status changes 

SINCE = datetime.now() - timedelta(hours=24)
# 25% uptime |------------------U------|  6 hours up ---> 25% uptime
EVENT_UP = datetime.now() - timedelta(hours=6)
test_list=[StatusChange(new_status='UP', timestamp=EVENT_UP)]
# 75% uptime |------------------D------|  18 hours up ---> 75% uptime 
test_list2=[StatusChange(new_status='DOWN', timestamp=EVENT_UP)]
# 50% uptime |------D------------U------|
EVENT_DOWN= datetime.now() - timedelta(hours=18)
test_list3=[StatusChange(new_status='DOWN', timestamp=EVENT_DOWN), StatusChange(new_status='UP', timestamp=EVENT_UP)]
# print(EVENT_UP, EVENT_DOWN)

###test 4 |-D---U------------------D--|  19 hours up ---> 79.17% uptime
ED1=datetime.now() - timedelta(hours=23)
EU1=datetime.now() - timedelta(hours=20)
ED2=datetime.now() - timedelta(hours=2)

test_list4=[StatusChange(new_status='DOWN', timestamp=ED1),\
            StatusChange(new_status='UP', timestamp=EU1),\
            StatusChange(new_status='DOWN', timestamp=ED2)]

####test 5 |D----U-----------------D--|    18 hours up ----> 75.0% uptime
ED1_5=datetime.now() - timedelta(hours=24)
EU1_5=datetime.now() - timedelta(hours=20)
ED2_5=datetime.now() - timedelta(hours=2)

test_list5=[StatusChange(new_status='DOWN', timestamp=ED1_5),\
            StatusChange(new_status='UP', timestamp=EU1_5),\
            StatusChange(new_status='DOWN', timestamp=ED2_5)]

####test 6: Down and Up at the same time |-DU--------------------D--|    22 hours up ----> 91.67% uptime
ED1_6=datetime.now() - timedelta(hours=23) 
EU1_6=datetime.now() - timedelta(hours=23)
ED2_6=datetime.now() - timedelta(hours=2)

test_list6=[StatusChange(new_status='DOWN', timestamp=ED1_6),\
            StatusChange(new_status='UP', timestamp=EU1_6),\
            StatusChange(new_status='DOWN', timestamp=ED2_6)]

####test 7: |-D-----U-------D---------U--|   10 hours up ---->    41.67% 
ED1_7=datetime.now() - timedelta(hours=23) 
EU1_7=datetime.now() - timedelta(hours=18)
ED2_7=datetime.now() - timedelta(hours=11)
EU2_7=datetime.now() - timedelta(hours=2)


test_list7=[StatusChange(new_status='DOWN', timestamp=ED1_7),\
            StatusChange(new_status='UP', timestamp=EU1_7),\
            StatusChange(new_status='DOWN', timestamp=ED2_7),\
            StatusChange(new_status='UP', timestamp=EU2_7)]


if __name__ == "__main__":
    print("Implement some cases")
    assert calculate_uptime('UP', [], None)==100.0
    assert calculate_uptime('DOWN', [], None)==0.0
    assert calculate_uptime("UP", test_list, SINCE) == 25.0, calculate_uptime("UP", test_list, SINCE)
    assert calculate_uptime("DOWN", test_list2, SINCE) == 75.0, calculate_uptime("DOWN", test_list2, SINCE)
    assert calculate_uptime('UP', test_list3, SINCE) == 50.0, calculate_uptime('UP', test_list3, SINCE)
    assert calculate_uptime('DOWN', test_list4, SINCE) == 79.17, calculate_uptime('DOWN', test_list4, SINCE)
    assert calculate_uptime('DOWN', test_list5, SINCE) == 75.0, calculate_uptime('DOWN', test_list5, SINCE)
    assert calculate_uptime('DOWN', test_list6, SINCE) == 91.67, calculate_uptime('DOWN', test_list6, SINCE)
    assert calculate_uptime('UP', test_list7, SINCE) == 41.67, calculate_uptime('UP', test_list7, SINCE)

    # calculate_uptime('DOWN', test_list7, SINCE)
