import json

# imports added in Lab 3 version
import math
import os
from .graphs import WeightedGraph, dijkstra
from django.conf import settings

import sys
sys.path.append('../lab1/')
import tramdata as td

TRAM_FILE = os.path.join('static/tramnetwork.json')

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
        return float(self.stopdict[stop]['lat']), float(self.stopdict[stop]['lon'])         

    def time_between_stops(self, stop1, stop2):
        return td.time_between_stops(self.linedict, self.timedict, stop1, stop2)

    def distance_between_stops(self, stop1, stop2):
        return td.distance_between_stops(self.stopdict, stop1, stop2)
    
    def lines_via_stop(self, stop):
        return td.lines_via_stop(self.linedict, stop)

    def lines_stop_list(self, line):
        return self.linedict[line]
    
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
        return (min_pos["lat"]), min_pos["lon"], max_pos["lat"], max_pos["lon"]


def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile) as trams:
        tramdict = json.loads(trams.read())
    return TramNetwork(tramdict)


def specialize_stops_to_lines(network):
    spec_network = WeightedGraph()
    spec_network.timedict = network.timedict
    spec_network.distance_between_stops = network.distance_between_stops

    for line in network.all_lines_list():
        i = 0
        stops = network.lines_stop_list(line)
        while i < len(stops)-1:
            stop1 = (stops[i], line)
            stop2 = (stops[i+1], line)
            spec_network.add_edge(stop1, stop2)

            if stop1[0] in spec_network.timedict and stop2[0] in spec_network.timedict[stop1[0]]:                       
                time = spec_network.timedict[stop1[0]][stop2[0]]
                spec_network[stop1][stop2]["time"] = time
            else:
                time = spec_network.timedict[stop2[0]][stop1[0]]
                spec_network[stop1][stop2]["time"] = time
            
            distance = spec_network.distance_between_stops(stop1[0], stop2[0])
            spec_network[stop1][stop2]["distance"] = distance

            i+=1
    for stop1 in spec_network.vertices():
        for stop2 in spec_network.vertices():
            if stop1[0] == stop2[0] and stop1 != stop2:
                spec_network.add_edge(stop1, stop2)
                spec_network[stop1][stop2]["time"] = 1
                spec_network[stop1][stop2]["distance"] = 1


    return spec_network

def specialized_transition_time(spec_network, a, b, changetime=10):
    if a[0] == b[0]:
        return changetime
    else:
        return spec_network[a][b]["time"]

def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    if a[0] == b[0]:
        return changedistance
    else:
        return spec_network[a][b]["distance"]

# G = readTramNetwork()
# sn = specialize_stops_to_lines(G)
# print(specialized_transition_time(sn, ("Chalmers", "8"), ("Angered Centrum", "8")))
# print(specialized_geo_distance(sn, ("Chalmers", "8"), ("Angered Centrum", "8")))