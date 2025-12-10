# visualization of shortest path in Lab 3, modified to work with Django

from .trams import readTramNetwork, specialize_stops_to_lines, specialized_geo_distance, specialized_transition_time
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings
from django.core.files.storage import default_storage

def show_shortest(dep, dest):
    network = readTramNetwork()
    spec_network = specialize_stops_to_lines(network)

    dep_line = network.lines_via_stop(dep)[0]
    dest_line = network.lines_via_stop(dest)[0]

    quickest = dijkstra(spec_network, (dep, dep_line), 
                        cost=lambda u, v: specialized_transition_time(spec_network, u, v))[(dest, dest_line)]
    shortest = dijkstra(spec_network, (dep, dep_line),
                        cost=lambda u, v: specialized_geo_distance(spec_network, u, v))[(dest, dest_line)]

    for dep_line in network.lines_via_stop(dep):
        for dest_line in network.lines_via_stop(dest):
            test_quickest = dijkstra(spec_network, (dep, dep_line), 
                        cost=lambda u, v: specialized_transition_time(spec_network, u, v))[(dest, dest_line)]
            test_shortest = dijkstra(spec_network, (dep, dep_line),
                        cost=lambda u, v: specialized_geo_distance(spec_network, u, v))[(dest, dest_line)]
            if len(test_quickest) < len(quickest):
                quickest = test_quickest
            if len(test_shortest) < len(shortest):
                shortest = test_shortest

    time = 0
    i = 0
    while i < len(quickest)-1:
        stop1 = quickest[i]
        stop2 = quickest[i+1]
        time += specialized_transition_time(spec_network, stop1, stop2)
        i+=1

    distance = 0
    i = 0
    while i < len(shortest)-1:
        stop1 = shortest[i]
        stop2 = shortest[i+1]
        distance += specialized_geo_distance(spec_network, stop1, stop2)
        i+=1

    strs_quickest = [" - ".join(stop) for stop in quickest]
    strs_shortest = [" - ".join(stop) for stop in shortest]
    

    timepath = f'Quickest: {', '.join(strs_quickest)}, {time} minutes'
    geopath = f'Shortest: {', '.join(strs_shortest)}, {distance} km'

    shortest = [info.split("-")[0].strip() for info in strs_shortest]
    quickest = [info.split("-")[0].strip() for info in strs_quickest]

    def colors(v):
        if v in shortest and v in quickest:
            return "cyan"
        elif v in shortest:
            return 'green'
        elif v in quickest:
            return 'orange'
        else:
            return 'white'

    # build dynamic file name from arguments, safely
    dep_safe = default_storage.get_valid_name(dep)
    dest_safe = default_storage.get_valid_name(dest)
    outfile_unique_name = f"shortest_path_{dep_safe}_{dest_safe}.svg"

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    infile = os.path.join(settings.BASE_DIR, 'tram/templates/tram/images/gbg_tramnet.svg')
    outfile = os.path.join(settings.BASE_DIR, f'tram/templates/tram/images/generated/{outfile_unique_name}')
    color_svg_network(infile, outfile, colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath, outfile
