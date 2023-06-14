import random
import statistics

# un-comment one of the 'variables' below to see how 'time saved' or 'average distance run' metric change through them. 
# variable = [num for num in range(1, 61) if num % 4 == 0] # This can be common ranges for the number of seconds the bus will take passengers at the stop.
# variable = [2, 4, 8, 10] # This can be variations for running speed in m/s.
# variable = [600, 900, 1800,3600] # This can be the frequencies of the bus arrivals in seconds.
# variable = [20, 40, 80, 120] # This can be the distance of visibility of the bus for the passenger in meters.
variable = [1] # By default, variable is set to [1] so that there will be no variational analysis for any parameters.
metric = []

for x in variable: # x is determined by all the values in the variable list. If the variational analysis for a given parameters in the initial conditions set below is going to be investigated, the value for that parameter should be x instead of a constant.
    waited_times = []
    distances_run = []

    for j in range(10000): # This is a Monte Carlo simulation, where multiple randomized experiences are run and metrics are averaged in the end.

        passenger_loc = -50 # Passenger's initial distance to the stop in meters.

        constant_bus_speed = 10 # Bus speed in the simulation in m/s.
        constant_running_speed = 4 # Passenger's running speed in m/s.
        constant_walking_speed = 1 # Passenger's walking speed in m/s.
        constant_bus_in_stop_time = 10 # Number of seconds the bus will board passengers at the stop.

        bus_visibilty_distance = 40 # The distance of visibilit of the bus for the passenger before the bus stop.
        bus_interval = 600 # Frequency of bus arrivals in seconds.
        bus_loc = -round(random.uniform(-constant_bus_speed * bus_interval, 0)/constant_bus_speed) * constant_bus_speed # Bus initial location relative to the stop in meters. This is set as a random value between the distance a bus can travel within its frequency of commuting and the stop.
        # In this simulation, the stop location is 0 and the passenger has a distance from the stop. By choosing a random distance for the bus, we ensure to randomize the arrival of the passenger as well since the degree of freedom of n randomly set values is n-1 = 2-1 = 1.
        
        
        passenger_in_stop = False 
        bus_in_stop = False
        arrived_time = ''
        waited_time = ''

        locs = []
        distance_run = 0

        for t in range(0, 100000): # variable t is time in the simulation. It always starts with 0 and then the simulation goes on until the passenger gets in the bus where the loop breaks.




            if -bus_visibilty_distance < bus_loc <= 0 and -bus_visibilty_distance < passenger_loc <= 0: # If passenger is within the visibility distance and the bus is approaching or is waiting at the stop, then the passenger will run. Otherwise, they will walk.
                passenger_speed = constant_running_speed
            else:
                passenger_speed = constant_walking_speed

            if passenger_loc > 0: # To ensure that the passenger will never get past the stop, but rather they'll stay at the stop once arrived.
                passenger_in_stop = True
                passenger_loc = 0

            if passenger_in_stop == True:
                passenger_speed = 0


            passenger_loc = passenger_loc + passenger_speed # The passenger's location increments by their velocity every second (i.e. every iteration in the loop).

            if passenger_speed == constant_running_speed:
                distance_run = distance_run + passenger_speed # This is to track the distance "run" by the passenger, so that we can calculate the average distance run later.



            if bus_loc == 0 and bus_in_stop == False:
                arrived_time = t # This is to store the time when the bus has arrived at the stop, so that we can ensure it will stay at the stop for a certain number of seconds before it departs.
                bus_in_stop = True 


            if bus_in_stop == False:
                bus_speed = constant_bus_speed

            if bus_loc == 0:
                if bus_in_stop == True:
                    if t - arrived_time < constant_bus_in_stop_time: # Here we check if the bus has already spend enough time at the stop before letting it go in the simulation again.  
                        bus_speed = 0 # The bus has to remain still at the stop.
                    else:
                        bus_speed = constant_bus_speed # The bus has to depart.
                        bus_in_stop = False

            if bus_loc > 0: # If the bus departs the stop (with its location necessarily having to be positive, then we take the bus back to the location of the next bus, which has will come at the next interval.
                bus_loc = bus_loc - constant_bus_speed * (bus_interval - constant_bus_in_stop_time)

            bus_loc = bus_loc + bus_speed # The bus's location increments by its velocity every second.

            locs.append([bus_loc, passenger_loc, passenger_speed]) # This is to track bus location, passenger location, and passenger speed over time.

            if passenger_in_stop == True and bus_in_stop == True: #If both the passenger and the bus are at the stop, then the passenger will get in and the loop breaks.
                waited_time = t # We store the measured time so far when the passenger gets in before we break the loop.
                waited_times.append(waited_time)
                break;

        distances_run.append(distance_run) # We track the distance run by the passenger in the iteration, so that we can have the distribution analysis e.g. average later.

    metric.append([x, statistics.mean(waited_times), statistics.mean(distances_run)]) # We store the variable x, as well as two aggregate metrics to analyze variational elasticity of the initial conditions.




print (waited_times)
print(statistics.mean(waited_times))
print(statistics.mean(distances_run))
# locs

import matplotlib.pyplot as plt
import pandas as pd

metric = pd.DataFrame(metric, columns = ['variable', 'time', 'distance_run'])
plt.plot(metric.variable, metric.distance_run)


