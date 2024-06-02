import datetime
import time
from autoplayer.scheduler import Scheduler


s = Scheduler("test_tasks", datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 50)))

# Usage
while s.has_tasks():
    s.scheduler.run(blocking=False)
    time.sleep(1) 
