######################################################################################################################
# The Alpha Particles 2.0 project was made by Kyrollos Iskandar.
######################################################################################################################

### Program for Timing Experiment 1: Concatenation using a numpy array vs using a pandas DataFrame.

import random # Produce some random numbers.
import time # ... for timing experiments.
import os # ... for making a directory.

import numpy as np # numpy is one of the contestants.
import pandas as pd # pandas is one of the contestants.
import matplotlib.pyplot as plt # ... for producing plots of the results of the timing experiment.

def main_T1():
    try:
        os.mkdir("T1_Results") # This is the directory for saving the results of this timing experiment.

    except: # If the folder already exists, there is no need to recreate it.
        pass # Just keep going.

    InitialParticleNum = 10 # ... an example. 10 alpha particles initially.


    ### Initialise lists for collecting the data of the timing experiment.
    NumStep_List = []

    timer_np_Mean_List = []
    timer_DF_Mean_List = []

    timer_np_Sum_List = []
    timer_DF_Sum_List = []


    ### Initialise the numpy array and pandas DataFrame that are to be used for concatenating more columns to them.
    x0 = np.array([[0.0]] * InitialParticleNum)
    x0_DF = pd.DataFrame([0.0] * InitialParticleNum)


    ### Start the timing experiment.
    for NumStep in range(100, 5100 + 500, 500): # NumStep represents the total number of simulation steps in the AlphaParticles2.py program.
        NumStep_List.append(NumStep) # Collect the data.
        
        Dict = {key : [[random.random()]] * InitialParticleNum for key in range(0, NumStep)} # In every simulation step in the AlphaParticles2.py program, there is a list of x-positions of the alpha particles. The list in the values in the dictionary represents that list of x-positions.

        timer_np = [] # Initialise a list for collecting execution times of numpy array concatentation.
        for key in range(0, len(Dict)): # Concatenate all of the lists into one numpy array.
            start_np = time.time()
            x0 = np.concatenate((x0, np.array(Dict[key])), axis = 1) # This is the numpy array concatenation we are timing.
            end_np = time.time()

            timer_np.append(end_np - start_np) # Collect the execution time for the numpy array concatenation.

        timer_np_Mean_List.append(np.array(timer_np).mean()) # Summarise the execution times.
        timer_np_Sum_List.append(np.array(timer_np).sum())
        

        timer_DF = [] # Initialise a list for collecting execution times of pandas DataFrame concatentation.
        for key in range(0, len(Dict)): # Concatenate all of the lists into one pandas DataFrame.
            start_DF = time.time()
            x0_DF = pd.concat([x0_DF, pd.DataFrame(Dict[key])], axis = 1) # This is the pandas DataFrame concatenation we are timing.
            end_DF = time.time()

            timer_DF.append(end_DF - start_DF)

        timer_DF_Mean_List.append(np.array(timer_DF).mean()) # Summarise the execution times.
        timer_DF_Sum_List.append(np.array(timer_DF).sum())


    ### Plot the results of the experiment.
    # Plot the average execution time as a function of the number of simulation steps.
    plt.figure()
    plt.scatter(NumStep_List, timer_np_Mean_List, marker = "x")
    plt.scatter(NumStep_List, timer_DF_Mean_List, marker = ".")
    plt.xlabel("Total number of simulation steps")
    plt.ylabel("Average time spent concatenating a list /s")
    plt.legend(labels = ("numpy array concatenation", "pandas DataFrame concatenation"))
    plt.savefig("T1_Results/AverageConcatenationTime.png")

    # Plot the total execution time as a function of the number of simulation steps.
    plt.figure()
    plt.scatter(NumStep_List, timer_np_Sum_List, marker = "x")
    plt.scatter(NumStep_List, timer_DF_Sum_List, marker = ".")
    plt.xlabel("Total number of simulation steps")
    plt.ylabel("Total time spent concatenating lists /s")
    plt.legend(labels = ("numpy array concatenation", "pandas DataFrame concatenation"))
    plt.savefig("T1_Results/TotalConcatenationTime.png")


if __name__ == "__main__":
    main_T1()


# REFERENCES:
    # Python Software Foundation (2020). random — Generate pseudo-random numbers, https://docs.python.org/3/library/random.html.
    # Python Software Foundation (2020). time — Time access and conversions, https://docs.python.org/3/library/time.html.
    # Python Software Foundation (2020). os — Miscellaneous operating system interfaces, https://docs.python.org/3/library/os.html.
    # NumPy (2020). NumPy v1.19.0, https://numpy.org/.
    # the pandas development team (2020). pandas, https://pandas.pydata.org/.
    # Hunter, J, Dale, D, Firing, E, Droettboom, M & The Matplotlib development team Matplotlib: Visualization with Python, https://matplotlib.org/.