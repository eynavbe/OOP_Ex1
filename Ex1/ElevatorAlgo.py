import json
import csv
import math
from Ex1.Building import Building
from Ex1.CallForElevator import CallForElevator
from Ex1.Elevator import Elevator
from Ex1.MyElevator import MyElevator


class ElevatorAlgo:
    """Places the calls to the appropriate elevator. """
    up, down = 1, -1

    def __init__(self, path_file_json: str = "B2.json", path_file_csv: str = "Calls_a.csv"):
        self.path_file_json = path_file_json
        self.path_file_csv = path_file_csv
        builtins = self.read_json(self.path_file_json)
        calls = self.read_calls_csv(self.path_file_csv)
        self.allocate_an_elevator(calls, builtins)

    """ read file json of building and return object Building """
    def read_json(self, path_file):
        file = open("data/Ex1_Buildings/"+path_file, )
        data = json.load(file)
        min_floor = data["_minFloor"]
        max_floor = data["_maxFloor"]
        builtins_list = []
        for i in data['_elevators']:
            id_b = i["_id"]
            speed = i["_speed"]
            min_floor = i["_minFloor"]
            max_floor = i["_maxFloor"]
            close_time = i["_closeTime"]
            open_time = i["_openTime"]
            start_time = i["_startTime"]
            stop_time = i["_stopTime"]
            elevator = Elevator(id_b, speed, min_floor, max_floor, close_time, open_time, start_time, stop_time)
            builtins_list.append(elevator)
        file.close()
        return Building(min_floor, max_floor, builtins_list)

    """ read file csv of calls and return list of CallForElevator """
    def read_calls_csv(self, path_file):
        calls = []
        file = open("data/Ex1_Calls/"+path_file, )
        csv_reader = csv.reader(file)
        for row in csv_reader:
            name = row[0]
            time = row[1]
            src = row[2]
            dest = row[3]
            state = row[4]
            allocate_elevator = row[5]
            call = CallForElevator(name, float(time), int(src), int(dest), int(state), int(allocate_elevator))
            calls.append(call)
        file.close()
        return calls

    """  write file csv of calls - CallForElevator """
    def write_calls_csv(self, calls_choose):
        path_file_json_new = self.path_file_json.replace(".json", "")
        file = open('data/Ex1_Out/out_'+path_file_json_new+"_"+self.path_file_csv, 'w', encoding='UTF8', newline='')
        writer = csv.writer(file)
        for i in range(len(calls_choose)):
            columns = [c.strip() for c in str(calls_choose[i]).strip(', ').split(',')]
            writer.writerow(columns)
        file.close()

    """  This method is the main optimal allocation algorithm for allocating the"""
    def allocate_an_elevator(self, calls, builtins):
        calls_choose = []
        elev_num = Building.number_of_elevators(builtins)
        my_elevators = []
        my_elevators_copy = []
        for i in range(elev_num):
            my_elevators_copy.append(MyElevator())
        for i in range(elev_num):
            my_elevators.append(MyElevator())
        if elev_num > 0:
            for call in calls:
                if CallForElevator.get_src(call) == CallForElevator.get_dest(call):
                    continue
                if (CallForElevator.get_src(call) > Building.get_max_floor(builtins)) or (CallForElevator.get_src(call) < Building.get_min_floor(builtins)):
                    continue
                if (CallForElevator.get_dest(call) > Building.get_max_floor(builtins)) or (CallForElevator.get_dest(call) < Building.get_min_floor(builtins)):
                    continue
                ans = self.allocate_an_elevator_call_to_elevator(call, elev_num,builtins,my_elevators_copy)
                my_elevators[ans] = my_elevators_copy[ans]
                call_choose = CallForElevator(CallForElevator.get_name(call), CallForElevator.get_time(call), CallForElevator.get_src(call), CallForElevator.get_dest(call), CallForElevator.get_state(call), ans)
                calls_choose.append(call_choose)
                j = 0
                for i in my_elevators:
                    my_elevators_copy[j] = MyElevator(MyElevator.get_list_stops(i), MyElevator.get_list_times(i))
                    j = j + 1
            self.write_calls_csv(calls_choose)

    """  Place the call in all lists copy elevators """
    def allocate_an_elevator_call_to_elevator(self, call, elev_num, builtins, my_elevators_copy):
        for i in range(elev_num):
            self.time(call, my_elevators_copy[i], Building.get_one_elevator(builtins, i))
        ans = self.allocate_an_elevator_choose_elevator(elev_num, my_elevators_copy)
        return ans

    """
    This method selects which elevator the calls will be placed on - 
    according to the smallest time of the elevator after placing the calls in all the elevators
    return:  the index of the elevator to which this call was allocated to
    """
    def allocate_an_elevator_choose_elevator(self, elev_num, my_elevators_copy):
        ans = 0
        if elev_num != (ans + 1):
            for i in range(1, elev_num):
                time_ans = self.final_time(my_elevators_copy[ans])
                time_i = self.final_time(my_elevators_copy[i])
                if time_ans > time_i:
                    ans = i
        return ans

    """ returns the total time of the elevator """
    def final_time(self, my_elevator):
        return MyElevator.get_list_times(my_elevator)[MyElevator.num_of_times(my_elevator) - 1]

    """ puts the call in the right place in the list and updates the time list """
    def time(self, call, my_elevator, this_elevator):
        i = ElevatorAlgo.where_time_call_not_passed(self, call, my_elevator, this_elevator)
        ElevatorAlgo.insert_call_in_lists(self, call, my_elevator, i, this_elevator)

    """ where in the list is the call received - where time call not passed """
    def where_time_call_not_passed(self, call, my_elevator, this_elevator):
        i = 0
        while i < MyElevator.num_of_times(my_elevator) and CallForElevator.get_time(call) > MyElevator.get_list_times(my_elevator)[i]:
            i = i + 1
        if i < MyElevator.num_of_stops(my_elevator)-1:
            i = i + 1
            time_stop1_to_stop2 = math.fabs(MyElevator.get_list_stops(my_elevator)[i] - CallForElevator.get_src(call))/Elevator.get_speed(this_elevator)
            time_now = MyElevator.get_list_times(my_elevator)[i] + time_stop1_to_stop2
            if math.floor(time_now) > math.floor(CallForElevator.get_time(call)):
                i = i - 1
        if i > 0:
            i = i - 1
            time_stop1_to_stop2 = (math.fabs(MyElevator.get_list_stops(my_elevator)[i] - CallForElevator.get_src(call))) / (Elevator.get_speed(this_elevator))
            time_now = MyElevator.get_list_times(my_elevator)[i] + time_stop1_to_stop2
            if math.floor(time_now) < math.floor(CallForElevator.get_time(call)):
                i = i + 1
        if i < MyElevator.num_of_stops(my_elevator):
            if i > 0:
                floor_before = 0
                floor_now = MyElevator.get_list_stops(my_elevator)[i]
                floor_now_time = MyElevator.get_list_times(my_elevator)[i]
                if i > 1:
                    floor_before = MyElevator.get_list_stops(my_elevator)[i-1]
                if CallForElevator.get_time(call) < floor_now_time:
                    if floor_before < floor_now and CallForElevator.get_src(call) <= floor_now and floor_before <= CallForElevator.get_src(call):
                        i = i - 1
                    if floor_before > floor_now and CallForElevator.get_src(call) >= floor_now and floor_before >= CallForElevator.get_src(call):
                        i = i - 1
        return i

    """ insert call in lists - list time and list stops """
    def insert_call_in_lists(self, call, my_elevator, i, this_elevator):
        status = ElevatorAlgo.status_call(self, call)
        copy_stop = []
        list_times = []
        put_src, put_dest, add_src = False, False, True
        for f in MyElevator.get_list_stops(my_elevator):
            copy_stop.append(f)
        for f in MyElevator.get_list_times(my_elevator):
            list_times.append(f)
        k = self.where_start_same_status1(my_elevator, status, i, call)
        until_where_same_status_k = ElevatorAlgo.until_where_same_status(self, my_elevator, k, status)
        if i > 0 and i < MyElevator.num_of_stops(my_elevator):
            floor_now = MyElevator.get_list_stops(my_elevator)[i]
            if CallForElevator.get_src(call) == floor_now:
                put_src = True
                add_src = False
        if k > i:
            g = k
            if k == MyElevator.num_of_stops(my_elevator):
                g = k - 1
            for r in range(i, g):
                floor_now = MyElevator.get_list_stops(my_elevator)[r+1]
                floor_before = MyElevator.get_list_stops(my_elevator)[r]
                if CallForElevator.get_src(call) == floor_now:
                    if CallForElevator.get_time(call) > MyElevator.get_list_times(my_elevator)[r+1]:
                        copy_stop.insert(r + 2, CallForElevator.get_src(call))
                        list_times = self.insert_list_time_stop(r + 2, call, list_times, my_elevator,
                                                                CallForElevator.get_src(call), this_elevator, copy_stop)
                        my_elevator.list_stops = copy_stop
                        my_elevator.list_times = list_times
                        put_src = True
                    else:
                        put_src = True
                        add_src = False
                if floor_before == CallForElevator.get_src(call):
                    if CallForElevator.get_time(call) > MyElevator.get_list_times(my_elevator)[r]:
                        copy_stop.insert(r + 1, CallForElevator.get_src(call))
                        list_times = self.insert_list_time_stop(r + 1, call, list_times, my_elevator,
                                                                CallForElevator.get_src(call), this_elevator, copy_stop)
                        my_elevator.list_stops = copy_stop
                        my_elevator.list_times = list_times
                        put_src = True
                    else:
                        put_src = True
                        add_src = False

                if floor_before < floor_now and CallForElevator.get_src(
                        call) < floor_now and floor_before < CallForElevator.get_src(call):
                    copy_stop.insert(r+1, CallForElevator.get_src(call))
                    list_times = self.insert_list_time_stop(r+1, call, list_times, my_elevator,
                                                            CallForElevator.get_src(call), this_elevator, copy_stop)
                    my_elevator.list_stops = copy_stop
                    my_elevator.list_times = list_times
                    put_src = True

                if floor_before > floor_now and CallForElevator.get_src(
                        call) > floor_now and floor_before > CallForElevator.get_src(call):
                    copy_stop.insert(r + 1, CallForElevator.get_src(call))
                    list_times = self.insert_list_time_stop(r + 1, call, list_times, my_elevator,
                                                            CallForElevator.get_src(call), this_elevator, copy_stop)
                    my_elevator.list_stops = copy_stop
                    my_elevator.list_times = list_times
                    put_src = True
                if r == 0 and put_src == False:
                    if 0 < floor_before and floor_before < CallForElevator.get_src(call):
                        copy_stop.insert(r + 1, CallForElevator.get_src(call))
                        list_times = self.insert_list_time_stop(r + 1, call, list_times, my_elevator,
                                                                CallForElevator.get_src(call), this_elevator, copy_stop)

                        my_elevator.list_stops = copy_stop
                        my_elevator.list_times = list_times
                        put_src = True
                    if 0 > floor_before and floor_before > CallForElevator.get_src(call):
                        copy_stop.insert(r + 1, CallForElevator.get_src(call))
                        list_times = self.insert_list_time_stop(r + 1, call, list_times, my_elevator,
                                                                CallForElevator.get_src(call), this_elevator, copy_stop)

                        my_elevator.list_stops = copy_stop
                        my_elevator.list_times = list_times
                        put_src = True
        if put_src and add_src:
            k = k + 1
            until_where_same_status_k = until_where_same_status_k + 1
        if until_where_same_status_k > 0:
            if CallForElevator.get_src(call) == MyElevator.get_list_stops(my_elevator)[until_where_same_status_k-1]:
                if CallForElevator.get_time(call) < MyElevator.get_list_times(my_elevator)[until_where_same_status_k-1]:
                    put_src = True
                    add_src = False
        if until_where_same_status_k == MyElevator.num_of_stops(my_elevator):
            if not put_src:
                copy_stop.insert(until_where_same_status_k, CallForElevator.get_src(call))
                my_elevator.list_stops = copy_stop
                list_times = self.insert_list_time_stop(until_where_same_status_k, call, list_times, my_elevator, CallForElevator.get_src(call), this_elevator,copy_stop)
                my_elevator.list_times = list_times
                until_where_same_status_k = until_where_same_status_k + 1
                put_src = True
            copy_stop.insert(until_where_same_status_k, CallForElevator.get_dest(call))
            my_elevator.list_stops = copy_stop
            list_times = self.insert_list_time_stop(until_where_same_status_k, call, list_times, my_elevator, CallForElevator.get_dest(call), this_elevator,copy_stop)
            my_elevator.list_times = list_times
            put_dest = True
            return
        if status == self.up:
            for j in range(until_where_same_status_k - k + 1):
                if CallForElevator.get_src(call) == MyElevator.get_list_stops(my_elevator)[k + j]:
                    put_src = True
                    add_src = False
                if CallForElevator.get_src(call) < MyElevator.get_list_stops(my_elevator)[k+j] and put_src == False :
                    copy_stop.insert(k+j, CallForElevator.get_src(call))
                    list_times = self.insert_list_time_stop(k+j, call, list_times, my_elevator, CallForElevator.get_src(call), this_elevator, copy_stop)
                    my_elevator.list_stops = copy_stop
                    my_elevator.list_times = list_times
                    put_src = True
                if CallForElevator.get_dest(call) == MyElevator.get_list_stops(my_elevator)[k + j] and put_src:
                    put_dest = True
                if CallForElevator.get_dest(call) < MyElevator.get_list_stops(my_elevator)[k + j] and put_src and put_dest == False:
                    copy_stop.insert(k + j, CallForElevator.get_dest(call))
                    my_elevator.list_stops = copy_stop
                    list_times = self.insert_list_time_stop(k + j, call, list_times, my_elevator,CallForElevator.get_dest(call), this_elevator,copy_stop)
                    my_elevator.list_times = list_times
                    put_dest = True
            j = until_where_same_status_k - k + 1
            if put_src and add_src and put_dest == False and k + j < MyElevator.num_of_stops(my_elevator):
                if put_src and put_dest == False and CallForElevator.get_dest(call) < MyElevator.get_list_stops(my_elevator)[k + j] :
                    copy_stop.insert(k + j, CallForElevator.get_dest(call))
                    my_elevator.list_stops = copy_stop
                    list_times = self.insert_list_time_stop(k + j, call, list_times, my_elevator,CallForElevator.get_dest(call), this_elevator,copy_stop)
                    my_elevator.list_times = list_times
                    put_dest = True
                if CallForElevator.get_dest(call) == MyElevator.get_list_stops(my_elevator)[k + j]:
                    put_dest = True
                until_where_same_status_k += 1
            if not put_src:
                until_where_same_status_k = until_where_same_status_k + 1
                copy_stop.insert(until_where_same_status_k, CallForElevator.get_src(call))
                my_elevator.list_stops = copy_stop
                list_times = self.insert_list_time_stop(until_where_same_status_k, call, list_times, my_elevator, CallForElevator.get_src(call), this_elevator,copy_stop)
                my_elevator.list_times = list_times
                put_src = True
            if not put_dest:
                until_where_same_status_k = until_where_same_status_k + 1
                copy_stop.insert(until_where_same_status_k, CallForElevator.get_dest(call))
                my_elevator.list_stops = copy_stop
                list_times = self.insert_list_time_stop(until_where_same_status_k, call, list_times, my_elevator, CallForElevator.get_dest(call), this_elevator,copy_stop)
                my_elevator.list_times = list_times
                put_dest = True
        if status == self.down:
            for j in range(until_where_same_status_k - k + 1):
                if CallForElevator.get_src(call) == MyElevator.get_list_stops(my_elevator)[k + j]:
                    put_src = True
                    add_src = False
                if CallForElevator.get_src(call) > MyElevator.get_list_stops(my_elevator)[k + j] and put_src == False:
                    copy_stop.insert(k + j, CallForElevator.get_src(call))
                    list_times = self.insert_list_time_stop(k + j, call, list_times, my_elevator,
                                                            CallForElevator.get_src(call), this_elevator, copy_stop)
                    my_elevator.list_stops = copy_stop
                    my_elevator.list_times = list_times
                    put_src = True
                if CallForElevator.get_dest(call) == MyElevator.get_list_stops(my_elevator)[k + j] and put_src:
                    put_dest = True
                if CallForElevator.get_dest(call) > MyElevator.get_list_stops(my_elevator)[k + j] and put_src and put_dest == False:
                    copy_stop.insert(k + j, CallForElevator.get_dest(call))
                    my_elevator.list_stops = copy_stop
                    list_times = self.insert_list_time_stop(k + j, call, list_times, my_elevator,CallForElevator.get_dest(call), this_elevator,copy_stop)
                    my_elevator.list_times = list_times
                    put_dest = True
            j = until_where_same_status_k - k + 1
            if put_src and add_src and not put_dest and k + j < MyElevator.num_of_stops(my_elevator):
                if CallForElevator.get_dest(call) < MyElevator.get_list_stops(my_elevator)[
                    k + j] and put_src and not put_dest:
                    copy_stop.insert(k + j, CallForElevator.get_dest(call))
                    my_elevator.list_stops = copy_stop
                    list_times = self.insert_list_time_stop(k + j, call, list_times, my_elevator,
                                                            CallForElevator.get_dest(call), this_elevator,
                                                            copy_stop)
                    my_elevator.list_times = list_times
                    put_dest = True
                if CallForElevator.get_dest(call) == MyElevator.get_list_stops(my_elevator)[k + j]:
                    put_dest = True
                until_where_same_status_k += 1
            if put_src == False:
                until_where_same_status_k = until_where_same_status_k + 1
                copy_stop.insert(until_where_same_status_k, CallForElevator.get_src(call))
                my_elevator.list_stops = copy_stop
                list_times = self.insert_list_time_stop(until_where_same_status_k, call, list_times,
                                                        my_elevator, CallForElevator.get_src(call),
                                                        this_elevator, copy_stop)
                my_elevator.list_times = list_times
                put_src = True
            if not put_dest:
                until_where_same_status_k = until_where_same_status_k + 1
                copy_stop.insert(until_where_same_status_k, CallForElevator.get_dest(call))
                my_elevator.list_stops = copy_stop
                list_times = self.insert_list_time_stop(until_where_same_status_k, call, list_times,
                                                        my_elevator, CallForElevator.get_dest(call),
                                                        this_elevator, copy_stop)
                my_elevator.list_times = list_times
                put_dest = True
        return

    """ insert call in list stops """
    def insert_list_time_stop(self, k, call, list_times, my_elevator, floor, this_elevator, copy_stop):
        # time of before pre stop and the now stop
        floor_before = 0
        time_now = CallForElevator.get_time(call)
        if k != 0:
            floor_before = copy_stop[k-1]
        time_stop1_to_stop2 = (math.fabs(floor_before - floor)) / (Elevator.get_speed(this_elevator))
        time_floor = Elevator.get_stop_time(this_elevator) + Elevator.get_start_time(this_elevator) + Elevator.get_open_time(this_elevator) + Elevator.get_close_time(this_elevator)
        if k != 0:
            time_now = MyElevator.get_list_times(my_elevator)[k-1]
            if time_now < CallForElevator.get_time(call):
                time_now = CallForElevator.get_time(call) + time_floor + time_stop1_to_stop2
            else:
                time_now = time_now + time_stop1_to_stop2 + time_floor
        else:
            time_now = 1.3 + time_now + time_stop1_to_stop2 + time_floor
        list_times.insert(k, round(time_now))
        if len(list_times) == 0 or k+1 == len(list_times):
            return list_times
        k = k + 1
        time_stop1_to_stop2 = (math.fabs(copy_stop[k] - floor)) / Elevator.get_speed(this_elevator)
        time_floor = Elevator.get_stop_time(this_elevator) + Elevator.get_start_time(this_elevator) + Elevator.get_open_time(this_elevator) + Elevator.get_close_time(this_elevator)
        time_now = time_now + time_stop1_to_stop2 + time_floor
        list_times[k] = round(time_now)
        j = k
        while j < len(copy_stop)-1:
            time_now = list_times[j]
            time_stop1_to_stop2 = (math.fabs(copy_stop[j] - copy_stop[j + 1])) / Elevator.get_speed(this_elevator)
            time_floor =  Elevator.get_stop_time(this_elevator) + Elevator.get_start_time(
                this_elevator) + Elevator.get_open_time(this_elevator) + Elevator.get_close_time(this_elevator)
            time_now = time_now + time_stop1_to_stop2 + time_floor
            j = j + 1
            list_times[j] = round(time_now)
        return list_times

    """return index where start same status - the status of call and the status of list stops elevator"""
    def where_start_same_status1(self, my_elevator, status, i, call):
        for k in range(MyElevator.num_of_stops(my_elevator) - 1):
            if k+i < MyElevator.num_of_stops(my_elevator)-1 and (ElevatorAlgo.status_2_stops(self, my_elevator, k+i)) == status:
                if status == self.up:
                    if MyElevator.get_list_stops(my_elevator)[k+i] <= CallForElevator.get_src(call):
                        return k+i
                if status == self.down:
                    if MyElevator.get_list_stops(my_elevator)[k+i] >= CallForElevator.get_src(call):
                        return k+i
        return MyElevator.num_of_stops(my_elevator)

    """return the status of call"""
    def status_call(self, call):
        status = self.down
        if CallForElevator.get_src(call) < CallForElevator.get_dest(call):
            status = self.up
        return status

    """return the status of 2 stops"""
    def status_2_stops(self, my_elevator, k):
        status = self.down
        if MyElevator.get_list_stops(my_elevator)[k] < MyElevator.get_list_stops(my_elevator)[k + 1]:
            status = self.up
        return status

    """return until where same status - get status and my_elevator and k (where start same status)"""
    def until_where_same_status(self, my_elevator, k, status):
        if MyElevator.num_of_stops(my_elevator) == 0:
            return 0
        if status == self.down:
            while k < MyElevator.num_of_stops(my_elevator)-1 and MyElevator.get_list_stops(my_elevator)[k] > MyElevator.get_list_stops(my_elevator)[k + 1]:
                k = k + 1
        if status == self.up:
            while k < MyElevator.num_of_stops(my_elevator)-1 and MyElevator.get_list_stops(my_elevator)[k] < MyElevator.get_list_stops(my_elevator)[k + 1]:
                k = k + 1
        return k