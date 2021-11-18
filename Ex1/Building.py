class Building:
    """This class represents a building with several floors and elevators."""
    def __init__(self, min_floor: int = 0, max_floor: int = 0, elevators: list = []):
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.elevators = elevators

    """ return the minimal floor in this building. """
    def get_min_floor(self) -> int:
        return self.min_floor

    """ return the maximal floor in this building. """
    def get_max_floor(self) -> int:
        return self.max_floor

    """ return list elevators """
    def get_elevators(self):
        return self.elevators

    """ i the index of the elevator.
      return the i"th elevator. """
    def get_one_elevator(self, i):
        return self.elevators[i]

    """return the number of elevators (1 or more) in this building """
    def number_of_elevators(self):
        return len(self.elevators)

    def __str__(self):
        return "[ min_floor: " + str(self.min_floor) + ", max_floor: " + str(self.max_floor) + str(self.elevators) +"]"