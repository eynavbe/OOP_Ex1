# OOP_Ex1

## Offline Algorithm
An offline algorithm is an algorithm that performs operations based on prior information. All information is transmitted as input or data before the program is executed and then, the program is executed according to all existing data.
In our program: An offline elevator algorithm is an algorithm in which all elevator calls are made before elevator operation. Once all the calls have been made they will be placed in the appropriate elevators once according to what is most appropriate. The adjustment will be made with an overall view of all the calls and therefore will also be more efficient than an online algorithm.
An offline algorithm makes it possible to build a more efficient plan because all the information is available to it in advance and therefore it will act according to it.


## Problem space
In a building with several floors, there are m elevators. The elevators in the building are smart elevators, meaning a passenger chooses the floor he wants to reach while he is ordering the elevator.
The most suitable elevator for passengers should be placed so that their average travel time (from the time of reading for the elevator to the time of getting out of it) will be minimal and extremely efficient.
• People choose which floor they want to go up / down, when the maximum floor                                             only has to go down and the minimum floor only has to go up.
• As soon as a call to the elevator is received, the passenger should be placed in the most suitable elevator.  
• The elevator has a maximum and minimum floor and it cannot go up or down beyond these floors
• The elevator stops only on floors where there is a call from passengers or reaching a person's destination in an elevator
• The elevator that responds to the call is the nearest elevator / elevator that will take a minimum of time to reach / an elevator that is in any case the floor in its own way.
.• The elevator will transport passengers in a minimum of time
• The elevator has a fixed travel time and a fixed stop time 
• Each floor can have a number of passengers - the number of passengers is relevant only when there is one who wants to get on and the other down (because there is no need to take into account the load of the elevator and the number of passengers allowed).
• All elevators start on the 0th floor.
• When calling the elevator there are several options: The elevator is above, under or on the requested floor.


## 4 similar works that deal with the optimization of elevators that inspired us for the task:
https://www.geeksforgeeks.org/smart-elevator-pro-geek-cup/
https://thinksoftware.medium.com/elevator-system-design-a-tricky-technical-interview-question-116f396f2b1c
https://stackoverflow.com/questions/493276/modelling-an-elevator-using-object-oriented-analysis-and-design
https://studylib.net/doc/7878746/on-line-algorithms-versus-off-line-algorithms-for-the-ele


## How our algorithm is executed
#### Our classes:
•	Building class - provides data on the list of elevators, number of floors, max floor and min floor in the building. This class represents a building with several floors and elevators.
•	Elevator class - Provides data on the speed, id, stopping time, and min and max floors of an elevator.
•	CallForElevator class - Provides information on destination floor, source floor, state, allocate elevator, and elevator call time of call. This class represents a call for an elevator - with a dedicated destination
•	MyElevator class - realizes the list of elevators stop, and list of times. 
•	ElevatorAlgo class - Places the calls to the appropriate elevator. 
•	MyTestCase class - Test the code
•	Bonus class - the implemented code of Bonus - python

#### Description of the algorithm's operation
we have list of calls and list of time. 
The Elevator list is a list of stop station – for any call that will allocate to the elevator, its source floor and destination will be placed in this list.
The time list include the time the elevator will reach the floors in the Elevator stop list.
1) Go through the first call in the order of the calls we received, then move on to the next call and so on.
2) Checking the times list in a loop, as soon as we arrive at a time larger than the current call we are checking, save the position before it as i.
3) In the location we saved (i) check if the inlay there is appropriate. We will check the direction of the elevator in position i, if the direction is appropriate we will place it there.
 • If the destination / call floor is already on the elevator list after position i, and the direction is appropriate, we will not place the floor that is already, and calculate the times according to what was before the reading (or if only one floor is, we will only add according to the added floor that is no longer on the list).
Note, if placed in position i, that the elevator will not pass the floor until then (by calculating the time of arrival of the elevator). If the elevator passes the floor we will check the position i + 1 (The elevator can pass the floor in case the time of arrival of the elevator to the floor is before the floor after, but the reading time is done after the elevator passes the floor).
If it does not appropriate  we will continue to check every 2 items in the list until we find the right position, and then, insert it in a sorted manner by "blocks" of descent and ascent. 
 4) Return the new list of each elevator and check the total time of each elevator after the placement of the current call we tested. The elevator with the shortest total time after placement is the elevator that will be placed for call.
note, the unselected elevators should be left without the call we checked
We will update the list of times in the selected elevator.
• If the elevator is empty he will only calculate the time it will take for the elevator to get to the call floor and compare with the other elevators and place according to the shortest time.


## Bonus:
A graphical simulation that shows the movement of elevators in relation to requests in GUI - python. 
•	class Bonus - the implemented code - python

The simulation of 2 elevators in motion according to a list of calls between the 2nd and 10th floors.
Simulation clip of the algorithm of files B2.json, Calls_a.csv:
https://www.youtube.com/watch?v=YPPQOODfGzQ
       






