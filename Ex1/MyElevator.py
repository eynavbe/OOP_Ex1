class MyElevator:
    """This class realizes the list of elevators stop, and list of times. """
    def __init__(self, list_stops: list = [], list_times: list = []):
        self.list_stops = list_stops
        self.list_times = list_times

    """This methods return the list of elevators stop"""
    def get_list_stops(self):
        return self.list_stops

    """This methods return the list of elevators times stop"""
    def get_list_times(self):
        return self.list_times

    """This methods return the length list of elevators times stop"""
    def num_of_stops(self):
        return len(self.list_stops)

    """This methods return the length list of elevators stop"""
    def num_of_times(self):
        return len(self.list_times)

    def __str__(self):
        return "[ list_stops: " + str(self.list_stops) + " ,list_times: " + str(self.list_times) + "]"