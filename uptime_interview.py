# You have to calculate a device's 'uptime %', as the % of time, since a given date until now, during which it was
# online

from datetime import datetime, timedelta
from enum import Enum
from typing import List


class Status(str, Enum):
    UP = 'UP'
    DOWN = 'DOWN'


class StatusChange:
    def __init__(self, new_status: Status, timestamp: datetime):
        self.new_status = new_status
        self.timestamp = timestamp


def calculate_uptime(current_status: Status, status_changes: List[StatusChange], since: datetime) -> float:
    # You can do the following assumptions about data:
    # - statuses alternate correctly; you won't have two UPs or DOWNs in sequence
    # - timestamps are sorted from the oldest to the newest
    # - timestamps are all > 'since' and < datetime.now()
    #
#     pass
    #100% alwys up
    if current_status == Status.UP and status_changes==[]:
        return 100.0
    elif current_status ==Status.DOWN and status_changes==[]:
        return 0
    else:
        totaltime=datetime.now()-since
        downtime=status_changes[0].timestamp-since
        uptime=100*((totaltime-downtime).total_seconds()/totaltime.total_seconds())
        if current_status==Status.UP:
            return uptime
        else:
            return 100.0 - uptime

SINCE = datetime.now() - timedelta(hours=24)
EVENT_UP = datetime.now() - timedelta(hours=6)
test_list=[StatusChange(new_status='UP', timestamp=EVENT_UP)]

test_list2=[StatusChange(new_status='DOWN', timestamp=EVENT_UP)]

if __name__ == "__main__":
    print("Implement some cases")
    assert calculate_uptime('UP', [], None)==100.0
    assert calculate_uptime('DOWN', [], None)==0
    assert calculate_uptime("UP", test_list, SINCE) == 25.0, calculate_uptime("UP", test_list, SINCE)
    assert calculate_uptime("DOWN", test_list2, SINCE) == 75.0, calculate_uptime("DOWN", test_list2, SINCE)