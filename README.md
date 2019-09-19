# GTFS Realtime Python API

This package makes it easy to poll bus stop information from any transit service that provides [GTFS Realtime](https://developers.google.com/transit/gtfs-realtime/ "GTFS Realtime") data.

### Usage

Simply edit `config.py` to include the URL to the `TripUpdates.pb` file provided by the transit service and place the files `routes.txt` and `stops.txt` from the static GTFS zip (also from the transit service) in the same folder. After that is setup you can call the API like this:

```python
import gtfs

# Get all known upcoming busses to stop id 1820.
for route, time in gtfs.get("1820"):
    print("{}\t{}".format(gtfs.show(time), route))
```

You can also specify which route(s) to get data from:
```python
gtfs.get("1820", "6") # Only route 6
gtfs.get("1820", ["6, 13"]) # Routes 6 or 13
```
Note that all parameters can also be passed as integers for convenience, and will be converted to strings internally. As well, route and stop ids match the transit service's specification and are converted into the GTFS id system using the `.txt` files.
