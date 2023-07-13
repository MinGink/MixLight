
import os
import json
import random
import itertools
import numpy as np
random.seed(666)
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns



class Inters():

    def __init__(self,inter):

        self.inter = inter
        self.id = inter["id"]


        # road
        self.list_in_roads= []     #NESW
        self.list_out_roads = []   #NESW

        self.dict_in_roads = {}
        self.dict_out_roads = {}

    def insert_road(self, road, type=None):

        if type == 'in':
            self.list_in_roads.append(road)
        elif type == "out":
            self.list_out_roads.append(road)
        else:
            print("Error: Type Wrong!")
            raise NotImplementedError




    def del_pair(self):
        start_roads = [x['id'] for x in self.list_out_roads]
        end_roads = [x['id'] for x in self.list_in_roads]

        del_pair = list(itertools.product(start_roads, end_roads))
        return del_pair





def flow_generator(roadmap, density, balance, dist_type,speed):

    roadnet_file_name = 'roadnet_' + roadmap +'.json'
    roadnet_path = os.path.join("../Datasets", roadmap, roadnet_file_name)
    log_dir = os.path.join("../Datasets", roadmap)

    with open(roadnet_path) as f:
        roadnet = json.load(f)

    intersections = roadnet["intersections"]
    virtual = [x for x in intersections if x['virtual']]
    virtual_id = [i["id"] for i in virtual]
    roads = roadnet["roads"]

    start_roads = [x['id'] for x in roads if x['startIntersection'] in virtual_id]
    end_roads = [x['id'] for x in roads if x['endIntersection'] in virtual_id]

    od_pair = list(itertools.product(start_roads, end_roads))

    print("origin pairs:",len(od_pair))




    inters = []
    for i in range(len(virtual)):
        inters.append(Inters(virtual[i]))

    id2inters = {i.id: i for i in inters}

    # allocate roads
    for road in roadnet["roads"]:
        iid = road["startIntersection"]
        if iid in virtual_id:
            id2inters[iid].insert_road(road, "out")
        iid = road["endIntersection"]
        if iid in virtual_id:
            id2inters[iid].insert_road(road, 'in')


    false_pair = []
    for i in inters:
        false_pair.extend(i.del_pair())

    final_pair = [x for x in od_pair if x not in false_pair]




    #print(od_pair)
    print("final pairs:",len(final_pair))


    if not balance:
        EW_pair = []
        NS_pair = []
        for pair in final_pair:
            start = pair[0].split("_")
            end = pair[1].split("_")

            if start[-1] == '0' and end[-1]== '0':
                EW_pair.append(pair)
            elif start[-1] == '2' and end[-1]== '2':
                EW_pair.append(pair)
            elif start[-1] == '1' and end[-1]== '1':
                NS_pair.append(pair)
            elif start[-1] == '3' and end[-1]== '3':
                NS_pair.append(pair)
            else:
                pass

        rest_pair = [x for x in final_pair if x not in EW_pair]
        #rest_pair = [x for x in rest_pair if x not in NS_pair]


        assert len(final_pair) == len(rest_pair) + len(EW_pair)

        #print(len(final_pair))
        print(len(EW_pair))
        print(len(NS_pair))
        print(len(rest_pair))
        rest_pair.extend(random.sample(EW_pair, 18))
        rest_pair.extend(random.sample(NS_pair,18))

        #assert len(final_pair) == len(rest_pair)
        final_pair = rest_pair






    flow = []
    data_dist = []

    if dist_type == 'uni':

        for i in range (density):

            route = random.sample(od_pair,1)
            time = random.randint(0,3600)

            data_dist.append(time)

            vehicle_template = {
                "length": 5.0, #random.sample([5.0, 10.0, 20.0], 1)[0],
                "width": 2.0,
                "maxPosAcc": 2.0,
                "maxNegAcc": 4.5,
                "usualPosAcc": 2.0,
                "usualNegAcc": 4.5,
                "minGap": 2.5,
                "maxSpeed": speed,#random.sample([11.11, 16.67], 1)[0],
                "headwayTime": 2.0 #random.sample([1.5, 2.0], 1)[0]
            }


            vehicle_flow ={
                            "vehicle": vehicle_template,
                            "route": route[0],
                            "interval": 5,
                            "startTime": time,
                            "endTime": time
            }
            flow.append(vehicle_flow)

    elif dist_type == 'gau':


        for i in range(density):
            route = random.sample(od_pair, 1)
            time = int(random.gauss(1800,600))

            if time >3600:
                time = 3600
            elif time <0:
                time = 0

            #f = open(os.path.join('dataset_time.csv'), 'a+')
            #f.write("{0},{1},\n".format(i,time))
            #f.close()

            data_dist.append(time)

            vehicle_template = {
                "length": 5.0, #random.sample([5.0, 10.0, 20.0], 1)[0],
                "width": 2.0,
                "maxPosAcc": 2.0,
                "maxNegAcc": 4.5,
                "usualPosAcc": 2.0,
                "usualNegAcc": 4.5,
                "minGap": 2.5,
                "maxSpeed": 11.11,#random.sample([11.11, 16.67], 1)[0],
                "headwayTime": 2.0 #random.sample([1.5, 2.0], 1)[0]
            }

            vehicle_flow = {
                "vehicle": vehicle_template,
                "route": route[0],
                "interval": 5,
                "startTime": time,
                "endTime": time
            }
            flow.append(vehicle_flow)

    else:
        raise Exception('wrong distribution type!')


    if balance:
        flow_file = "flow_" + dist_type +'_' + str(density) +'_'+str(speed) + ".json"
    else:
        flow_file = "im_flow_" + dist_type + '_' + str(density) +'_'+str(speed) + ".json"

    flow_path = os.path.join(log_dir, flow_file)

    json.dump(flow, open(flow_path, "w"),indent=4)
    print(flow_path)
    print("File{} generated successfully!!!".format(flow_file))

    data_dist = np.array(data_dist)
    print(data_dist)
    fig = sns.displot(data_dist)
    #fig = fig.get_figure()
    fig.savefig('output.png')







def one():
    roadmap = '3x4' # 3x4 18  4x4 32  4X5 36
    density = 3000
    speed = 11.11


    balance_list = [True, False]
    dist_list = ['uni','gau']

    for balance in balance_list:
        for dist in dist_list:
            flow_generator(roadmap, density, balance, dist, speed)


if __name__ == '__main__':
    one()