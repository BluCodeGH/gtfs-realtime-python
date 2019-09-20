import os
import sys
from time import sleep
from datetime import datetime, timedelta
import gtfs

dt = timedelta(minutes=int(sys.argv[1]))
start = datetime.utcnow() + timedelta(minutes=int(sys.argv[2]))
if len(sys.argv) > 3:
  cmd = " ".join(sys.argv[3:])
else:
  cmd = None

double = False
while True:
  gtfs.fetch()
  for route, time in gtfs.get(1820, [13, 6]):
    if datetime.utcnow() + dt > time > start:
      print(gtfs.show(time) + "\t" + route)
      if not double:
        double = True
        break
      if cmd:
        os.system(cmd.replace("{}", route + ": " + gtfs.show(time)))
      sys.exit(0)
  else:
    double = False
    sleep(60)
    continue
  sleep(30)
