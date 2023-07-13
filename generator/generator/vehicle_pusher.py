file_path = "../local/map_xuhui.json"

import json
import itertools
json_roadnet = json.load(open(file_path))
intersections = json_roadnet["intersections"]
virtual = [x['id'] for x in intersections if x['virtual']]
# print(intersections)

roads = json_roadnet["roads"]
start_roads = [x['id'] for x in roads if x['startIntersection'] in virtual]
end_roads = [x['id'] for x in roads if x['endIntersection'] in virtual]
roads_name = [x['id'] for x in roads]

od_pair = list(itertools.product(roads_name, roads_name))

# for x in od_pair:
import random
od_pair_sample = random.sample(od_pair, 500)
print(len(od_pair))

vehicle_template = {
    "length": 5.0,
    "width": 2.0,
    "maxPosAcc": 2.0,
    "maxNegAcc": 4.5,
    "usualPosAcc": 2.0,
    "usualNegAcc": 4.5,
    "minGap": 2.5,
    "maxSpeed": 16.67,
    "headwayTime": 1.5
}

flow = [
    {
        "vehicle": vehicle_template,
        "route":x,
        "interval": 50.0,
        "startTime": random.randint(0,100),
        "endTime": -1
    }
    for x in od_pair_sample
]

json.dump(flow, open("../local/flow_xuhui.json", "w"))