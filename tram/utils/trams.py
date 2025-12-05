import json

# imports added in Lab 3 version
import math
import os
from .graphs import WeightedGraph
from django.conf import settings

TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')


# TODO: use your Lab 2 class definition, but add one method
# class TramNetwork(WeightedGraph):    
    # def extreme_positions(self):
        # stops = self._stopdict.values()
        # minlat = min([s._position[0] for s in stops])
        # etc
        # return minlat, minlon, maxlat, maxlon

class TramNetwork(WeightedGraph):
    def __init__(self, tramdict):
        super().__init__()
        self.stopdict = tramdict["stops"]
        self.linedict = tramdict["lines"]
        self.timedict = tramdict["times"]
        for stop in self.stopdict:
            self.add_vertex(stop)
        for line, stops in self.linedict.items():
            i = 0
            while i < len(stops)-1:
                self.add_edge(stops[i], stops[i+1])
                i+=1
        for stop1, stops in self.timedict.items():
            for stop2, time in stops.items():
                self.set_weight(stop1, stop2, time)

    def stop_geo_pos(self, stop):
        return self.stopdict[stop]        

    def time_between_stops(self, stop1, stop2):
        return td.time_between_stops(self.linedict, self.timedict, stop1, stop2)

    def distance_between_stops(self, stop1, stop2):
        return td.distance_between_stops(self.stopdict, stop1, stop2)
    
    def lines_via_stop(self, stop):
        return td.lines_via_stop(self.linedict, stop)

    def lines_stop_list(self, line):
        return linedict[line]
    
    def all_stops_list(self):
        return list(stop for stop in self.stopdict)
    
    def all_lines_list(self):
        return list(line for line in self.linedict)

    def extreme_positions(self):
        min_pos = {
            "lat" : float("inf"),
            "lon" : float("inf")
        }
        max_pos = {
            "lat" : float("-inf"),
            "lon" : float("-inf")
        }
        for stop, pos in self.stopdict.items():
            for attr, val in pos.items():
                if float(val) < min_pos[attr]:
                    min_pos[attr] = float(val)
                if float(val) > max_pos[attr]:
                    max_pos[attr] = float(val)
        return min_pos["lat"], min_pos["lon"], max_pos["lat"], max_pos["lon"]


def readTramNetwork():
    # TODO: your own trams.readTramNetwork()
    pass


def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance

