from datetime import datetime, timedelta
import csv
import requests
import gtfs_realtime_pb2 as gtfs
import config

r_name_id = {}
r_id_name = {}
stops = {}
feed = None

def fetch():
  global r_id_name, feed
  with open("routes.txt") as f:
    reader = csv.DictReader(f)
    for row in reader:
      r_name_id[row["route_short_name"].lstrip("0")] = row["route_id"]
  r_id_name = {v:k for k, v in r_name_id.items()}

  with open("stops.txt") as f:
    reader = csv.DictReader(f)
    for row in reader:
      stops[row["stop_code"]] = row["stop_id"]

  r = requests.get(config.url)
  feed = gtfs.FeedMessage.FromString(r.content) # pylint: disable=E1101

def get(stop, routes=None):
  fetch()
  stop = stops[str(stop)]
  if routes is not None:
    if not isinstance(routes, list):
      routes = [routes]
    routes = [r_name_id[str(route)] for route in routes]

  times = []
  for e in feed.entity:
    if routes is None or e.trip_update.trip.route_id in routes:
      route = r_id_name[e.trip_update.trip.route_id]
      for s in e.trip_update.stop_time_update:
        if s.stop_id == stop:
          time = datetime.utcfromtimestamp(s.arrival.time)
          if time < datetime.utcnow():
            continue
          times.append((route, time))

  times.sort(key=lambda t: t[1])
  return times

def main():
  # print stop times for routes 6 and 13 at stop 1820
  for route, time in get(1820, [6, 13]):
    print(show(time) + "\t" + route)

def show(time):
  time -= timedelta(hours=4)
  return time.strftime("%I:%M %p ").lstrip("0")

if __name__ == '__main__':
  main()
