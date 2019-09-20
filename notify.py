import os
import sys
from time import sleep
from datetime import datetime, timedelta
import gtfs

dt = timedelta(minutes=int(sys.argv[1]))
if len(sys.argv) > 2:
  cmd = " ".join(sys.argv[2:])
else:
  cmd = None

while True:
  gtfs.fetch()
  for route, time in gtfs.get(1820, [13, 6]):
    if datetime.utcnow() + dt > time:
      print(gtfs.show(time) + "\t" + route)
      if cmd:
        os.system(cmd.replace("{}", route + ": " + gtfs.show(time)))
      sys.exit(0)
  sleep(60)
