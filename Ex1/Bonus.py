import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from Ex1.ElevatorAlgo import ElevatorAlgo
from Ex1.MyElevator import MyElevator
matplotlib.use('TkAgg')
"""A graphical simulation that shows the movement of elevators in relation to requests in GUI """


def main():
    ElevatorAlgo("B2.json", "Calls_a.csv")
    calls = ElevatorAlgo.my_elevators
    calls1 = MyElevator.get_list_stops(calls[0])
    calls2 = MyElevator.get_list_stops(calls[1])
    size = len(min(MyElevator.get_list_stops(calls[0]), MyElevator.get_list_stops(calls[1])))
    for i in range(size):
        plt.clf()
        plt.axis([0, 3, -3, 11])
        x = int(calls1[i])
        y = int(calls2[i])
        data = pd.DataFrame({"elevator 1": [x, x + 1], "elevator 2": [y, y + 1]})
        data.boxplot()
        plt.pause(0.5)
    plt.show()


if __name__ == "__main__":
    main()