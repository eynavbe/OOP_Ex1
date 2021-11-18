class Elevator:
    """This class of an Elevator - the information with which the calls is placed"""
    def __init__(self, id_b: int = 0, speed: float = 0.0, min_floor: int = 0, max_floor: int = 0, close_time: float = 0.0, open_time: float = 0.0, start_time: float = 0.0, stop_time: float = 0.0):
        self.id_b = id_b
        self.speed = speed
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.close_time = close_time
        self.open_time = open_time
        self.start_time = start_time
        self.stop_time = stop_time

    """Returns the id"""
    def get_id(self) -> int:
        return self.id_b

    """Returns the speed (in floor per second)"""
    def get_speed(self) -> float:
        return self.speed

    """Returns the minimal floor number to which this Elevator can reach"""
    def get_min_floor(self) -> int:
        return self.min_floor

    """ Returns the maximal floor number to which this Elevator can reach """
    def get_max_floor(self) -> int:
        return self.max_floor

    """Returns the time (in seconds it takes the Elevator to close its doors"""
    def get_close_time(self) -> float:
        return self.close_time

    """ Returns the time in seconds it takes the Elevator to open its doors."""
    def get_open_time(self) -> float:
        return self.open_time

    """Return the time in seconds that it takes the elevator to start moving in full speed """
    def get_start_time(self) -> float:
        return self.start_time

    """Return the time in seconds that it takes the elevator to stop moving in full speed"""
    def get_stop_time(self) -> float:
        return self.stop_time

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[ id: " + str(self.id_b) + ", speed: " + str(self.speed) + ", min_floor: " + str(self.min_floor) +\
               ", max_floor: " + str(self.max_floor) + ", close_time: " + str(self.close_time) + ", open_time: " \
               + str(self.open_time) + ", start_time: " + str(self.start_time) + ", stop_time: " + str(self.stop_time) + "]"
