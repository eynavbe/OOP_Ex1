class CallForElevator:
    """This class represents a call for an elevator - with a dedicated destination """
    def __init__(self, name: str = "Elevator", time: float = 0.0, src: int = 0, dest: int = 0, state: int = 0, allocate_elevator: int = 0):
        self.name = name
        self.state = state
        self.allocate_elevator = allocate_elevator
        self.src = src
        self.dest = dest
        self.time = time

    """ returns the name of call """
    def get_name(self) -> str:
        return self.name

    """ returns this call current state. """
    def get_state(self) -> int:
        return self.state

    """This methods return the index of the Elevator in the building to which this call was assigned to"""
    def get_allocate_elevator(self) -> int:
        return self.allocate_elevator

    """return the source floor of this elevator call was init at."""
    def get_src(self) -> int:
        return self.src

    """return the destenation floor to which this elevator call is targeted to."""
    def get_dest(self) -> int:
        return self.dest

    """Returns the time (in second) of the given state"""
    def get_time(self) -> float:
        return self.time

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.name) + ", " + str(self.time) + ", " + str(self.src) + ", " + str(self.dest) + ", " + \
               str(self.state) + ", " + str(self.allocate_elevator)