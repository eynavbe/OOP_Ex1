import unittest
import csv
import json
from Ex1.ElevatorAlgo import ElevatorAlgo


class MyTestCase(unittest.TestCase):
    """ creat 10 calls for elevator"""
    with open("data\Ex1_Calls\call_test.csv", "w", newline='') as f:
        wCall = csv.writer(f)
        wCall.writerow(["call0 ", "13.89 ", "3 ", "0 ", "0 ", "-1"])
        wCall.writerow(["call1 ", "14.02 ", "2 ", "1 ", "0 ", "-1"])
        wCall.writerow(["call2 ", "15.0 ", "1 ", "8 ", "0 ", "-1"])
        wCall.writerow(["call3 ", "15.65 ", "7 ", "9 ", "0 ", "-1"])
        wCall.writerow(["call4 ", "15.9 ", "10 ", "0 ", "0 ", "-1"])
        wCall.writerow(["call5 ", "17.3 ", "9 ", "10 ", "0 ", "-1"])
        wCall.writerow(["call6 ", "18.0 ", "2 ", "11 ", "0 ", "-1"])
        wCall.writerow(["call7 ", "22.156 ", "2 ", "5 ", "0 ", "-1"])
        wCall.writerow(["call8 ", "83.56 ", "1 ", "0 ", "0 ", "-1"])
        wCall.writerow(["call9 ", "100.10 ", "5 ", "9 ", "0 ", "-1"])
    f.close()

    """  creat new building with one elevator"""
    building0 = {"_minFloor": 0, "_maxFloor": 10, "_elevators": [
        {
            "_id": 0,
            "_speed": 1.0,
            "_minFloor": 0,
            "_maxFloor": 10,
            "_closeTime": 2.0,
            "_openTime": 2.0,
            "_startTime": 3.0,
            "_stopTime": 3.0
        }
     ]
    }

    """  creat new building with 2 elevators"""
    building1 = {"_minFloor": 0, "_maxFloor": 10, "_elevators": [
        {
            "_id": 0,
            "_speed": 1.0,
            "_minFloor": 0,
            "_maxFloor": 10,
            "_closeTime": 2.0,
            "_openTime": 2.0,
            "_startTime": 3.0,
            "_stopTime": 3.0
        },
        {
            "_id": 1,
            "_speed": 2.0,
            "_minFloor": 0,
            "_maxFloor": 10,
            "_closeTime": 2.0,
            "_openTime": 2.0,
            "_startTime": 3.0,
            "_stopTime": 3.0
        }
     ]
    }
    with open("data/Ex1_Buildings/building0_test.json", "w") as b0:
        json.dump(building0, b0)
    b0.close()

    with open("data/Ex1_Buildings/building1_test.json", "w") as b1:
        json.dump(building1, b1)
    b1.close()
    
    """  test allocation with one Elevator"""
    def test_ElevatorAlgo0(self):
        ElevatorAlgo("building0_test.json", "call_test.csv")
        with open('data\Ex1_Out\out_building0_test_call_test.csv', 'r') as myFile:
            result_algo = csv.reader(myFile)
            my_list = list(result_algo)
        myFile.close()

        self.assertEqual(my_list[0][5], "0")
        self.assertEqual(my_list[1][5], "0")
        self.assertEqual(my_list[2][5], "0")
        self.assertEqual(my_list[3][5], "0")
        self.assertEqual(my_list[4][5], "0")
        self.assertEqual(my_list[5][5], "0")
        self.assertEqual(my_list[6][5], "0")
        self.assertEqual(my_list[7][5], "0")
        self.assertEqual(my_list[8][5], "0")

    """  test allocation with 2 Elevator"""
    def test_ElevatorAlgo1(self):
        ElevatorAlgo("building1_test.json", "call_test.csv")
        with open('data\Ex1_Out\out_building1_test_call_test.csv', 'r') as myFile:
            result_algo = csv.reader(myFile)
            my_list = list(result_algo)
        myFile.close()

        self.assertEqual(my_list[0][5], "1")
        self.assertEqual(my_list[1][5], "0")
        self.assertEqual(my_list[2][5], "0")
        self.assertEqual(my_list[3][5], "1")
        self.assertEqual(my_list[4][5], "1")
        self.assertEqual(my_list[5][5], "0")
        self.assertEqual(my_list[6][5], "0")
        self.assertEqual(my_list[7][5], "1")
        self.assertEqual(my_list[8][5], "0")


if __name__ == '__main__':
    unittest.main()
