import os
import json
import random
import itertools
random.seed(123)

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


    def sort_road(self):

        for road in self.list_in_roads:
            index = road['id'].split("_")
            if index[-1] == '0':
                self.dict_in_roads['W'] = road['id']
            elif index[-1] == '1':
                self.dict_in_roads['S'] = road['id']
            elif index[-1] == '2':
                self.dict_in_roads['E'] = road['id']
            elif index[-1] == '3':
                self.dict_in_roads['N'] = road['id']
            else:
                raise Exception('Wrong road!')

        self.list_in_roads = []
        for direct in ['N','E','S','W']:
            self.list_in_roads.append(self.dict_in_roads[direct])


        for road in self.list_out_roads:
            index = road['id'].split("_")
            if index[-1] == '0':
                self.dict_out_roads['E'] = road['id']
            elif index[-1] == '1':
                self.dict_out_roads['N'] = road['id']
            elif index[-1] == '2':
                self.dict_out_roads['W'] = road['id']
            elif index[-1] == '3':
                self.dict_out_roads['S'] = road['id']
            else:
                raise Exception('Wrong road!')

        self.list_out_roads = []
        for direction in ['N', 'E', 'S', 'W']:
            self.list_out_roads.append(self.dict_out_roads[direction])

    def generate_false_pair(self):
        self.sort_road()

        del_inter_pair = []

        for i in range(len(self.list_in_roads)):
            del_inter_pair.append((self.list_in_roads[i], self.list_out_roads[i]))

        del_inter_pair.extend(list(itertools.product(self.list_in_roads, self.list_in_roads)))
        del_inter_pair.extend(list(itertools.product(self.list_out_roads, self.list_out_roads)))

        #del_inter_pair.append((self.list_in_roads[0], self.list_out_roads[1]))
        #del_inter_pair.append((self.list_in_roads[1], self.list_out_roads[2]))
        #del_inter_pair.append((self.list_in_roads[2], self.list_out_roads[3]))
        #del_inter_pair.append((self.list_in_roads[3], self.list_out_roads[0]))

        return del_inter_pair


    def generate_turn_right_pair(self):

        del_inter_pair = []

        del_inter_pair.append((self.list_in_roads[2], self.list_out_roads[1]))
        del_inter_pair.append((self.list_in_roads[3], self.list_out_roads[2]))
        del_inter_pair.append((self.list_in_roads[0], self.list_out_roads[3]))
        del_inter_pair.append((self.list_in_roads[1], self.list_out_roads[0]))

        return del_inter_pair


def flow_generator(roadmap, density, balance, dist_type,speed):

    roadnet_file_name = 'roadnet_' + roadmap +'.json'
    roadnet_path = os.path.join("../Datasets", roadmap, roadnet_file_name)
    log_dir = os.path.join("../Datasets", roadmap)

    with open(roadnet_path) as f:
        roadnet = json.load(f)

    non_virtual_inters = [i for i in roadnet["intersections"] if not i["virtual"]]

    inters = []
    for i in range(len(non_virtual_inters)):
        inters.append(Inters(non_virtual_inters[i]))

    all_inters = [i["id"] for i in non_virtual_inters]
    id2inters = {i.id: i for i in inters}

    # allocate roads
    for road in roadnet["roads"]:
        iid = road["startIntersection"]
        if iid in all_inters:
            id2inters[iid].insert_road(road, "out")
        iid = road["endIntersection"]
        if iid in all_inters:
            id2inters[iid].insert_road(road, 'in')

    del_pair = []

    flase_pair = []
    turn_right_pair = []
    for i in inters:
        flase_pair.extend(i.generate_false_pair())
        turn_right_pair.extend(i.generate_turn_right_pair())

    print("single turn right pair:",len(turn_right_pair))

    '''
    list(set(turn_right_pair))
    print(len(turn_right_pair))

    print(turn_right_pair)

    print("all turn right pair:", len(turn_right_pair))
    #print(len(turn_right_pair))


    '''

    del_pair.extend(flase_pair)
    del_pair.extend(turn_right_pair)

    del_pair.append(('road_1_0_1,road_2_1_3'))
    del_pair.append(('road_2_2_3,road_1_1_1'))


    start_roads = []
    end_roads = []
    for i in inters:
        start_roads.extend(i.list_in_roads)
        end_roads.extend(i.list_out_roads)

    start_roads = list(set(start_roads))
    end_roads = list(set(end_roads))

    od_pair = list(itertools.product(start_roads, end_roads))

    print("total pairs:", len(od_pair))

    for pair in od_pair:
        if pair[0] == pair[1]:
            od_pair.remove(pair)

    for pair in del_pair:
        try:
            od_pair.remove(pair)
        except:
            pass


    #print(od_pair)
    print("final pairs:",len(od_pair))


    if not balance:
        direction_pair = []
        for pair in od_pair:
            start = pair[0].split("_")
            end = pair[1].split("_")

            if start[-1] == '0' and end[-1]== '0':
                direction_pair.append(pair)

        for _ in range(len(od_pair)):
            for pair in direction_pair:
                od_pair.append(pair)

    flow = []
    if dist_type == 'uni':

        for i in range (density):

            route = random.sample(od_pair,1)
            time = random.randint(0,3600)

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
            time = int(random.gauss(0,1) * 1200  + 1800)
            if time >3600:
                time = 3600
            elif time <0:
                time = 0

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



def run():

    roadmap_list = ['1x2']
    density_list = [3500]
    speed_list = [8.88, 11.11, 16.67,]
    balance_list = [True,False]
    dist_list = ['uni','gau']

    for roadmap in roadmap_list:
        for balance in balance_list:
            for dist_type in dist_list:
                for density in density_list:
                    for speed in speed_list:
                        flow_generator(roadmap, density, balance, dist_type,speed)


def one():
    roadmap = '1x3'
    density = 2400
    balance = True
    speed = 11.11
    dist = 'uni'

    flow_generator(roadmap, density, balance, dist, speed)


if __name__ == '__main__':
    run()
    #one()