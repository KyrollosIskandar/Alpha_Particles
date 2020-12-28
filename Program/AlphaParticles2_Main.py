######################################################################################################################
# The Alpha Particles 2.0 project was made by Kyrollos Iskandar.
######################################################################################################################

####################################### Commands required to run the program #########################################
# NOTE: To run this program, type and ENTER python AlphaParticles2_Main.py in the command terminal. Also make sure to have the modules specified in the notice() function installed.
######################################################################################################################

# NOTE: You may wish to toggle on Word Wrap for reading the script. Alt + z is the shortcut for doing this.

##############################################################################################################################
############################################### About the program ############################################################
##############################################################################################################################
# NOTE: This program tries to answer the following question: "How far do alpha particles of a given initial kinetic energy travel in a given medium in the case where they are in a monoenergetic parallel beam?" This version of the program includes the consideration of an arbitrary medium and can express distance in arbitrary units, if the user chooses to.

##############################################################################################################################
if __name__ == "__main__":
    print("The program is loading. Please wait ...\n") # It can take a few seconds for the program to show the first message. This message here is for assuring the user that the program is just loading.

### We are going to start by importing the modules we need.
# Standard libraries ...
import math # We are going to use mathematical values such as natural logarithms, for example, in calculations.
import statistics as stat # ... for doing statistical analysis of the results of the simulations.
from datetime import datetime # We are going to use the local date and time to name the files that the program outputs.
import os # We need this module to make a directory for all of the data files that are going to be generated.
import sys # We need this module in case the user inputs a value outside the range of floating point numbers that Python can deal with.
import random # Import the "random" module of Python. We are going to use it to generate random numbers. We want to generate a randomised 3x3 matrix for taking each alpha particle from one simulation step to the next. And we want to have some control over its elements. However, the parts of the matrix that stay constant shall be defined globally while the parts that change for each particle and simulation step shall be put into a method in the AlphaParticles class, namely update_AlphaParticleMomentum().
import multiprocessing as mp # ... for parallelising the execution class methods and thus reduce their overall execution time.
import time # ... for timing the execution of code without outputting the clutter that is outputted by pprofile's deterministic profiling.

# External modules ...
import numpy as np # We are going to deal with arrays because they are more useful than lists of lists. The indexing in lists of lists is not quite what I want. For example, if List = [[1,0,0]] * 3 and then I say List[1][1] = 2, I would get [[1,2,0],[1,2,0],[1,2,0]] instead of [[1,0,0],[1,2,0],[1,0,0]], which is what numpy gives me when I use numpy.array().
import matplotlib.pyplot as plt # We are going to plot data, so we need matplotlib.pyplot.
import pandas as pd # ... for reading data from CSV files and for dealing with DataFrames where appropriate.
import psutil # ... for counting the number of physical cores rather than logical processors of a CPU. This module is to be used with the multiprocessing module for determining how many Pool processes to make.

# My script files ...
import TimerAdmin # TimerAdmin is a profiler administrator specifically for my program. The TimerAdmin.py file has only class and method definitions, so no code is executed from it when it is imported.

# REFERENCES: 
    # Python Software Foundation (2020). math — Mathematical functions, https://docs.python.org/3/library/math.html.
    # NumPy. (2020). NumPy v1.19.0. Retrieved from https://numpy.org/
    # Hunter, J., Dale, D., Firing, E., Droettboom, M., & The Matplotlib development team. (15 September 2020). Matplotlib: Visualization with Python. Retrieved from https://matplotlib.org/
    # the pandas development team. (2020). pandas. pandas. Retrieved from https://pandas.pydata.org/
    # Python Software Foundation. (2020, 17 September 2020). datetime — Basic date and time types. Retrieved from https://docs.python.org/3/library/datetime.html
    # Python Software Foundation. (2020, 17 September 2020). os — Miscellaneous operating system interfaces. Retrieved from https://docs.python.org/3/library/os.html
    # Hofmann, F. Creating and Deleting Directories with Python. Retrieved from https://stackabuse.com/creating-and-deleting-directories-with-python/
    # Python Software Foundation. (2020, 18 September 2020). sys — System-specific parameters and functions. Retrieved from https://docs.python.org/3/library/sys.html
    # Python Software Foundation. (2020, 17 September 2020). random — Generate pseudo-random numbers. Retrieved from https://docs.python.org/3/library/random.html
    # Python Software Foundation (2020). psutil 5.7.2, https://pypi.org/project/psutil/.
    # Check the version of Python package / library,  https://note.nkmk.me/en/python-package-version/.
    # Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
    # Fayek, H (2020). Week 11 Case Study: Linear Regression, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.


def initialise_Program(): # This code is placed inside a function to protect it from being run more than once when multiprocessing is used.
    ### Now we are going to obtain the timestamp from the user's system for the purpose of naming the outputted folder and files.
    try: # The code here is inside a try-except code block just in case the program cannot obtain the present date and time from the user's computer.
        timestamp = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) # The use of this timestamp is to give a unique name to the files that the program outputs so that it is easier for the user to document their work/research. The timetamp tells the user when the simulation began. The timestamp is a string because it is going to be used in the write() method for writing text to a text file.
        ContinueProgram = None # This variable must have a value because it is included in the RETURN statement below. And if the EXCEPT section below is not run, an error will be raised saying that this variable is referenced before assignment.
    
    except: # The except statement here is present in case an error is raised due to the program not being able to obtain the present date and time.
        print("For some reason, the program could not obtain the present date and time from your computer. The date and time were going to be used for naming the files outputted by the program and are not necessary for generating the results themselves.")
        ContinueProgram = input("Would you like to continue running the program? (y: yes, n: no) ")
        
        try:
            if ContinueProgram in set(["y", "Y"]): # Defining multiple conditions for a string value in this way is more compact than defining the conditions using "==" and "or".
                print("Ok. The outputted files will not have a timestamp.") # Tell the user how their choice will affect their work.
                timestamp = "" # Omit the timestamp from the names of the outputted files.
            
            elif ContinueProgram in set(["n", "N"]): # Defining multiple conditions for a string value in this way is more compact than defining the conditions using "==" and "or".
                print("The program will now exit.") # This is what the user wished to happen.
                exit()
            
            else:
                print("Error: You did not provide a valid answer. The program will now exit.") # This is a way of handling an invalid answer to the question that was asked of the user.
                exit()
            
            # REFERENCE: Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.

        except: # This except statement is present in case an error is raised in the IF-ELIF-ELSE statement above as a whole code block.
            print("Error Unknown: The program will now exit.")
            exit()

    # REFERENCES:
        # Programiz. Python strftime(). Retrieved from https://www.programiz.com/python-programming/datetime/strftime
        # Programiz. Python Exception Handling Using try, except and finally statement. Retrieved from https://www.programiz.com/python-programming/exception-handling

    
    ### Now we are going to use the os module to create a directory for the data files that are going to be produced by the program.
    try:
        DirectoryToSaveTo = "Data_" + timestamp + "/" # We want the folder's name to have the timestamp of when the simulation began. The definition of the folder's name has "/" in it so that, if the folder cannot be made, the data files can still be saved in the same directory as the program file. The "/" character, when used when defining file names, is what tells Python to save the file in another folder relative to the program file's directory. Also, using "/" instead of "\" may avoid problems in the case where the program was run on a Mac computer.
        os.mkdir(DirectoryToSaveTo) # The folder would not be present until after the program is run because its name depends on the timestamp of when the simulation began. Thus, it must be made during the program's runtime. Also, it is suitable to save it using the specified relative path from the program file.
    
    except:
        print("For some reason, the directory in which the data files were going to be saved could not be created.")
        ContinueProgram = input("Would you like to continue running the program? (y: yes, n: no) ")
        
        try:
            if ContinueProgram in ["y", "Y"]: # Defining multiple conditions for a string value in this way is more compact than defining the conditions using "==" and "or".
                print("Ok. The outputted files will be in the same directory as AlphaParticles.py instead.") # Tell the user how their choice will affect their work.
                DirectoryToSaveTo = "" # Just provide an empty string for this variable so it is defined. No new folder will actually be made because there is no "/" character in this variable.
            
            elif ContinueProgram in ["n", "N"]: # Defining multiple conditions for a string value in this way is more compact than defining the conditions using "==" and "or".
                print("The program will now exit.") # This is what the user wished to happen.
                exit()
            
            else:
                print("Error: You did not provide a valid answer. The program will now exit.") # This is a way of handling an invalid answer to the question that was asked of the user.
                exit()
        
        except: # This except statement is present in case an error is raised in the IF-ELIF-ELSE statement above as a whole code block.
            print("Error Unknown: The program will now exit.")
            exit()

    
    ### Now we are going to obtain the minimum and maximum floating point numbers that Python can handle on the system for the purpose of handling floating point inputs from the user.
    try:
        FloatMin = sys.float_info.min
        FloatMax = sys.float_info.max

    except: # The minimum and maximum floating point values that Python can deal with are defined here directly in case, for some reason, the sys module fails to be imported or the minimum and maximum floating point numbers cannot be determined using the sys module.
        FloatMin = 2.2250738585072014e-308 # This number was the output when I inputted sys.float_info.min in the Python shell.
        FloatMax = 1.7976931348623157e+308 # This number was the output when I inputted sys.float_info.max in the Python shell.
    
    
    PhysicalCPUCoreCount = psutil.cpu_count(logical = False) # Count the number of physical cores, not logical processors. Some CPUs have multiple logical processors per core. And Python uses an entire core per instance. We do not want to try to use more physical cores than what the CPU has.
    CPUCoresToNotUse = 1 # This variable is for multiprocessing. At least one physical CPU core is spared so that the program does not potentially stall or overheat the computer it is being run on, while still harnessing the computer's available resources to a reasonable extent.

    if PhysicalCPUCoreCount > 1: # Most, if not all, computers have a CPU with multiple physical cores. We do not want the program to use all of them so that the computer does not stall or potentially overheat while a simulation is running.
        MaxCPUCoresToUse = PhysicalCPUCoreCount - CPUCoresToNotUse
    
    elif PhysicalCPUCoreCount == 1: # Some computers may have a CPU with only 1 physical core. However, this is probably rare, but it is good to account for it. However, while the program will probably still run on those computers, multiprocessing will not be done on them because they have only 1 CPU core anyway.
        MaxCPUCoresToUse = 1
    
    return timestamp, ContinueProgram, DirectoryToSaveTo, FloatMin, FloatMax, MaxCPUCoresToUse

if __name__ == "__main__": # initialise_Program() must be executed before the definitions below are run to avoid issues with variables not being defined when multiprocessing is used.
    timestamp, ContinueProgram, DirectoryToSaveTo, FloatMin, FloatMax, MaxCPUCoresToUse = initialise_Program() # Also, the values being assigned in this line must be taken out of the function so that they can be used throughout the rest of the program.
    timing_studies = TimerAdmin.TimingStudies(DirectoryToSaveTo, timestamp) # This is the object for the timing experiments. It must be defined before the rest of the code is even looked at by the Python interpreter.

    # REFERENCES:
        # Fayek, H (2020). Week 11 Case Study: Linear Regression, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
    
### Now we define classes. I choose to use Object-Oriented Programming (OOP) because while Structured Programming (SP) groups statements into functions, OOP groups functions into classes. Therefore, I see OOP as being more organised than SP.
if __name__ == "__main__": # This IF statement prevents slave processes from executing code they are not supposed to execute. Apparently, these processes execute the program under a name that is not "__main__".
    timing_studies.start_ClassDefinition_ErrorChecking = time.time()


class ErrorChecking: # This class has methods for checking for errors in the user's inputs.
    def __init__(self):
        self.MinimumAlphaEnergy_eV = 1 # ... in units of eV. This variable had to be defined here because it is used in the child classes of the ErrorChecking class. When an alpha particle has lost all of its energy, it leaves the beam of alpha particles. However, it still has a very tiny amount of energy when it leaves the beam. An alpha particle leaves the beam when it captures free electrons and becomes a helium atom. I think that kinetic energy is 1 eV, though the kinetic energy an alpha particle has when it captures free electrons is probably in a range of energies. I need to do more research to know what these energies are.

        self.FloatMin = FloatMin # Make these two values available within multiprocessing when the pooled processes effectively run their own instances of the program with __name__ != "__main__". FloatMin is used in the update_AlphaParticlePosition() method of the AlphaParticles class.
        self.FloatMax = FloatMax
    
    def bound_FloatingPointInput(self, input_float): # This method is for making sure the floating point numbers that the user inputs are within the range of floating point numbers that Python can handle.
        self.input_float = input_float
        while (self.input_float < -FloatMax) or (self.input_float > FloatMax):  # ... if the inputted floating point number is too large.
            print() # Separate the message below from other text that was printed to the screen earlier.
            print("Error: Python cannot handle floating point numbers with a magnitude greater than {}.".format(FloatMax)) # The string's format() method appears to work here even though the string is inside the input() function rather than the print() function.
            
            try: # The code in the TRY section can return an error if the user inputs something other than a number.
                self.input_float = float(input("Please input a replacement value with a magnitude between {} and {}: ".format(FloatMin, FloatMax))) # Let the user try again in inputting a suitable floating point number.
            
            except: # The code in the EXCEPT section will be executed if the user inputs something other than a number.
                print("Error: You did not input a floating point number. The program will now exit.")
                exit() # Exit the program instead of asking the user again to input a suitable floating point number, lest there possibly be many nested repetitions of the same code in this script.

        if (-FloatMax < self.input_float < -FloatMin) or (FloatMin < self.input_float < FloatMax): # This is the range of floating point numbers that Python can handle. Having this IF statement *after* the WHILE loop above makes sure that it gets executed after Python exits the WHILE loop.
            return self.input_float # If the inputted floating point number is in the range of floating point numbers Python can handle, then there is no issue. The rest of the program sees only what is after the RETURN keyword.
        
        elif self.input_float == 0.0: # Apparently, when Python feeds a floating point number with a magnitude less than FloatMin into the bound_FloatingPointInput() function, the number becomes 0.0. In this simulation, it is appropriate to treat floating point numbers with magnitudes less than FloatMin as 0.0.
            print() # Separate the message below from other text that was printed to the screen earlier.
            print("You inputted a floating point number with a magnitude less than {}. Your inputted number will be treated as 0.0.".format(FloatMin))
            
            return 0.0 # The rest of the program sees only what is after the RETURN keyword.

    
    def checkResult_boundFloatingPointInput(self, result): # This method is for dealing with any unusual outputs from the bound_FloatingPointInput() method.
        while result is None: # Apparently, the bound_FloatingPointInput() function outputs None when the magnitude of the inputted *replacement* floating point number is less than FloatMin.
            print() # Separate the message below from other text that was printed to the screen earlier.
            print("Error: The value you inputted could not be accepted.") # I am not sure what the issue is exactly. However, the inputted floating point number is not acceptable.
            
            try: # The code in the TRY section can return an error if the user inputs something other than a number.
                self.input_float = float(input("Please input a replacement value with a magnitude between {} and {}: ".format(FloatMin, FloatMax))) # Let the user try again in inputting a suitable floating point number.
            
            except: # The code in the EXCEPT section will be executed if the user inputs something other than a number.
                print("Error: You did not input a floating point number. The program will now exit.")
                exit() # Exit the program instead of asking the user again to input a suitable floating point number, lest there possibly be many nested repetitions of the same code in this script.
            
            result = self.bound_FloatingPointInput(self.input_float) # The new inputted floating point number must be checked again from the start of the process by which inputted floating point numbers are checked.
        
        return result # The rest of the program sees only what is after the RETURN keyword.
    

    def check_FloatingPointInput(self, FloatingPointInput): # This method that reduces the character count from using the above two methods directly.
        CheckedResult = self.checkResult_boundFloatingPointInput(self.bound_FloatingPointInput(FloatingPointInput))

        return CheckedResult

if __name__ == "__main__":
    timing_studies.end_ClassDefinition_ErrorChecking = time.time()
    timing_studies.append_TimingResults("ErrorChecking class definition", timing_studies.end_ClassDefinition_ErrorChecking - timing_studies.start_ClassDefinition_ErrorChecking, "Once")
    
    timing_studies.start_ClassDefinition_ProgramAdmin = time.time()
    

class ProgramAdmin(ErrorChecking): # I am using a class for defining the functions here to keep the formatting of this program file consistent.
    def __init__(self):
        super().__init__() # Inherit the MinimumAlphaEnergy_eV variable.

    
    def show_AboutTheProgram(self): # Tell the user basic information about the program.
        print("The program has loaded.")
        print("#" * 100) # If the user is using the program in the command terminal, having a title that stands out from the surrounding text can make it easier for the user to distinguish what was output to the terminal for one simulation from what was output to the terminal for another simulation that was run before or after it.
        print("#" * 41 + " Alpha Particles 2.0 " + "#" * (100 - 41 - len(" Alpha Particles 2.0 "))) # The title has the name of the program.
        print("#" * 100) # This is part of the title.
        print("Welcome to the Alpha Particles simulator program, version 2.0, for Windows 10.") # This is an introduction of the program for the user.
        print("It calculates the mean and maximum ranges of an alpha particle beam through a medium. It also plots the number of alpha particles in the beam as a function of distance travelled through the medium.") # This is a brief description of what the program can do for the user.
        print("The program also has a radiotherapy game and a beam attenuation quiz.")
        print() # Let the text printed to the command terminal be organised into paragraphs. Any text that is printed to the terminal will be separated from the text in this function definition by an empty line.

    
    def show_Instructions(self): # Tell the user intructions for how to use the program.
        print("Please input values for the parameters when prompted.")
        print("The higher the initial number of particles, the more time the simulation will take to complete.", "\n", "You are recommended to start with a small number for the initial number of particles and gradually increase this number towards your target value while noting the computation times.")
        print("If you need to stop a simulation before it completes, press Ctrl + c while in the command terminal.")
        print() # Let the text printed to the command terminal be organised into paragraphs. Any text that is printed to the terminal will be separated from the text in this function definition by an empty line.

    
    def get_InputsForAlphaBeam(self): # This method is how the program accepts input from the user about the characteristics of the alpha particle beam. These characteristics are the initial kinetic energy of the alpha particles and how many particles are initially in the beam.
        ## Get an input for the initial kinetic energy of the alpha particles.
        try: # This try-except code block is for handling errors due to the user's input.
            self.InitialKineticEnergy = self.check_FloatingPointInput(float(input("What is the initial kinetic energy of the alpha particles, in MeV? "))) # The calculations that involve this variable require that this variable be a number. An alpha particle can have a kinetic energy that is a floating point number. Therefore, this variable is made to be float type.
        
        except:
            print("Error: You did not input a floating point number for the initial kinetic energy. The program will now exit.") # The user must input a floating point value for the initial kinetic energy.
            exit() # Do not continue running the program because the user did not specify a valid value for the variable. The RETURN keyword may still let the program run.
        
        while self.InitialKineticEnergy <= 0: # If the user specifies a value for the initial kinetic energy that does not raise an error but is physically invalid. A negative kinetic energy is invalid.
            print("Error: You must specify a value greater than 0.0 for the initial kinetic energy of the alpha particles. Please try again.")
            
            try: # This try-except code block is for handling errors due to the user's input.
                self.InitialKineticEnergy = self.check_FloatingPointInput(float(input("What is the initial kinetic energy of the alpha particles, in MeV? "))) # Let the user try again in inputting a valid value for this variable.
            
            except:
                print("Error: You did not input a floating point number for the initial kinetic energy. The program will now exit.") # The user must input a floating point value for the initial kinetic energy. I want the EXCEPT statements to cleanly exit the user from the program. This is more robustly achieved using exit() than the RETURN keyword because the RETURN keyword may allow the program to continue running depending on its indentation level in the script.
                exit() # Do not continue running the program because the user did not specify a valid initial kinetic energy. If the program continues to run, it may crash due to the initial kinetic energy not being defined. I use usually use exit() in the command terminal to exit a Python shell, so it should work in a script, too.
        
        print()

        
        ## Get an input for the initial number of alpha particles in the beam.
        try: # This try-except code block is for handling errors due to the user's input.
            self.InitialParticleNumber_Float = self.check_FloatingPointInput(float(input("How many alpha particles are initially in the beam? "))) # ... for checking if the user inputted a floating point number for the initial number of particles and telling them how the program handled this input.
            self.InitialParticleNumber = int(self.InitialParticleNumber_Float) # Alpha particles are counted as whole alpha particles, so we treat this value as an integer. A portion of an alpha particle is *not* an alpha particle. The user may input a number in scientific notation; for example, 2e3. However, int("2e3") returns an error, but float("2e3") does not. A solution then is to first covert the string "2e3" to a float then to an integer. (See Nymeria (2018) below.)
        
        except:
            print("Error: You did not input an integer greater than 0 for the initial number of alpha particles in the beam. The program will now exit.") # This is what the user must do.
            exit() # Do not continue running the program because the user did not specify a valid value for the variable. The RETURN keyword may still let the program run.
        
        while self.InitialParticleNumber <= 0:
            print("Error: You must input an integer greater than 0 for the initial number of alpha particles in the beam. Please try again.") # This is what the user must do.
            
            try: # This try-except code block is for handling errors due to the user's input.
                self.InitialParticleNumber = int(self.check_FloatingPointInput(float(input("How many alpha particles are initially in the beam? ")))) # Let the user try again in inputting a valid value for this variable.
            
            except:
                print("Error: You did not input an integer greater than 0 for the initial number of alpha particles in the beam. The program will now exit.") # This is what the user must do.
                exit() # Do not continue running the program because the user did not specify a valid value for the variable. The RETURN keyword may still let the program run.
        
        if self.InitialParticleNumber_Float - self.InitialParticleNumber != 0.0: # ... in case the user inputs a floating point number for the initial number of particles. Python cuts off the decimal places of a floating point number when it converts the number to an integer.
            print("Warning: Only integer numbers are accepted for the initial number of particles. Your input will be treated as {}.".format(int(self.InitialParticleNumber)))

        print()

        
        ## Get an input for which probability density function to use for generating random numbers for the randomised 3x3 matrix (RandomMatrix).
        try: # While an error may not be raised due to the user's input because it will be converted to a string, this try-except code block is present just in case an error occurs.
            self.RandomDistribution = input("Which probability density function would you like to use for the generation of random numbers for the simulation?\n\tOptions (type the name of the probability density function you wish to use):\n\t\t> basic (the basic random number generator of Python's random module. It generates numbers between 0 and 1, including 0 but not 1)\n\t\t> discrete (the user specifies the fineness of the discretisation. Numbers are generated with equal probability)\n\t\t> triangular (ranges from 0 to 1 with a mode of 0. The probability of generating a number n between 0 and 1 decreases linearly from a maximum probability at 0 to zero probability at 1)\n\t\t> uniform (includes both 0 and 1)\nChoice: ") # This program lets the user select which probability density function they wish to use for the generation of random numbers. The user can input anything for this variable because their input will be converted to a string.
            
            while self.RandomDistribution not in set(["basic", "discrete", "triangular", "uniform"]): # Make sure that the input the user provides in reply to the prompt in the previous line is the name of one of the specified probability density functions. Using "not in" and a list of values is more compact than using multiple "==" statements with multiple "or"s.
                print("Error: You must type the name of one of the probability density functions that are specified in the list above. Please try again.")
                self.RandomDistribution = input("Choice: ") # The user already saw the message of what they must do for giving valid input to this variable. Printing the message to the screen again is not necessary.
        
        except:
            print("Error: You did not type the name of one of the probability density functions that were specified in the list above. The program will now exit")
            exit() # Do not continue running the program because the user did not specify a valid value for the variable. The RETURN keyword may still let the program run.
        
        print()

        try:
            self.ToSeed = input("Would you like to seed the random number generators using a seed you provide? (y/n) ")
            
            while self.ToSeed not in set(["y", "Y", "n", "N"]):
                print("Error: You must answer yes (y) or no (n). Please try again.")
                self.ToSeed = input("Answer: ")
        
        except:
            print("You did not provide a valid answer. The program will now exit.")
            exit()
        
        if self.ToSeed in set(["y", "Y"]):
            try:
                self.Seed = int(self.check_FloatingPointInput(float(input("\tPlease input an integer seed number for the random number generators of the program: "))))
                print()
            
            except:
                print("You did not provide an integer for the seed. The program will now exit.")
                exit()

            random.seed(a = self.Seed, version = 2) # Initialise the random number generators of the random standard library.
        
        elif self.ToSeed in set(["n", "N"]):
            print("Ok. The random number generators will *not* be seeded.")
            self.Seed = None # ... so no error is raised when the value for the seed is saved to a data file due to this variable not being defined.
            print()
        
        # REFERENCES:
            # Python Software Foundation. (2020, 11 September 2020). random — Generate pseudo-random numbers. Retrieved from https://docs.python.org/3/library/random.html

        return self.InitialKineticEnergy, self.InitialParticleNumber, self.RandomDistribution # This sequence of values exits the function and can be used elsewhere in the program. When the get_Inputs() function is executed, the rest of the program sees a sequence of the numbers that are in the RETURN statement. This is why InitialKineticEnergy, InitialParticleNumber = get_Inputs() in the main() function is valid.

    
    def get_InputsForAlphaBeam_CrossSectionalArea(self): # This method is for the Alpha Radiotherapy Game.
        self.BeamHeight = self.check_FloatingPointInput(float(input("What is the height of the alpha beam, in cm? ")))
        self.BeamWidth = self.check_FloatingPointInput(float(input("What is the width of the alpha beam, in cm? ")))

        return self.BeamHeight, self.BeamWidth
    
    
    def get_InputsForMedium(self): # The user is going to specify a medium that is going to be used in the simulation that is in terms of distance travelled through a medium. Although this method is related to the medium rather than the alpha particle beam, at least one of the parameters defined in the make_Medium() method are dependent on the properties of the beam. For example, the CrossSection depends on the kinetic energy of the alpha particle. However, I am not certain about this and I am going to use the expression for the CrossSection shown in the make_Medium() method.
        try:
            self.AtomicNumber = self.check_FloatingPointInput(float(input("What is the atomic number of the medium? "))) # The atomic number for a compound may not be an integer. So we shall leave this variable as a floating point number.
            
            while self.AtomicNumber <= 0.0:
                print("Error: The atomic number cannot be zero or a negative number. Please try again.")
                self.AtomicNumber = self.check_FloatingPointInput(float(input("What is the atomic number of the medium? "))) # The atomic number for a compound may not be an integer. So we shall leave this variable as a floating point number.

        except:
            print("Error: You did not provide a valid answer. The program will now exit.")
            exit()
        
        
        try:
            self.AtomicWeight = self.check_FloatingPointInput(float(input("What is the atomic weight of the medium, in units of g/mol? ")))

            while self.AtomicWeight <= 0.0:
                print("Error: The atomic weight cannot be zero or a negative number. Please try again.")
                self.AtomicWeight = self.check_FloatingPointInput(float(input("What is the atomic weight of the medium, in units of g/mol? ")))
        
        except:
            print("Error: You did not provide a valid answer. The program will now exit.")
            exit()
        
        
        try:
            self.MassDensity = self.check_FloatingPointInput(float(input("What is the mass density of the medium, in units of g/cm^3? ")))
            
            while self.MassDensity <= 0.0:
                print("Error: The mass density cannot be zero or a negative number. Please try again.")
                self.MassDensity = self.check_FloatingPointInput(float(input("What is the mass density of the medium, in units of g/cm^3? ")))
            
        except:
            print("Error: You did not provide a valid answer. The program will now exit.")
            exit()

        return self.AtomicNumber, self.AtomicWeight, self.MassDensity # Return the variables for use when multiple instances of a simulation are run.
    
    
    def specify_MediumForRTGame(self): # We are going to specify the physical characteristics of human tissue. The relevant characteristics are atomic number, atomic weight and mass density.
        ### Human tissue is made of multiple chemical elements. We are going to use the elemental composition defined by the International Commission on Radiation Units and Measurements (ICRU). The elements we are interested in are hydrogen (H), carbon (C), nitrogen (N) and oxygen (O).
        ## First, we are going to define the atomic number.
        # We are going to consider the composition by mass fraction. The mass fractions sum to 1, as expected.
        self.H_MassFraction = 1.01172e-1
        self.C_MassFraction = 1.11000e-1
        self.N_MassFraction = 2.60000e-2
        self.O_MassFraction = 7.61828e-1
        self.MassFractionList = np.array([self.H_MassFraction, self.C_MassFraction, self.N_MassFraction, self.O_MassFraction]) # This list is going to make calculating the effective atomic number simpler. It is a numpy array for element-wise multiplication.

        # For calculating an effective atomic number of human tissue, we need to know the atomic number of each of the elements.
        self.H_AtomicNumber = 1
        self.C_AtomicNumber = 6
        self.N_AtomicNumber = 7
        self.O_AtomicNumber = 8
        self.AtomicNumberList_Tissue = np.array([self.H_AtomicNumber, self.C_AtomicNumber, self.N_AtomicNumber, self.O_AtomicNumber]) # This list is going to make calculating the effective atomic number simpler. It is a numpy array for element-wise multiplication.

        self.AtomicNumber_Tissue = (self.MassFractionList * self.AtomicNumberList_Tissue).sum() # We are going to define the effective atomic number as the sum of the elements' atomic numbers weighted by mass fraction.

        ## Next, we are going to define the atomic weight.
        self.H_AtomicWeight = 1.00794 # ... in units of g/mol.
        self.C_AtomicWeight = 12.0107 # ... in units of g/mol.
        self.N_AtomicWeight = 14.0067 # ... in units of g/mol.
        self.O_AtomicWeight = 15.9994 # ... in units of g/mol.
        self.AtomicWeightList_Tissue = np.array([self.H_AtomicWeight, self.C_AtomicWeight, self.N_AtomicWeight, self.O_AtomicWeight]) # This list is going to make calculating the effective atomic number simpler. It is a numpy array for element-wise multiplication.

        self.AtomicWeight_Tissue = (self.MassFractionList * self.AtomicWeightList_Tissue).sum() # We are going to define the effective atomic number as the sum of the elements' atomic weights weighted by mass fraction.

        ## Lastly, we define the mass density. Alpha particles typically do not penetrate deep into the skin, so we are interested in the mass density of skin.
        self.MassDensity_Tissue = 1.02 # ... in units of g/cm^3.

        # REFERENCES:
            # International Commission on Radiation Units & Measurements Inc. (2020). Reports, https://icru.org/link-index.
            # CRC handbook of chemistry and physics : a ready-reference book of chemical and physical data, 2017). 97 ed. 6000 Broken Sound Parkway NW, Suite 300 Boca Raton, FL 33487-2742: Taylor & Francis Group, LLC.
            # National Institute of Standards and Technology Atomic Weights and Isotopic Compositions for All Elements, https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&ascii=html&isotype=all.
            # Liang, X & Boppart, S A (2010). Biomechanical Properties of In Vivo Human Skin From Dynamic Optical Coherence Elastography. IEEE Transactions on Biomedical Engineering 57, 4 953–959.

    
    def get_MediumCharacteristicsForRTGame(self):
        return self.AtomicNumber_Tissue, self.AtomicWeight_Tissue, self.MassDensity_Tissue
    
    
    def present_RTGameProblem(self):
        self.DoseToDeposit_Gy = 0.08 # Units: Gy. This is the radiation dose that the user must deposit into the tissue. Usually in radiotherapy, therapeutic doses are 2.0 Gy. However, the program takes too much time to simulate the high number of alpha particles and/or high initial kinetic energy required to achieve an absorbed dose of 2.0 Gy. Perhaps even more optimisation/multiprocessing of the program can let this absorbed dose be achieved within a reasonable execution time.
    
        print("You must deposit {} Gy of radiation dose into tissue.".format(self.DoseToDeposit_Gy))
        print("The tissue has the following characteristics:")
        print("\t> Effective atomic number = {}".format(self.AtomicNumber_Tissue))
        print("\t> Atomic weight = {} g/mol".format(self.AtomicWeight_Tissue))
        print("\t> Mass density = {} g/cm^3".format(self.MassDensity_Tissue))
        print()
        print("Goal: Define an alpha particle beam that can deliver {} Gy of radiation dose to the tissue.".format(self.DoseToDeposit_Gy))
        print("\t> Note: The beam's cross-sectional area is square-shaped.")
        print()

        return self.DoseToDeposit_Gy

    
    def present_AttenuationQuizDetails(self):
        print("In this quiz, an alpha particle beam of a random energy will be generated.")
        print("Also, a medium and a beam transmission fraction will be randomly chosen for you to consider.")
        print("Your task is to predict the thickness(es) of the material(s) that will transmit the aforementioned fraction of the beam. A material attenuates the beam more if it is thicker.")
        print("You may specify the number of materials you would like to consider, but the program will select them.")
    
    
    def choose_MediaForAttenuationQuiz(self):
        ### Define the media/materials from which a medium will be randomly sampled.
        ## Order of the elements in the list: Material name, Atomic number, Atomic weight (g/mol), Mass density (g/cm^3).
        # NOTE: Mass densities are at 20 degrees C unless otherwise stated.
        try:
            self.MaterialLibrary_DF = pd.read_csv("AttenuationQuiz_MaterialLibrary.csv").T.reset_index(drop = True).T
        
        except FileNotFoundError:
            print("Error: The CSV file named 'AttenuationQuiz_MaterialLibrary' was not found. Please make sure that there is such a file in the same directory as the script file of this program and try again. The program will now exit.")
            exit()
        
        except: # ... in case the error is not a FileNotFoundError error.
            print("Error: For some reason, the program could not read the input file. Please restart the program and input the material thicknesses via the command terminal. The program will now exit.")
            exit()
        
        if self.MaterialLibrary_DF.shape[0] == 0: # The user can remove media/materials from the file. This means they can empty it. The quiz needs at least one material to run.
            print("Error: The 'AttenuationQuiz_MaterialLibrary.csv' file is empty. Please specify at least one material in it and restart the program. The program will now exit.")
            exit()
        
        ## Make sure that the 'AttenuationQuiz_MaterialLibrary.csv' file is formatted correctly. The user can add, or even remove, materials from it.
        for row in range(0, self.MaterialLibrary_DF.shape[0]):
            try:
                assert self.MaterialLibrary_DF.iloc[row, 0] == str(self.MaterialLibrary_DF.iloc[row, 0])
            
            except:
                print("Error: The 'AttenuationQuiz_MaterialLibrary.csv' file is not formatted correctly at row {}. All entries in the first column, Material name, must be material names.".format(row + 1))
                print("Please fix the formatting of the file and restart the program. The program will now exit.")
                exit()
            

            try:
                assert self.MaterialLibrary_DF.iloc[row, 1] == int(self.check_FloatingPointInput(float(self.MaterialLibrary_DF.iloc[row, 1])))
            
            except:
                print("Error: The 'AttenuationQuiz_MaterialLibrary.csv' file is not formatted correctly at row {}. All entries in the second column, Atomic number, must be integers.".format(row + 1))
                print("Please fix the formatting of the file and restart the program. The program will now exit.")
                exit()
            

            try:
                assert self.MaterialLibrary_DF.iloc[row, 2] == self.check_FloatingPointInput(float(self.MaterialLibrary_DF.iloc[row, 2]))
            
            except:
                print("Error: The 'AttenuationQuiz_MaterialLibrary.csv' file is not formatted correctly at row {}. All entries in the third column, Atomic weight (g/mol), must be floating point numbers between {} and {}.".format(row + 1, FloatMin, FloatMax))
                print("Please fix the formatting of the file and restart the program. The program will now exit.")
                exit()
            

            try:
                assert self.MaterialLibrary_DF.iloc[row, 3] == self.check_FloatingPointInput(float(self.MaterialLibrary_DF.iloc[row, 3]))
            
            except:
                print("Error: The 'AttenuationQuiz_MaterialLibrary.csv' file is not formatted correctly at row {}. All entries in the fourth column, Mass density (g/cm^3), must be floating point numbers between {} and {}.".format(row + 1, FloatMin, FloatMax))
                print("Please fix the formatting of the file and restart the program. The program will now exit.")
                exit()
        
        
        try:
            self.NumberOfMediaToConsider = int(self.check_FloatingPointInput(float(input("How many media would you like to the quiz to consider? "))))
        
            while self.NumberOfMediaToConsider <= 0:
                print("Error: You must specify a positive integer for the number of media to consider. Please try again.")
                self.NumberOfMediaToConsider = int(self.check_FloatingPointInput(float(input("How many media would you like to the quiz to consider? "))))

        except:
            print("Error: You must specify a positive integer for the number of media to consider. The program will now exit.")
            exit()
        
        self.ChosenMaterials_DF = pd.DataFrame() # Initialise an empty pandas DataFrame for use in the FOR loop below.

        ### Choose a material from the library at random.
        for medium in range(0, self.NumberOfMediaToConsider):
            self.ChosenMaterials_DF = pd.concat([self.ChosenMaterials_DF, self.MaterialLibrary_DF.iloc[random.randint(0, self.MaterialLibrary_DF.shape[0] - 1)].T], axis = 1) # Randomly select a material to ask about in the attenuation quiz. For some reason, the inputs from the file would be read in transpose of what we expect. So we transpose the result later.
        
        self.ChosenMaterials_DF = self.ChosenMaterials_DF.T.reset_index(drop = True) # It is not necessary to transpose this DataFrame back to its original orientation.

        
        ### Add a column to the ChosenMaterials_DF DataFrame for collecting the user's predicted thickness(es) of the medium/media.
        self.ChosenMaterials_DF = (pd.concat([self.ChosenMaterials_DF, pd.DataFrame(np.zeros((self.ChosenMaterials_DF.shape[0], 1)))], axis = 1)).T.reset_index(drop = True).T
        
        print()

        for medium in range(0, self.ChosenMaterials_DF.shape[0]): # Show the user which materials were chosen.
            print("Chosen material {}:".format(medium + 1), self.ChosenMaterials_DF.iloc[medium, 0])
            print("Atomic number {} =".format(medium + 1), self.ChosenMaterials_DF.iloc[medium, 1])
            print("Atomic weight {} =".format(medium + 1), self.ChosenMaterials_DF.iloc[medium, 2], "g/mol")
            print("Mass density {} =".format(medium + 1), self.ChosenMaterials_DF.iloc[medium, 3], "g/cm^3")
            print()

        return self.ChosenMaterials_DF # This DataFrame is going to be used in the AttenuationQuiz class for the attenuation quiz.

    
    def choose_AlphaBeamCharacteristicsForAttenuationQuiz(self):
        self.MaximumAlphaEnergy_Quiz = 1e-3 # Units: MeV.
        
        # Randomly choose a *valid* initial kinetic energy for the alpha particles. For this value to be valid, it must be larger than the minimum kinetic energy that will be simulated.
        self.InitialKineticEnergy_Quiz = random.uniform(a = 0.0, b = 1.0) * self.MaximumAlphaEnergy_Quiz # Units: MeV.
        
        while self.InitialKineticEnergy_Quiz <= (self.MinimumAlphaEnergy_eV * 1e-6): # We do not want the initial kinetic energy being less than or equal to the minimum kinetic energy that will be simulated. The units for the energies here are MeV.
            self.InitialKineticEnergy_Quiz = random.uniform(a = 0.0, b = 1.0) * self.MaximumAlphaEnergy_Quiz # Recalculate the initial kinetic energy of the alpha particles.

        self.InitialParticleNumber_Quiz = 100 # Let it be a number that would not lead to computation times being too long.
        self.RandomDistribution_Quiz = "basic" # ... for now.

        return self.InitialKineticEnergy_Quiz, self.InitialParticleNumber_Quiz, self.RandomDistribution_Quiz
    

    def get_InputsForBeamAnalysisFromFile(self): # Read the inputs from a file so that I do not have to input them every time when I do a timing experiment.
        try:
            self.InputFile_BeamAnalysis = open("InputsForBeamAnalysis.txt", "r")
            self.InputFileLines_BeamAnalysis = self.InputFile_BeamAnalysis.readlines()
            self.InputFile_BeamAnalysis.close()
        
        except FileNotFoundError:
            print("Error: The text file named 'InputsForBeamAnalysis' was not found. Please make sure that there is such a file in the same directory as the script file of this program and try again. The program will now exit.")
            exit()
        
        except: # ... in case the error is not a FileNotFoundError error.
            print("Error: For some reason, the program could not read the input file. Please restart the program and input the material thicknesses via the command terminal. The program will now exit.")
            exit()

        # The format of the input file is very strict.
        try:
            self.InitialKineticEnergy_FileInput = self.check_FloatingPointInput(float(self.InputFileLines_BeamAnalysis[0].replace("Initial kinetic energy of the alpha particles = ", "").replace(" MeV", "")))
            self.InitialParticleNumber_FileInput = int(self.check_FloatingPointInput(float(self.InputFileLines_BeamAnalysis[1].replace("Initial particle number = ", ""))))
            self.RandomDistribution_FileInput = str(self.InputFileLines_BeamAnalysis[2].replace("Probability density function = ", "").replace("\n",""))
            self.WhetherOrNotToSeed_FileInput = str(self.InputFileLines_BeamAnalysis[3].replace("Whether or not to seed = ", "").replace("\n",""))
            self.AtomicNumber_FileInput = int(self.check_FloatingPointInput(float(self.InputFileLines_BeamAnalysis[5].replace("Atomic number of the medium = ", ""))))
            self.AtomicWeight_FileInput = int(self.check_FloatingPointInput(float(self.InputFileLines_BeamAnalysis[6].replace("Atomic weight of the medium = ", "").replace(" g/mol", ""))))
            self.MassDensity_FileInput = int(self.check_FloatingPointInput(float(self.InputFileLines_BeamAnalysis[7].replace("Mass density of the medium = ", "").replace(" g/cm^3", ""))))
            self.SimInstances_FileInput = int(self.check_FloatingPointInput(float(self.InputFileLines_BeamAnalysis[8].replace("Number of simulation instances = ", ""))))
        
        except:
            print("Error when reading the input file: Please make sure that the file's contents are formatted as follows. Then try running the program again. Alternatively, provide the inputs manually.")
            print("#" * 10, "Start of input file: Read from the next line", "#" * 10)
            print("Initial kinetic energy of the alpha particles = 1e-2 MeV")
            print("Initial particle number = 20")
            print("Probability density function = basic")
            print("Whether or not to seed = y")
            print("Seed = 0")
            print("Atomic number of the medium = 1")
            print("Atomic weight of the medium = 1 g/mol")
            print("Mass density of the medium = 1 g/cm^3")
            print("Number of simulation instances = 2")
            print("#" * 10, "End of input file: Ignore this line", "#" * 10)
            print("You may provide any valid input after the '= ' that you would otherwise provide manually via the command terminal. The inputs shown here are an example.")
            exit()

        return self.InitialKineticEnergy_FileInput, self.InitialParticleNumber_FileInput, self.RandomDistribution_FileInput, self.WhetherOrNotToSeed_FileInput, self.AtomicNumber_FileInput, self.AtomicWeight_FileInput, self.MassDensity_FileInput, self.SimInstances_FileInput
    
        # REFERENCES:
            # Programiz Python Exception Handling Using try, except and finally statement, https://www.programiz.com/python-programming/exception-handling.

    
    def get_InputsForRTGameFromFile(self): # Read the inputs from a file so that I do not have to input them every time when I do a timing experiment.
        try:
            self.InputFile_RTGame = open("InputsForRTGame.txt", "r")
            self.InputFileLines_RTGame = self.InputFile_RTGame.readlines()
            self.InputFile_RTGame.close()

        except FileNotFoundError:
            print("Error: The text file named 'InputsForRTGame' was not found. Please make sure that there is such a file in the same directory as the script file of this program and try again. The program will now exit.")
            exit()
        
        except: # ... in case the error is not a FileNotFoundError error.
            print("Error: For some reason, the program could not read the input file. Please restart the program and input the material thicknesses via the command terminal. The program will now exit.")
            exit()

        # The format of the input file is very strict.
        try:
            self.InitialKineticEnergy_FileInput = self.check_FloatingPointInput(float(self.InputFileLines_RTGame[0].replace("Initial kinetic energy of the alpha particles = ", "").replace(" MeV", "")))
            self.InitialParticleNumber_FileInput = int(self.check_FloatingPointInput(float(self.InputFileLines_RTGame[1].replace("Initial particle number = ", ""))))
            self.RandomDistribution_FileInput = str(self.InputFileLines_RTGame[2].replace("Probability density function = ", "").replace("\n",""))
            self.WhetherOrNotToSeed_FileInput = str(self.InputFileLines_RTGame[3].replace("Whether or not to seed = ", "").replace("\n",""))
            self.BeamHeight_FileInput = self.check_FloatingPointInput(float(self.InputFileLines_RTGame[5].replace("Beam height = ", "").replace(" cm", "")))
            self.BeamWidth_FileInput = self.check_FloatingPointInput(float(self.InputFileLines_RTGame[6].replace("Beam width = ", "").replace(" cm", "")))
        
        except:
            print("Error when reading the input file: Please make sure that the file's contents are formatted as follows. Then try running the program again. Alternatively, provide the inputs manually.")
            print("#" * 10, "Start of input file: Read from the next line", "#" * 10)
            print("Initial kinetic energy of the alpha particles = 1e-2 MeV")
            print("Initial particle number = 50")
            print("Probability density function = basic")
            print("Whether or not to seed = y")
            print("Seed = 0")
            print("Beam height = 1 cm")
            print("Beam width = 1 cm")
            print("#" * 10, "End of input file: Ignore this line", "#" * 10)
            print("You may provide any valid input after the '= ' that you would otherwise provide manually via the command terminal. The inputs shown here are an example.")
            exit()

        return self.InitialKineticEnergy_FileInput, self.InitialParticleNumber_FileInput, self.RandomDistribution_FileInput, self.WhetherOrNotToSeed_FileInput, self.BeamHeight_FileInput, self.BeamWidth_FileInput
    
        # REFERENCES:
            # Programiz Python Exception Handling Using try, except and finally statement, https://www.programiz.com/python-programming/exception-handling.


    def initialise_TimersForMain(self):
        self.ExecutionTime_main_SimDistance_Option_Input = 0.0
        self.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input = 0.0
        self.ExecutionTime_program_admin_get_InputsForAlphaBeam = 0.0
        self.ExecutionTime_program_admin_get_InputsForMedium = 0.0
        self.ExecutionTime_main_SimInstances_Input = 0.0
        self.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input = 0.0
        self.ExecutionTime_main_AnalyseBeam_AppendTimingResults = 0.0

        return self.ExecutionTime_main_SimDistance_Option_Input, self.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input, self.ExecutionTime_program_admin_get_InputsForAlphaBeam, self.ExecutionTime_program_admin_get_InputsForMedium, self.ExecutionTime_main_SimInstances_Input, self.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input, self.ExecutionTime_main_AnalyseBeam_AppendTimingResults

    # REFERENCES:
        # Zelle, J M (2017). Python Programming: An Introduction to Computer Science, 3rd ed. 2154 NE Broadway, Suite 100, Portland, Oregon 97232: Franklin, Beedle & Associates Inc.
        # Nymeria. (2018). How to fix this? ValueError: invalid literal for int() with base 10 error in Python. Retrieved from https://www.edureka.co/community/30685/this-valueerror-invalid-literal-for-with-base-error-python
        # Python Software Foundation. (2020, 11 September 2020). random — Generate pseudo-random numbers. Retrieved from https://docs.python.org/3/library/random.html
        # Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
        # Fayek, H (2020). Week 4 I/O, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
        # Fayek, H. (2020). Week 5 Functions and Modularity. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
        # National Institute of Standards and Technology Atomic Weights and Isotopic Compositions for All Elements, https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&ascii=html&isotype=all.
        # CRC handbook of chemistry and physics : a ready-reference book of chemical and physical data, 2017). 97 ed. 6000 Broken Sound Parkway NW, Suite 300 Boca Raton, FL 33487-2742: Taylor & Francis Group, LLC.
        # the pandas development team (2014). pandas.read_csv, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html.
if __name__ == "__main__":
    timing_studies.end_ClassDefinition_ProgramAdmin = time.time()
    timing_studies.append_TimingResults("ProgramAdmin class definition", timing_studies.end_ClassDefinition_ProgramAdmin - timing_studies.start_ClassDefinition_ProgramAdmin, "Once")

    timing_studies.start_ClassDefinition_AlphaParticles = time.time()


class AlphaParticles(ErrorChecking): # *Define* a class for the alpha particles.
    def __init__(self, InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity): # The arguments of the __init__() method, except the "self" argument, are what the user inputs when the program is run.
        super().__init__() # Inherit the MinimumAlphaEnergy_eV variable.

        # Here are some constants that are going to be used in the simulation. They are taken from the references specified below.
        self.ElectronMass = 0.0005485803 # ... in units of u, or g/mol.
        self.ClassicalElectronRadius_m = 2.8179403227e-15 # ... in units of m. This value is the classical electron radius and is going to be used for determining the cross-section of an alpha particle interacting with an electron. A cross-section is a measure of the probability of interaction/collision.
        self.ClassicalElectronRadius_cm = self.ClassicalElectronRadius_m * 1e2 # ... in units of cm.
        self.AlphaMass = 4.00150618 # ... in units of u, or g/mol. An alpha particle is 7300 times heavier than an electron.
        self.AvogadrosNum = 6.022140857e23 # Avogadro's number, in units of /mol. This constant can be used to convert the mass of 1 mol of alpha particles to the mass of 1 alpha particle.
        self.J_eV_ConversionFactor = 1.6021766208e-19 # ... in units of J/eV. This conversion factor can be used to convert between energy units of J and eV, where 1 eV is equal to the kinetic energy that an electron has when it is accelerated from rest through 1 V of potential difference. The eV is a practical unit for expressing the kinetic energies of subatomic particles. If we used the J, the numbers will be very small and possibly difficult to visualise.

        self.AlphaMass_kg = (self.AlphaMass / self.AvogadrosNum) * 1e-3 # ... in units of kg. Expressing the mass of a subatomic particle in kg is necessary for working with momentum vectors in SI units.
        self.ElectronMass_kg = (self.ElectronMass / self.AvogadrosNum) * 1e-3 # ... in units of kg. Expressing the mass of a subatomic particle in kg is necessary for working with momentum vectors in SI units.

        # Initialise conditions for alpha particles to stay in the beam.
        self.MinimumAlphaMomentum = (2 * self.AlphaMass_kg * self.MinimumAlphaEnergy_eV * self.J_eV_ConversionFactor) ** (1/2) # ... in units of kg m/s. The program keeps track of the alpha particles' energy by their momentum. Thus, it must calculate the momentum-equivalent of the minimum energy.
        
        # Diagonal elements of the randomised 3x3 matrix, RandomMatrix. They are constant.
        # The matrix has the form [[C_xx     C_yx     C_zx]
        #                          [C_xy     C_yy     C_zy]
        #                          [C_xz     C_yz     C_zz]]
        # When an alpha particle collides with an electron head-on, it is *not* deflected from its initial path, but slows down. In this case, the off-diagonal elements of the matrix are 0 while the diagonal elements are as they are defined below.
        self.C_xx = (1 - 4 * self.ElectronMass / self.AlphaMass) ** (1/2)
        self.C_yy = (1 - 4 * self.ElectronMass / self.AlphaMass) ** (1/2)
        self.C_zz = (1 - 4 * self.ElectronMass / self.AlphaMass) ** (1/2)

        # REFERENCES:
            # National Institute of Standards and Technology. Atomic Weights and Isotopic Compositions for All Elements. Retrieved from https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&ascii=html&isotype=all
            # CRC handbook of chemistry and physics : a ready-reference book of chemical and physical data. (2017).  (97 ed.). 6000 Broken Sound Parkway NW, Suite 300 Boca Raton, FL 33487-2742: Taylor & Francis Group, LLC.
        
        # Here are some variables that are going to be used in the simulation. They are defined in the __init__() method because they must be present in the computer's memory before anything else in the class.
        self.InitialKineticEnergy = InitialKineticEnergy # The user specifies the initial kinetic energy of the alpha particles.
        self.InitialMomentumX = (2 * self.AlphaMass_kg * InitialKineticEnergy * 1e6 * self.J_eV_ConversionFactor) ** (1/2) # The simulation keeps track of each alpha particle by a momentum vector. It actually sees each particle as a momentum vector. This is equation converts from kinetic energy to momentum assuming that the alpha particle is travelling at a *non-relativistic* velocity. The positive square root is taken because the alpha particle starts off travelling in the *positive* direction of the x-axis. In this equation, the units of the kinetic energy of the alpha particle must be converted from MeV to J. While considering the *relativistic* kinetic energies of the particles is more accurate than considering their *non-relativistic* kinetic energies, I must know their velocities. And to know their velocities, I must implement a metric spatial coordinate system to tell the program what is 1 cm, 1 mm, etc.. I may implement the concept of distance into a future version of the program - maybe in Assignment 3.
        
        self.InitialParticleNumber = InitialParticleNumber # The initial number of particles in the beam is going to be used in calculating the mean range and maximum range of the alpha particles. The mean range is defined as the distance from the source that 50% of all initial alpha particles arrive at.
        self.ParticleNumber = InitialParticleNumber # At the start of the simulation, the beam of alpha particles has the initial number of alpha particles that the user defined. However, as the simulation progresses, some alpha particles will leave the beam, thus decreasing the number of alpha particles in the beam. This variable is for keeping track of the number of alpha particles in the beam throughout the simulation.
        self.RandomDistribution = RandomDistribution # The user can specify which probability density function the program will use to generate random numbers. The random numbers affected by the choice of this probability density function will be used to generate the randomised 3x3 matrix, RandomMatrix. RandomMatrix is to be used to repeatedly update the momentum vector of every alpha particle.
        self.AmountOfNumbers = None # Define the AmountOfNumbers variable for *immediate* use in an IF statement in the randomNum_0to1() method. The main reason of this line of code is to avoid the error that says the variable is not defined when it is called in the IF statement.
        
        self.MeanRange_Description = "" # Prepare a description about the mean range. Depending on the user's inputs, the mean range may not be assigned a value as expected. This variable is used in the write() method that creates a text file of the data to be outputted from the program. An empty string is its default value.
        self.MaximumRange_Description = "" # Prepare a description about the maximum range. Depending on the user's inputs, the maximum range may not be assigned a value as expected. This variable is used in the write() method that creates a text file of the data to be outputted fromt the program. An empty string is its default value.
        
        self.MeanRange = None # Make the MeanRange variable available for use in IF/ELIF conditions without assigning a value to it. The IF/ELIF statements are for handling errors associated with this variable not having a value assigned to it during the simulation.
        self.MaximumRange = None # Prepare the MaximumRange variable for cases where it is not assigned a value when it should be.
        self.MeanRange_Backwards = None # ... for error handling.
        self.MeanRange_Forwards = None # ... for error handling.

        # Define the variables needed for the case where the simulation is run in terms of distance travelled through a medium.
        self.InitialPositionX = 0.0 # This is the initial position of the alpha particles along the x-axis. The beam travels along the positive direction of the x-axis.

        # Define the variables needed for specifying the medium.
        self.AtomicNumber = AtomicNumber
        self.AtomicWeight = AtomicWeight
        self.MassDensity = MassDensity
        
        # REFERENCES:
            # Krane, K. S. (2014). Introductory Nuclear Physics (Reprint ed.). Durga Printo Graphics, Delhi: John Wiley & Sons, Inc.
            # W3Schools. (2020). Python None Keyword. Retrieved from https://www.w3schools.com/python/ref_keyword_none.asp
        
    
    def make_Medium(self):
        self.ElectronSpatialDensity = self.AtomicNumber * (self.MassDensity * self.AvogadrosNum / self.AtomicWeight) # Units: cm^-3. This variable is the number of electrons in the medium per unit volume.
        print()

        # REFERENCES:
            # Nave, C R Scattering Cross Section, http://hyperphysics.phy-astr.gsu.edu/hbase/Nuclear/crosec.html.

    
    def initialise_Simulation(self, instance): # Prepare the arrays, lists and other variables that are to be used in the simulation using what was defined in the class's __init__() method.
        print("Simulation Instance", instance + 1, "has been started with __name__ ==", __name__, "...")
        
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__": # All of these time.time() calls must be protected with this IF statement so that the slave processes do not raise the "NameError: name 'timing_studies' is not defined" error.
        #     timing_studies.start_InitialiseSimulation = time.time()
        
        # All of the alpha particles in the beam are going to be kept track of using a pandas DataFrame. We want to keep track of each particle's momentum vector and x-position.
        self.AlphaParticleIDsList = np.array(list([range(0, self.InitialParticleNumber)])).T # Initialise a list for making a list of identification (ID) numbers for the alpha particles.
        
        # Now we initialise their x-positions, i.e., their positions along the x-axis.
        self.PositionXArray = np.array([[self.InitialPositionX]] * self.InitialParticleNumber) # Now there is one position along the x-axis for each alpha particle. We want a column vector, not a row vector.
        # NOTE: Before optimisation ...
        # self.PositionXList_DF = pd.DataFrame([self.InitialPositionX] * self.InitialParticleNumber) # Now there is one position along the x-axis for each alpha particle.

        ## Now we initialise their momentum vectors.
        # Initialise a general momentum vector for the alpha particles.
        self.MomentumVectorList = np.array([[self.InitialMomentumX, 0.0, 0.0]] * self.InitialParticleNumber)  # This is the list of inital momentum vectors of the alpha particle, in units of kg m/s. At the start of the first simulation step, every alpha particle has this momentum vector. *Initialise* a list of momentum vectors to keep track of each alpha particle's momentum. Now there is one momentum vector for each alpha particle. The [] around each individual momentum vector makes sure that each momentum vector is its own list. Treating the list of momentum vectors as a numpy array is necessary for making the calculations in the simulation involving vectors and matrices work properly.
        # NOTE: Before optimisation ...
        # self.MomentumVectorList_DF = pd.DataFrame([self.MomentumVector] * self.InitialParticleNumber) # *Initialise* a list of momentum vectors to keep track of each alpha particle's momentum. Now there is one momentum vector for each alpha particle. The [] around "MomentumVector" makes sure that each momentum vector is its own list. Treating the list of momentum vectors as a numpy array is necessary for making the calculations in the simulation involving vectors and matrices work properly.

        ## Now we calculate the cross-sections, which is a function of the alpha particle's energy. Consequently, each alpha particle will have its own mean free path.
        # We are going to need to know the momentum magnitude of each alpha particle. Also, the magnitude is used in other parts of the program. So, we might as well put it into the information DataFrame so that it does not have to be recalculated unnecessarily.
        self.MomentumMagnitudeList = np.array([((self.MomentumVectorList ** 2).sum(axis = 1)) ** (1/2)]).T # Momentum magnitudes. We need the arrays to be in columns for the upcoming concatenation into the info list.
        self.CrossSectionList = (2 * math.pi * self.AlphaMass_kg * (self.ClassicalElectronRadius_m) ** 2) / self.MomentumMagnitudeList ** 2 # Cross-section for each alpha particle. The pandas Series supports an element-wise operation.
        self.MeanFreePathInMediumList = (self.ElectronSpatialDensity * self.CrossSectionList) ** -1 # Mean free path in the medium for each alpha particle.
        # NOTE: Before optimisation ...
        # self.MomentumMagnitudeList_DF = ((self.MomentumVectorList_DF ** 2).sum(axis = 1)) ** (1/2) # Momentum magnitudes.
        # self.CrossSectionList_DF = (2 * math.pi * self.AlphaMass_kg * (self.ClassicalElectronRadius_m) ** 2) / self.MomentumMagnitudeList_DF ** 2 # Cross-section for each alpha particle. The pandas Series supports an element-wise operation.
        # self.MeanFreePathInMediumList_DF = (self.ElectronSpatialDensity * self.CrossSectionList_DF) ** -1 # Mean free path in the medium for each alpha particle.


        # Now we put all the above information into one pandas DataFrame.
        self.AlphaParticlesInfoList_ID_X_Momentum = np.concatenate((self.AlphaParticleIDsList, self.PositionXArray, self.MomentumVectorList, self.MomentumMagnitudeList, self.CrossSectionList, self.MeanFreePathInMediumList), axis = 1) # This DataFrame will be useful for keeping each alpha particle's momentum vector attached to its x-position, especially when particles get removed from the beam when they have sufficiently low momentum.
        # NOTE: Before optimisation ...
        # self.AlphaParticlesInfoList_ID_X_Momentum_DF = pd.concat([pd.DataFrame(self.AlphaParticleIDsList), self.PositionXList_DF, self.MomentumVectorList_DF, self.MomentumMagnitudeList_DF, self.CrossSectionList_DF, self.MeanFreePathInMediumList_DF], axis = 1).T.reset_index(drop = True).T # This DataFrame will be useful for keeping each alpha particle's momentum vector attached to its x-position, especially when particles get removed from the beam when they have sufficiently low momentum.

        # *Initialise* a list for recording the number of alpha particles in the beam at each simulation step. Energy and range straggling of the particles does *not* affect the number of particles in the beam. Energy straggling is when all of the alpha particles start off with the same kinetic energy but lose different amounts of energy per collision with atomic electrons. Each particle has its own history of collisions and energy transfers. Particles with more energy travel further. Thus, energy straggling causes range straggling. Energy straggling is what causes the sigmoid curve at the end of the plot of the relationship between the number of particles in the beam and the simulation step. This plot is output from the program as a .png file.
        self.NumberParticlesInBeam = [self.InitialParticleNumber] # It is not necessary to treat this list as a numpy array because it is not used in any vector or matrix calculations.

        # Initialise a list for recording the numbers of the off-diagonal elements of the randomised 3x3 matrix (RandomMatrix). They are generated from the random numbers generated using the randomNum_0to1() method. The frequency of the occurrence of each RandomMatrix random number is going to be plotted to get an idea of the probability density function that was used to generate the numbers. The plot will be useful for the user for understanding the results of the simulation because which random numbers are generated affects the results.
        self.RandomNumList_C_xy = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_xz = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_yx = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_yz = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_zx = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_zy = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        
        self.DelayForShowingProgress = 2.5 # Units: s. Do not print the progress of each simulation instance to the command terminal at each simulation step, which would flood the terminal with text.
        self.DelayTimer = 0.0
        self.StartDelayTimer = None # This is one of my typical solutions for avoiding the error of a variable being referenced in an IF statement before being defined.
        
        if instance == 0: # Print this message only once.
            print("Alpha particles will be removed from the beam when their kinetic energies fall below {0:0.3f} eV.".format(self.MinimumAlphaEnergy_eV)) # At which kinetic energy alpha particles are removed from the beam affects the results that the program outputs. The user must know what is affecting their results so that they may document it in their work/research. The minimum alpha kinetic energy may not be 1 eV, but may be expressed by a demical number in the future. Using the format() method keeps such numbers neatly presented.
            print() # Separate the above print() statement from text that is going to be printed to the screen later.


        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_InitialiseSimulation = time.time()
        #     timing_studies.initialise_Simulation_List.append(timing_studies.end_InitialiseSimulation - timing_studies.start_InitialiseSimulation)
        
        # REFERENCES:
            # grassworm, & Cees Timmerman. (2020, 16 May 2020). Display a decimal in scientific notation. Retrieved from https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
            # The SciPy community (2020). numpy.concatenate, https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html.

        
    def randomNum_0to1(self, RandomDistribution): # Use this function to shorten the code that generates random numbers between 0 and 1 when giving the user the option to choose which random distribution to use for generating the random numbers. The higher the value of AmountOfNumbersMinus1, the more numbers between 0 and 1 that can be generated; this is better than having less numbers between 0 and 1 being generated. For example, randomNum_0to1(2) generates 0.0, 0.5 or 1.
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.start_RandomNum_0to1 = time.time()

        if self.RandomDistribution == "basic": # Use the basic random number generator of Python's random module.
            # NOTE: Before multiprocessing ...
            # if __name__ == "__main__":
            #     timing_studies.end_RandomNum_0to1 = time.time() # The use of the RETURN statement below mean that the end time.time() calls and appending of execution times must happen before the RETURN statements.
            #     timing_studies.randomNum_0to1_List.append(timing_studies.end_RandomNum_0to1 - timing_studies.start_RandomNum_0to1)
            
            return random.random()
        
        elif self.RandomDistribution == "discrete": # Use a probability density function of which the user can specify the discretisation. Numbers have an equal probability of being generated.
            try: # Approach the error handling for the AmountOfNumbers variable in the same way as the error-handling for the InitialParticleNumber variable was approached because both these variables must be an integer greater than 0.
                if self.AmountOfNumbers is None: # Ask the user to specify a value for AmountOfNumbers only if it does not already have a value. Without this IF statement, the user will be asked to input a value for this variable *every time the randomNum_0to1() method is called* in the case where the user specifed a discrete random distribution.
                    self.AmountOfNumbers = int(self.check_FloatingPointInput(float(input("\tOption: discrete\n\t\tHow many random numbers between 0 and 1 inclusive should be possible to be generated? "))) - 1)
            
            except:
                print("Error: You did not input an integer greater than 0 for the number of numbers that can be randomly generated. The program will now exit.")
                exit() # This is what I want the program to do in this case.
            
            while self.AmountOfNumbers <= 0: # ... if the user specified an integer value but it is negative.
                print("Error: You must input an integer greater than 0 for the number of numbers to be randomly generated. Please try again.")
                
                try:
                    self.AmountOfNumbers = int(self.check_FloatingPointInput(float(input("\tOption: discrete\n\t\tHow many random numbers between 0 and 1 inclusive should be possible to be generated? "))) - 1)
                
                except: # ... if the user gave an input that would raise an error.
                    print("You did not input an integer greater than 0. The program will now exit.")
                    exit() # This is what I want the program to do in this case.

            # NOTE: Before multiprocessing ...
            # if __name__ == "__main__":
            #     timing_studies.end_RandomNum_0to1 = time.time()
            #     timing_studies.randomNum_0to1_List.append(timing_studies.end_RandomNum_0to1 - timing_studies.start_RandomNum_0to1)
            
            return float(random.randint(a = 0, b = self.AmountOfNumbers) / self.AmountOfNumbers) # Normalise the random numbers to 1. The random numbers are fractions of the largest number that can be generated.
            
            # REFERENCE: Python Software Foundation. (2013, 1 August 2013). PEP 8 -- Style Guide for Python Code. Retrieved from https://www.python.org/dev/peps/pep-0008/
        
        elif self.RandomDistribution == "triangular": # Use a probability density function that is biased towards 0 and linearly decreases from 0 to 1 and where it is zero at 1.
            # NOTE: Before multiprocessing ...
            # if __name__ == "__main__":
            #     timing_studies.end_RandomNum_0to1 = time.time()
            #     timing_studies.randomNum_0to1_List.append(timing_studies.end_RandomNum_0to1 - timing_studies.start_RandomNum_0to1)
            
            return float(random.triangular(low = 0.0, high = 1.0, mode = 0.0))
        
        elif self.RandomDistribution == "uniform": # Use a uniform probability density function.
            # NOTE: Before multiprocessing ...
            # if __name__ == "__main__":
            #     timing_studies.end_RandomNum_0to1 = time.time()
            #     timing_studies.randomNum_0to1_List.append(timing_studies.end_RandomNum_0to1 - timing_studies.start_RandomNum_0to1)
            
            return float(random.uniform(a = 0.0, b = 1.0)) # When this function is executed, the rest of the program sees the code after the RETURN keyword.
        
        # REFERENCES:
            # Python Software Foundation. (2020, 11 September 2020). random — Generate pseudo-random numbers. Retrieved from https://docs.python.org/3/library/random.html
    
    
    def update_AlphaParticlePosition(self):
        ### Timing experiment:
        # This method is going to be executed many times per alpha particle. If we measure its execution time only once, we may not get a useful result. It is better to measure its average execution time. This means we must know how many times it has been executed. Let us use a temporary object for measuring each execution's runtime.
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.start_UpdateAlphaParticlePosition = time.time()
        
        ## Update the x-positions of the alpha particles.
        # Now we are going to update the positions of the alpha particles along the x-axis using the momentum unit vectors. We are going to express the distances travelled along the x-axis in terms of free paths. A free path is the distance an alpha particle has travelled without colliding with an electron. In this program, we are assuming the free paths are straight. The free paths are only magnitudes. However, the directions of the free paths affect how far each alpha particle travels along the x-axis. We can assign directions to the free paths by calculating the unit vectors of the momenta. A unit vector has a magnitude of 1, so it is only a direction and will not make any change to the magnitude of a free path.
        self.FreePathList = -1*np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 7]]).T * np.log(1 - np.random.uniform(low = 0, high = 1 + 1.1 * self.FloatMin, size = (self.AlphaParticlesInfoList_ID_X_Momentum.shape[0], 1))) # Alpha particles have a mean free path in media that depends on the probability that they will interact with the electrons, which in turn depends on the kinetic energies of the alpha particles. Each particle has its own free path. The np.random.uniform() method excludes the high endpoint. To include 1 in the range of values that can be generated, we increase the endpoint beyond 1 by an extremely small amount. With "-" at the front of the expression, the "bad operand type for unary -: NoneType" error was raised. So I replaced "-" with "-1*".
        # NOTE: Before optimisation ...
        # self.FreePathList = -np.array(self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:, 7]).reshape(1, self.AlphaParticlesInfoList_ID_X_Momentum_DF.shape[0]) * np.log(1 - np.random.rand(1, self.AlphaParticlesInfoList_ID_X_Momentum_DF.shape[0])) # Alpha particles have a mean free path in media that depends on the probability that they will interact with the electrons, which in turn depends on the kinetic energies of the alpha particles. Each particle has its own free path.
        
        # We are going to do matrix operations, which are better done using numpy arrays than pandas DataFrames.
        self.AlphaParticlesInfoList_ID_X_Momentum[:, 1] = self.AlphaParticlesInfoList_ID_X_Momentum[:, 1] + self.FreePathList.T * (self.AlphaParticlesInfoList_ID_X_Momentum[:, 2] / self.AlphaParticlesInfoList_ID_X_Momentum[:, 5])
        # NOTE: Before optimisation ...
        # self.AlphaParticlesInfoList_ID_X_Momentum = np.array(self.AlphaParticlesInfoList_ID_X_Momentum_DF)
        # self.MomentumMagnitudeList = np.array(self.MomentumMagnitudeList_DF)

        # self.AlphaParticlesInfoList_ID_X_Momentum_Transpose = self.AlphaParticlesInfoList_ID_X_Momentum.T # Apparently, the .T method cannot be used at the left side of the "=" operator.
        # self.AlphaParticlesInfoList_ID_X_Momentum_Transpose[1] = self.AlphaParticlesInfoList_ID_X_Momentum_Transpose[1] + self.FreePathList * (self.AlphaParticlesInfoList_ID_X_Momentum_Transpose[2] / self.AlphaParticlesInfoList_ID_X_Momentum_Transpose[5])
        # self.AlphaParticlesInfoList_ID_X_Momentum = self.AlphaParticlesInfoList_ID_X_Momentum_Transpose.T

        # self.AlphaParticlesInfoList_ID_X_Momentum_DF = pd.DataFrame(self.AlphaParticlesInfoList_ID_X_Momentum) # Appending columns to other columns is better done using pandas DataFrames than with numpy arrays. See the record_AlphaParticlePosition() method.
        

        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_UpdateAlphaParticlePosition = time.time()
        #     timing_studies.update_AlphaParticlePosition_List.append(timing_studies.end_UpdateAlphaParticlePosition - timing_studies.start_UpdateAlphaParticlePosition) # This is the execution time for one execution of the update_AlphaParticlePosition() method.
        
        # REFERENCES:
            # Johnston, P, Merchant, A, Taylor, M, Franich, R & Supple, J (2020). Lecture 2: Fundamentals and extensions to radiation transport, PHYS2139 – Radiotherapy Physics and Modelling, RMIT University.
            # The SciPy community (2020). numpy.log, https://numpy.org/doc/stable/reference/generated/numpy.log.html.
            # The SciPy community (2020). numpy.random.uniform, https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html.
            # Python Software Foundation (2020). math — Mathematical functions, https://docs.python.org/3/library/math.html.
            # the pandas development team. pandas.DataFrame.iloc. pandas. Retrieved from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
            # the pandas development team. (2014). pandas.DataFrame.sum. pandas. Retrieved from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html
            # Fayek, H (2020). Week 2 Data Types, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Fayek, H (2020). Week 9 Scientific Python, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # the pandas development team (2014). Merge, join, and concatenate, https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html.
            # FlyingTeller (2018). Python Error - TypeError: bad operand type for unary -: 'NoneType', https://stackoverflow.com/questions/49029020/python-error-typeerror-bad-operand-type-for-unary-nonetype.
    
    
    def record_AlphaParticlePosition(self): # Record the x-positions for later plotting the number of alpha particles in the beam as a function of distance.
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.start_RecordAlphaParticlePosition = time.time()
         
        if np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 1]]).T.shape[0] == self.PositionXArray.shape[0]:
            self.PositionXArray = np.concatenate((self.PositionXArray, np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 1]]).T), axis = 1)
        
        else:
            _ = np.concatenate((np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 1]]).T, np.zeros((self.PositionXArray.shape[0] - np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 1]]).T.shape[0], 1))), axis = 0) # Unlike pandas, numpy does not concatenate arrays that have an unequal number of rows. So we must make the array that is to be added have the same number of rows as the array to which it is to be added. Using 0s for this is suitable for the data analysis that is to be done after the simulation.
            self.PositionXArray = np.concatenate((self.PositionXArray, _), axis = 1) 
        # NOTE: Before optimisation ...
        # self.PositionXList_DF = pd.concat([pd.DataFrame(self.PositionXList_DF), self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:, 1]], axis = 1) # It is favourable that pandas concatenates DataFrames with unequal numbers of columns. The NaN values can be dealt with later when we try to plot the number of particles in the beam as a function of x-position. The approach used here with the DataFrames is the DataFrame-equivalent of using the append() method for lists.
        
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_RecordAlphaParticlePosition = time.time()
        #     timing_studies.record_AlphaParticlePosition_List.append(timing_studies.end_RecordAlphaParticlePosition - timing_studies.start_RecordAlphaParticlePosition) # This is the execution time for one execution of the record_AlphaParticlePosition() method.

        # REFERENCES:
            # The SciPy community (2020). numpy.concatenate, https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html.
        
    
    def generate_RandomMatrix_Momentum(self):
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.start_GenerateRandomMatrixMomentum = time.time()
        
        # Prepare the 3x3 randomised matrix that is going to be used to update the momentum vectors of the alpha particles. RandomMatrix is the 3x3 randomised matrix.
        self.MeFirst = random.randint(a = 0, b = 1) # This variable is for the IF-ELIF statement below. It is for randomising which of the two matrix elements below are defined first and which one is derived from the one that was defined first.
        
        if self.MeFirst == 0:
            self.C_xy = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_xx) # The absolute values of the numbers in each column of RandomMatrix must sum to 1 because each column represents how much of the corresponding component of the momentum vector at the start of the simulation step is distributed amongst the components of the momentum vector at the end of the simulation step. RandomMatrix is recalculated for each alpha particle per simulation step.
            self.C_xz = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_xx - self.C_xy) # The absolute values of the numbers in each column of RandomMatrix must sum to 1.
        
        elif self.MeFirst == 1:
            self.C_xz = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_xx)
            self.C_xy = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_xx - self.C_xz)

        # The alpha particle may be deflected in either the positive or negative direction of the y- and z-axes.
        self.SignList = [-1,1] # C_xy and C_xz are to be randomly assigned a sign.
        
        self.C_xy = self.C_xy * self.SignList[random.randint(a = 0, b = 1)]
        self.C_xz = self.C_xz * self.SignList[random.randint(a = 0, b = 1)] # We randomly select a sign again to avoid *always* getting a "- -" or "+ +" pair. We also want "+ -" and "- +" pairs to be possible.
        self.RandomNumList_C_xy.append(self.C_xy) # We are going to plot a frequency plot of each off-diagonal element of the randomised 3x3 matrix. So we must record each value.
        self.RandomNumList_C_xz.append(self.C_xz) # We are going to plot a frequency plot of each off-diagonal element of the randomised 3x3 matrix. So we must record each value.

        ## C_yx and C_yz:
        self.MeFirst = random.randint(a = 0, b = 1) # This variable is for the IF-ELIF statement below. It is for randomising which of the two matrix elements below are defined first and which one is derived from the one that was defined first.
        
        if self.MeFirst == 0:
            self.C_yx = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_yy) # The absolute values of the numbers in each column of RandomMatrix must sum to 1 because each column represents how much of the corresponding component of the momentum vector at the start of the simulation step is distributed amongst the components of the momentum vector at the end of the simulation step. RandomMatrix is recalculated for each alpha particle per simulation step.
            self.C_yz = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_yy - self.C_yx) # The absolute values of the numbers in each column of RandomMatrix must sum to 1.
        
        elif self.MeFirst == 1:
            self.C_yz = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_yy)
            self.C_yx = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_yy - self.C_yz)

        # The alpha particle may be deflected in either the positive or negative direction of the x- and z-axes. We randomly select a pair of signs again for added randomness because the choice of deflection in the positive or negative direction of an axis between orthogonal axes are independent of each other.
        self.C_yx = self.C_yx * self.SignList[random.randint(a = 0, b = 1)]
        self.C_yz = self.C_yz * self.SignList[random.randint(a = 0, b = 1)] # We randomly select a sign again to avoid *always* getting a "- -" or "+ +" pair. We also want "+ -" and "- +" pairs to be possible.
        self.RandomNumList_C_yx.append(self.C_yx) # We are going to plot a frequency plot of each off-diagonal element of the randomised 3x3 matrix. So we must record each value.
        self.RandomNumList_C_yz.append(self.C_yz) # We are going to plot a frequency plot of each off-diagonal element of the randomised 3x3 matrix. So we must record each value.

        ## C_zx and C_zy:
        self.MeFirst = random.randint(a = 0, b = 1) # This variable is for the IF-ELIF statement below. It is for randomising which of the two matrix elements below are defined first and which one is derived from the one that was defined first.
        
        if self.MeFirst == 0:
            self.C_zx = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_zz) # The absolute values of the numbers in each column of RandomMatrix must sum to 1 because each column represents how much of the corresponding component of the momentum vector at the start of the simulation step is distributed amongst the components of the momentum vector at the end of the simulation step. RandomMatrix is recalculated for each alpha particle per simulation step.
            self.C_zy = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_zz - self.C_zx) # The absolute values of the numbers in each column of RandomMatrix must sum to 1.
        
        elif self.MeFirst == 1:
            self.C_zy = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_zz)
            self.C_zx = self.randomNum_0to1(self.RandomDistribution) * (1 - self.C_zz - self.C_zy)

        # The alpha particle may be deflected in either the positive or negative direction of the x- and y-axes. We randomly select a pair of signs again for added randomness because the choice of deflection in the positive or negative direction of an axis between orthogonal axes are independent of each other.
        self.C_zx = self.C_zx * self.SignList[random.randint(a = 0, b = 1)]
        self.C_zy = self.C_zy * self.SignList[random.randint(a = 0, b = 1)] # We randomly select a sign again to avoid *always* getting a "- -" or "+ +" pair. We also want "+ -" and "- +" pairs to be possible.
        self.RandomNumList_C_zx.append(self.C_zx) # We are going to plot a frequency plot of each off-diagonal element of the randomised 3x3 matrix. So we must record each value.
        self.RandomNumList_C_zy.append(self.C_zy) # We are going to plot a frequency plot of each off-diagonal element of the randomised 3x3 matrix. So we must record each value.

        self.RandomMatrix = np.array([[self.C_xx, self.C_yx, self.C_zx], [self.C_xy, self.C_yy, self.C_zy], [self.C_xz, self.C_yz, self.C_zz]]) # We now assemble the randomised 3x3 matrix because we have defined all of its elements for the alpha particle in the present simulation step. We define it as a numpy array because lists of lists are not always suitable for matrix multiplication while numpy arrays are.

        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_GenerateRandomMatrixMomentum = time.time()
        #     timing_studies.generate_RandomMatrix_Momentum_List.append(timing_studies.end_GenerateRandomMatrixMomentum - timing_studies.start_GenerateRandomMatrixMomentum) # This is the execution time for one execution of the generate_RandomMatrix_Momentum() method.
        
        # REFERENCE: Python Software Foundation (2020). random — Generate pseudo-random numbers, https://docs.python.org/3/library/random.html.

    
    def update_AlphaParticleMomentum(self): # This method is for recalculating each alpha particle's momentum vector after the alpha particles collide with atomic electrons.
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.start_UpdateAlphaParticleMomentum = time.time()
        
        for particle in range(0, self.ParticleNumber): # We are going to calculate each alpha particle's final momentum vector at the end of the simulation step. Here, we iterate the matrix calculation over the number of alpha particles in the beam. These calculations are done at each simulation step.
            self.generate_RandomMatrix_Momentum() # Generate the randomised 3x3 matrix for updating the momentum vectors of the alpha particles.
        
            # #### debug for the radiotherapy game.
            # print("Inside update_AlphaParticleMomentum(self)'s FOR loop with particle =", particle)
            # print("self.generate_RandomMatrix_Momentum() in update_AlphaParticleMomentum(self) has been executed successfully ...\n")
            # ####

            ## Update the momenta of the alpha particles.
            # Now we are going to use RandomMatrix to update the momentum vector of each alpha particle minus the alpha particles that were removed from the beam. Each alpha particle has its own RandomMatrix applied to it because the random numbers are recalculated for each alpha particle. I am assuming that how a particular alpha particle transfers momentum to an electron does *not* affect how another alpha particle transfers momentum to an electron, whether that electron is the same one or another one.
            
            self.AlphaParticlesInfoList_ID_X_Momentum[particle, 2:5] = self.RandomMatrix.dot(self.AlphaParticlesInfoList_ID_X_Momentum[particle, 2:5])
            

        # NOTE: Before optimisation, there was also the following line of code ...
        # self.AlphaParticlesInfoList_ID_X_Momentum_DF = pd.DataFrame(self.AlphaParticlesInfoList_ID_X_Momentum)

        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_UpdateAlphaParticleMomentum = time.time()
        #     timing_studies.update_AlphaParticleMomentum_List.append(timing_studies.end_UpdateAlphaParticleMomentum - timing_studies.start_UpdateAlphaParticleMomentum) # This is the execution time for one execution of the generate_RandomMatrix_Momentum() method.

        # REFERENCES:
            # the pandas development team. pandas.DataFrame.iloc. pandas. Retrieved from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
            # W3Schools. (2020). Python Operators. Retrieved from https://www.w3schools.com/python/python_operators.asp
            # the pandas development team. (2014). pandas.DataFrame.sum. pandas. Retrieved from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html
            # The SciPy community. (2020, 29 June 2020). numpy.dot. Retrieved from https://numpy.org/doc/stable/reference/generated/numpy.dot.html#numpy.dot
                    
    
    def update_ParticleNum(self): # This method *manages* how many alpha particles remain in the beam. Alpha particles leave the beam when they lose too much energy due to colliding with too many atomic electrons. When their energy is extremely low, they capture atomic electrons and become helium atoms, thus leaving the beam.
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.start_UpdateParticleNum = time.time()
        
        #     timing_studies.start_UpdateParticleNum_MomentumMagnitudeCalculation = time.time()
        
        self.AlphaParticlesInfoList_ID_X_Momentum[:, 5] = (self.AlphaParticlesInfoList_ID_X_Momentum[:, 2:5] ** 2).sum(axis = 1) ** (1/2) # Recalculate the momentum magnitude of each alpha particle.
        # NOTE: Before optimisation ...
        # self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:, 5] = ((self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:, 2:5] ** 2).sum(axis = 1) ** (1/2)) # Recalculate the momentum magnitude of each alpha particle.
        
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_UpdateParticleNum_MomentumMagnitudeCalculation = time.time()

        #     timing_studies.start_UpdateParticleNum_NumpyArrayMask = time.time()
        
        self.AlphaParticlesInfoList_ID_X_Momentum = self.AlphaParticlesInfoList_ID_X_Momentum[self.AlphaParticlesInfoList_ID_X_Momentum[:, 5] > self.MinimumAlphaMomentum] # Remove the alpha particles from the beam that have momenta less than MinimumAlphaMomentum, which is the minimum momentum that a particle must have to stay in the beam. This line of code does not actually remove the alpha particles that have less than the minimum momentum but extracts the particles with momenta higher than the minimum momentum.
        # NOTE: Before optimisation ...
        # self.AlphaParticlesInfoList_ID_X_Momentum_DF = self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:,:][self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:, 5] > self.MinimumAlphaMomentum] # Remove the alpha particles from the beam that have momenta less than MinimumAlphaMomentum, which is the minimum momentum that a particle must have to stay in the beam. This line of code does not actually remove the alpha particles that have less than the minimum momentum but extracts the particles with momenta higher than the minimum momentum.
        # self.AlphaParticlesInfoList_ID_X_Momentum_DF = self.AlphaParticlesInfoList_ID_X_Momentum_DF.reset_index(drop = True) # It is necessary to reset the row indices of the DataFrame now that some of the rows have been removed. Doing this should avoid problems with indexing the DataFrame later.
        
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_UpdateParticleNum_NumpyArrayMask = time.time()

        self.ParticleNumber = self.AlphaParticlesInfoList_ID_X_Momentum.shape[0] # Tell the ParticleNumber variable that the number of particles in the beam has changed. MomentumVectorList is a numpy array. Thus, we use the .shape method to extract how many rows it has.
        # NOTE: Before optimisation ...
        # self.ParticleNumber = self.AlphaParticlesInfoList_ID_X_Momentum_DF.shape[0] # Tell the ParticleNumber variable that the number of particles in the beam has changed. MomentumVectorList is a numpy array. Thus, we use the .shape method to extract how many rows it has.

        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_UpdateParticleNum = time.time()
        #     timing_studies.update_ParticleNum_List.append(timing_studies.end_UpdateParticleNum - timing_studies.start_UpdateParticleNum) # This is the execution time for one execution of the update_ParticleNum() method.

        #     timing_studies.update_ParticleNum_MomentumMagnitudeCalculation_List.append(timing_studies.end_UpdateParticleNum_MomentumMagnitudeCalculation - timing_studies.start_UpdateParticleNum_MomentumMagnitudeCalculation)
        #     timing_studies.update_ParticleNum_NumpyArrayMask_List.append(timing_studies.end_UpdateParticleNum_NumpyArrayMask - timing_studies.start_UpdateParticleNum_NumpyArrayMask)
        
        # REFERENCES:
            # the pandas development team. pandas.DataFrame.iloc. pandas. Retrieved from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
            # W3Schools. (2020). Python Operators. Retrieved from https://www.w3schools.com/python/python_operators.asp
            # the pandas development team. (2014). pandas.DataFrame.sum. pandas. Retrieved from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html
            # Rauf Bhat (2018). Key error: 0 with dataframe filtered from another dataframe, https://stackoverflow.com/questions/52872119/key-error-0-with-dataframe-filtered-from-another-dataframe/52872388.
            # the pandas development team (2014). pandas.DataFrame.reset_index, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html.
            # Fayek, H (2020). Week 9 Scientific Python, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
        
    
    def calculate_Data(self): # At the end of the simulation, we have a large DataFrame that has information about the x-position of each alpha particle in each simulation step. We want to make a histogram of the number of particles in the beam as a function of distance out of this DataFrame.
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.start_CalculateData = time.time()
        
        # At this point, each alpha beam object has a PositionXArray array that is to be analysed.
        ## Calculate the maximum range of the alpha particles. NOTE: The x-positions are in the same units as the mean free path, which has units of m.
        self.MaximumRange = self.PositionXArray.max().max() # The maximum range is the largest number in the array. It is the furthest distance an alpha particle in the beam has travelled. It is the easiest value to calculate out of the ones we are interested in. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method.
        # NOTE: Before optimisation ...
        # self.PositionXList_DF = ((self.PositionXList_DF.T).reset_index(drop = True)).T # First, we make sure its columns are labelled by the simulation steps rather than all having the same label due to having been concatenated together. The reset_index() method works row-wise, so we transpose the DataFrame first. Then we reset the row labels and transpose the DataFrame back to its original shape. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method. However, we use parentheses to make reading the code easier.
        # self.MaximumRange = self.PositionXList_DF.max().max() # The maximum range is the largest number in the DataFrame. It is the furthest distance an alpha particle in the beam has travelled. It is the easiest value to calculate out of the ones we are interested in. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method.
        
        ## Calculate the number of alpha particles remaining in the beam as a function of distance.
        self.NumOfDistancesToCheck = 5e2 # This variable is for specifying the number of points to be created using the np.linspace() method.
        self.DistancesToCheck = list(np.linspace(start = 0.0, stop = self.MaximumRange, num = int(self.NumOfDistancesToCheck), endpoint = True)) # Create the DistancesToCheckList to be zipped into a dictionary as values.

        self.NumbersList = list(range(0, len(self.DistancesToCheck))) # The list created here will be zipped into the dictionary for the DistancesToCheck list as keys.
        
        self.DistancesToCheck_Dict = dict(zip(self.NumbersList, self.DistancesToCheck))

        self.ParticleNumList_Distance = [] # This list is going to have the number of alpha particles remaining in the beam at each distance of interest.
        for distance_Key in range(0, len(self.DistancesToCheck_Dict)): # Use a nested FOR loop for now. Nested FOR loops are known to be relatively slow, but they get the job done in this case.
            self.ParticleNumber_DistanceCheck = self.InitialParticleNumber # Reset this variable for use in the FOR loop below.
            
            for particle in range(0, self.PositionXArray.shape[0]): # Check how many particles passed the distance of interest.
                if self.PositionXArray[particle, :].max() <= self.DistancesToCheck_Dict[distance_Key]: # For each particle that did not pass the distance of interest, decrement the ParticleNum variable by 1.
                    self.ParticleNumber_DistanceCheck = self.ParticleNumber_DistanceCheck - 1
            # NOTE: Before optimisation ...
            # for particle in range(0, self.PositionXList_DF.shape[0]): # Check how many particles passed the distance of interest.
            #     if self.PositionXList_DF.iloc[particle,:].max() <= self.DistancesToCheck_Dict[distance_Key]: # For each particle that did not pass the distance of interest, decrement the ParticleNum variable by 1.
            #         self.ParticleNumber_DistanceCheck = self.ParticleNumber_DistanceCheck - 1
            

            self.ParticleNumList_Distance.append(self.ParticleNumber_DistanceCheck)
       
        
        ## Calculate the mean range of the alpha particles.
        try: # It is possible that self.InitialParticleNumber // 2 not be in the ParticleNumList_Distance list in the case where more than 1 alpha particle leaves the beam at the same time at the time when slightly more than 50% of the initial number of particles remain in the beam.
            self.MeanRange = self.DistancesToCheck_Dict[self.ParticleNumList_Distance.index(self.InitialParticleNumber // 2)] # The mean range is defined as the distance beyond which 50% of the initial number of particles travel.
        
        except: # The code in the EXCEPT section is focused on assigning an alternative value to MeanRange in the case where InitialParticleNumber // 2 number of particles was skipped during the simulation because more than 1 particle was removed from the beam.
            for num in range(1, self.InitialParticleNumber // 2 + 1):
                try: # The code below can actually raise a ValueError error if a particular value is not found in the ParticleNumList_Distance list. Therefore, we include a TRY-EXCEPT code block in the FOR loop.
                    if self.InitialParticleNumber // 2 + num >= self.InitialParticleNumber: # If this is the case, search for the furthest distance that *all* of the particles travelled just before the first particle left the beam.
                        self.MeanRange_Backwards = self.DistancesToCheck_Dict[self.ParticleNumList_Distance.index(len(self.ParticleNumList_Distance) - 1 - self.ParticleNumList_Distance[::-1].index(self.InitialParticleNumber))] # The index() method searches for the specified element from the start of the list. However, we want the index of the *last* element, so we flip the list. Having found the index of the last element in the flipped list, we want to know its index in the original list, so we calculate the original index.
                    else:
                        self.MeanRange_Backwards = self.DistancesToCheck_Dict[self.ParticleNumList_Distance.index(self.InitialParticleNumber // 2 + num)]
                
                    if self.InitialParticleNumber // 2 - num <= 0: # We do not want self.InitialParticleNumber // 2 - num being negative, so we stop it from being so.
                        self.MeanRange_Forwards = self.DistancesToCheck[-1] # Unlike with MeanRange_Backwards when the condition in the IF statement just above is True, we want the index of the first occurrence of 0 particles. The simulation stops when the number of particles in the beam is 0, meaning that there is only one occurrence of 0 in the list of the number of particles in the beam. We use the list version rather than the dictionary version of DistancesToCheck because [-1] for a dictionary means "the key named '-1'", which is not what we want, while for a list it refers to the last element, which is what we want.
                    else:
                        self.MeanRange_Forwards = self.DistancesToCheck_Dict[self.ParticleNumList_Distance.index(self.InitialParticleNumber // 2 - num)]

                    if (self.MeanRange_Backwards is not None) and (self.MeanRange_Forwards is not None):
                        break # Now that we have assigned a value to each of the two variables above, we do not need to iterate "num" anymore. We have what we wanted.
                    else:
                        continue

                except:
                    continue # We want to use the normal behaviour of a FOR loop in that it goes to its next iteration. It is because of the ValueError error that we use a TRY-EXCEPT code block.
            
            self.MeanRange = np.array(self.MeanRange_Backwards, self.MeanRange_Forwards).mean() # The slope at the descending end of the plot of the number of particles in the beam as a function of distance is approximately linear. So we do linear interpolation. I prefer to use a numpy array and the mean() method instead of doing (a + b)/2, because the latter option seems a bit hard-coded to me.

        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_CalculateData = time.time()
        #     timing_studies.calculate_Data_List.append(timing_studies.end_CalculateData - timing_studies.start_CalculateData)
        
        # REFERENCES:
            # Fayek, H (2020). Week 9 Scientific Python, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # the pandas development team (2014). pandas.DataFrame.reset_index, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html.
            # the pandas development team (2014). pandas.DataFrame.max, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.max.html.
            # The SciPy community (2020). numpy.linspace, https://numpy.org/doc/stable/reference/generated/numpy.linspace.html.
            # GeeksforGeeks Python | Convert two lists into a dictionary, https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/.
            # Fayek, H (2020). Week 2 Data Types, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Programiz Python List index(), https://www.programiz.com/python-programming/methods/list/index.
            # Anand S Kumar (2015). What is the meaning of “int(a[::-1])” in Python? [duplicate], https://stackoverflow.com/questions/31633635/what-is-the-meaning-of-inta-1-in-python.
            # Programiz Python break and continue, https://www.programiz.com/python-programming/break-continue.
            # Krane, K S (2014). Introductory Nuclear Physics, Reprint ed. Durga Printo Graphics, Delhi: John Wiley & Sons, Inc.
    
    
    def plot_ParticleNum(self): # Plot the number of alpha particles in the beam as a function of simulation step. The AttenuationQuiz class inherits this method.
        plt.figure(figsize = (17, 7)) # Make the figure have dimensions that are suitable for seeing the relationship between the number of particles in the beam and the distance the beam travelled more clearly.
        plt.scatter(self.DistancesToCheck, self.ParticleNumList_Distance, marker = ".", alpha = 0.5) # I do not want the markers of the scatter plot to be too big lest the apparent curve be seen as too thick to see the relationship clearly. In general, the number of alpha particles in a beam travelling through a medium stays constant for some distance and then rapidly drops to 0 near the maximum range of the particles. The rapid drop in the number of particles in the beam as a function of distance tends to be sigmoidal in shape. Using an "alpha" less than 1 means that we can see the plot from each instance of the simulation.
        plt.xlabel("Distance /m") # The units of distance are cm.
        plt.ylabel("Number of alpha particles in the beam") # We are plotting the number of alpha particles remaining in the beam as a function of distance.
        plt.savefig(DirectoryToSaveTo + "AlphaRange_" + timestamp + ".png") # Save the plot externally from AlphaParticles2.py so that the user can refer to it later. Give it a unique name that will cause the file to probably never be overwritten by the program unless another run of the simulation ends in the same second as the previous run.

        # REFERENCES:
            # Hunter, J, Dale, D, Firing, E, Droettboom, M & The Matplotlib development team matplotlib.pyplot.figure, https://matplotlib.org/3.3.1/api/_as_gen/matplotlib.pyplot.figure.html.
            # Hunter, J., Dale, D., Firing, E., Droettboom, M., & The Matplotlib development team. matplotlib.markers. Retrieved from https://matplotlib.org/3.1.1/api/markers_api.html#module-matplotlib.markers
            # Welch, A. J. How to Save a Plot to a File Using Matplotlib. Retrieved from https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
            # Hunter, J., Dale, D., Firing, E., Droettboom, M., & The Matplotlib development team. matplotlib.pyplot.savefig. Retrieved from https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html
            # Knoll, G. F. (2010). Radiation Detection and Measurement (4th ed.). 111 River Street, Hoboken, NJ 07030-5774: John Wiley & Sons, Inc.
            # Hofmann, F. Creating and Deleting Directories with Python. Retrieved from https://stackabuse.com/creating-and-deleting-directories-with-python/
    
    
    def show_Progress(self, instance):
        if __name__ == "__main__":
            timing_studies.start_ShowProgress = time.time()
        
        try:
            ### Calculate the progress.
            if self.ParticleNumber != 0: # Keep showing the maximum alpha particle kinetic energy in the beam until there are no more particles in the beam. The maximum kinetic energy decreases throughout the entire simulation. However, the number of alpha particles in the beam stays constant until near the end of the simulation where it rapidly decreases to 0. Thus, letting the user see the maximum alpha particle kinetic energy rather than how many particles remain in the beam gives them a better measure of the progress of the simulation.
                self.MaximumAlphaMomentum_now = max(((self.AlphaParticlesInfoList_ID_X_Momentum[:, 2:5] ** 2).sum(axis = 1) ** (1/2))) # Given the momentum vectors of all of the alpha particles in the beam, I want to pick out the one that has the highest magnitude. *In the same simulation step*, use the pandas DataFrame of the list of momentum vectors to calculate the magnitudes of the vectors all at once. Then pick out the maximum magnitude.
                self.MaximumAlphaEnergy_now = ((self.MaximumAlphaMomentum_now ** 2 / (2 * self.AlphaMass_kg)) / self.J_eV_ConversionFactor) * 1e-6 # This is the equation E_alpha = p_alpha ** 2 / (2 * AlphaMass), where E_alpha and p_alpha are the kinetic energy and momentum magnitude of the alpha particle, respectively. I want the kinetic energy in MeV.

                self.Progress_Percentage = (1.0 - self.MaximumAlphaEnergy_now / (self.InitialKineticEnergy - self.MinimumAlphaEnergy_eV * 1e-6)) ** (10) * 100 # The maximum alpha particle kinetic energy does not decrease linearly, but approximately proportionally to the specified power, which was chosen through trial and error. The "* 100" is for converting the fraction to a percentage.

            
            ### Show the progress.
            self.EndDelayTimer = time.time()

            if (self.StartDelayTimer is None) or (self.DelayTimer > self.DelayForShowingProgress):
                self.StartDelayTimer = time.time() # Give this variable a value.

            self.DelayTimer = self.EndDelayTimer - self.StartDelayTimer
            
            if self.DelayTimer > self.DelayForShowingProgress: # This time period is how much to wait before showing another message of the progress of each simulation instance.
                print("\tThe progress of Simulation Instance {}".format(instance + 1) + " is {0:0.2f}% ...".format(self.Progress_Percentage)) # It seems that all or none of the {}s must have a specification of the formatting to avoid the "ValueError: cannot switch from automatic field numbering to manual field specification" error. (I tried it myself, so there is no reference to cite.) Alternatively, I can separate the strings and use string concatenation.
              
        except AttributeError: # AttributeError is the error I saw in the command terminal when I specified an initial alpha particle kinetic energy less than the minimum energy required for a particle to stay in the beam.
            print("Error: You must specify an initial alpha particle kinetic energy greater than {} eV. The program will now exit.".format(self.MinimumAlphaEnergy_eV))
            exit() # This is what I want to happen in this case.
        
        except:
            print("Unknown Error: The program will now exit. Please restart the program and try again.") # An error besides AttributeError may be raised for some reason. I want the program to catch the error rather than crash.
            exit() # This is what I want to happen in this case.
        
        if __name__ == "__main__":
            timing_studies.end_ShowProgress = time.time()
            timing_studies.show_Progress_List.append(timing_studies.end_ShowProgress - timing_studies.start_ShowProgress) # This is the execution time for one execution of the update_ParticleNum() method.
        
        # NOTE: Before optimisation ...
        # try: # At least the AttributeError occurs for the MaximumAlphaMomentum_now variable in these code blocks due to the user specifying an initial alpha particle kinetic energy less than or equal to the minimum energy required by the particles to stay in the beam.
        #     if self.ParticleNumber != 0: # Keep showing the maximum alpha particle kinetic energy in the beam until there are no more particles in the beam. The maximum kinetic energy decreases throughout the entire simulation. However, the number of alpha particles in the beam stays constant until near the end of the simulation where it rapidly decreases to 0. Thus, letting the user see the maximum alpha particle kinetic energy rather than how many particles remain in the beam gives them a better measure of the progress of the simulation.
        #         self.MaximumAlphaMomentum_now = max(((self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:,2:5] ** 2).sum(axis = 1) ** (1/2))) # Given the momentum vectors of all of the alpha particles in the beam, I want to pick out the one that has the highest magnitude. *In the same simulation step*, use the pandas DataFrame of the list of momentum vectors to calculate the magnitudes of the vectors all at once. Then pick out the maximum magnitude.
        #         self.MaximumAlphaEnergy_now = ((self.MaximumAlphaMomentum_now ** 2 / (2 * self.AlphaMass_kg)) / self.J_eV_ConversionFactor) * 1e-6 # This is the equation E_alpha = p_alpha ** 2 / (2 * AlphaMass), where E_alpha and p_alpha are the kinetic energy and momentum magnitude of the alpha particle, respectively. I want the kinetic energy in MeV.
                    
        #     # Show the user the progress of the simulation in terms of the maximum kinetic energy of the alpha particles in the beam. This IF-ELIF code block is a solution to not printing the maximum kinetic energy at the end of each simulation step, which would flood the command terminal. Not flooding the command terminal allows the user to see the notices and the other basic information that were printed to the terminal before they inputted values.
        #     self.show_MaximumAlphaEnergy = "\tThe maximum alpha particle kinetic energy in the beam is " + "{:.3e}".format(self.MaximumAlphaEnergy_now) + " MeV, which is " + "{:.3e}".format(self.MaximumAlphaEnergy_now / self.InitialKineticEnergy) + " times the initial alpha particle kinetic energy.\n\t..." # This variable is defined to avoid repeating this code for each IF/ELIF statement below. It is used in the print() functions. The tab (\t) is for making these messages appear associated with the message about which simulation instance is being run.

        #     # REFERENCES:
        #         # Zelle, J. M. (2017). Python Programming: An Introduction to Computer Science (B. Jones Ed. 3rd ed.). 2154 NE Broadway, Suite 100, Portland, Oregon 97232: Franklin, Beedle & Associates Inc.
        #         # grassworm, & Cees Timmerman. (2020, 16 May 2020). Display a decimal in scientific notation. Retrieved from https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
            
        #     # The ProgressMonitorValue variable was defined in the __init__() method of the class for the purpose of regulating the execution of the statements in this IF-ELIF code block. Each IF/ELIF statement is to be evaluated to True only once per run of the simulation. While each condition about the MaximumAlphaEnergy_now variable may be evaluted to True many times per simulation, *adding the condition about the ProgressMonitorValue variable makes sure that* the set of conditions as a whole in each IF/ELIF statement are evaluated to True only once per simulation. Also, the energy ranges in all of the IF/ELIF statements must not overlap lest multiple IF/ELIF statements evaluate to True and cause ProgressMonitorValue to alternate repeatedly between values, which in turn would cause the command terminal to be flooded by the printed statements. The energy ranges in the IF/ELIF statements were chosen to not let the user wait too long before seeing the next message updating them on the present maximum kinetic energy of the alpha particles remaining in the beam.
        #     if (0.6 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.8 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 1):
        #         print("Showing the progress of Simulation Instance {} ...".format(instance + 1)) # This message is for telling the user which simulation instance is being run and it must be shown only once.
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 1 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.4 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.6 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 2):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 2 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.2 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.4 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 3):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 3 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.15 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.2 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 4):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 4 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.1 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.15 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 5):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 5 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.05 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.1 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 6):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 6 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.04 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.05 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 7):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 7 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.03 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.04 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 8):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 8 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.02 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.03 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 9):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 9 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (0.01 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.02 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 10):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 10 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (1e-3 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 0.01 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 11):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 11 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (1e-4 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 1e-3 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 12):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 12 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (1e-5 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 1e-4 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 13):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 13 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (1e-6 * self.InitialKineticEnergy < self.MaximumAlphaEnergy_now < 1e-5 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 14):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 14 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
            
        #     elif (self.MinimumAlphaEnergy_eV * 1e-6 < self.MaximumAlphaEnergy_now < 1e-6 * self.InitialKineticEnergy) and (self.ProgressMonitorValue != 15):
        #         print(self.show_MaximumAlphaEnergy) # This line of code is repeated. Thus, a variable was defined to decrease the amount of code that was repeated.
        #         self.ProgressMonitorValue = 15 # Setting ProgressMonitorValue to this value, in combination with the *monotonic* decrease of the number of alpha particles remaining in the beam, make sure that this IF statement does not evaluate to True again in the simulation.
        # except AttributeError: # AttributeError is the error I saw in the command terminal when I specified an initial alpha particle kinetic energy less than the minimum energy required for a particle to stay in the beam.
        #     print("Error: You must specify an initial alpha particle kinetic energy greater than {} eV. The program will now exit.".format(self.MinimumAlphaEnergy_eV))
        #     exit() # This is what I want to happen in this case.
        # except:
        #     print("Unknown Error: The program will now exit. Please restart the program and try again.") # An error besides AttributeError may be raised for some reason. I want the program to catch the error rather than crash.
        #     exit() # This is what I want to happen in this case.


        # REFERENCES:
            # Zelle, J. M. (2017). Python Programming: An Introduction to Computer Science (B. Jones Ed. 3rd ed.). 2154 NE Broadway, Suite 100, Portland, Oregon 97232: Franklin, Beedle & Associates Inc.
            # grassworm, & Cees Timmerman. (2020, 16 May 2020). Display a decimal in scientific notation. Retrieved from https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
            # Fayek, H. (2020). Week 3 Control Flow. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Programiz. Python Exception Handling Using try, except and finally statement. Retrieved from https://www.programiz.com/python-programming/exception-handling


    def process_Simulation(self, instance): # Pass the "instance" argument to the show_Progress() method.
        self.make_Medium()
        self.initialise_Simulation(instance) # Prepare the arrays, lists and other variables that are to be used in the simulation using what was defined in the class's __init__() method.
            
        ### Process the data. This WHILE loop is the simulation.
        while self.ParticleNumber > 0: # Use the ParticleNumber variable directly instead of using a method to retrieve it. I prefer this style.
            # We need something to take the alpha particles through each simulation step.
            self.update_AlphaParticlePosition() # Move each particle some distance until its location of collision with an electron.
            self.record_AlphaParticlePosition() # Record the new x-position of each alpha particle.
            self.update_AlphaParticleMomentum() # Simulate the collision of each alpha particle with an electron. Recalculate each alpha particle's momentum vector and position along the x-axis after the alpha particles collide with atomic electrons.
            self.update_ParticleNum() # *Manage* how many alpha particles remain in the beam. Alpha particles leave the beam when they lose too much energy due to colliding with too many atomic electrons. When their energy is extremely low, they capture atomic electrons and become helium atoms, thus leaving the beam. This method does the removing.
            
            self.show_Progress(instance) # Show the user the progress of the simulation so that they may know whether the program is running or frozen. When the WHILE loop in main() is running, the would not see any update about whether the program is running or frozen if the show_Progress() method did not exist.
        
        # REFERENCES:
            # Fayek, H. (2020). Week 6 Object-Oriented Programming. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            
        
    def get_Results(self):
        if __name__ == "__main__":
            timing_studies.start_GetResults = time.time()
        
            self.ParticleNumDict_Distance = dict(zip(self.DistancesToCheck, self.ParticleNumList_Distance)) # Associate the distances with the number of particles in the beam considering that the distances are randomly generated.
        
            timing_studies.end_GetResults = time.time()
            timing_studies.get_Results_List.append(timing_studies.end_GetResults - timing_studies.start_GetResults)

        return self.MaximumRange, self.ParticleNumDict_Distance, self.MeanRange
        
if __name__ == "__main__":
    timing_studies.end_ClassDefinition_AlphaParticles = time.time()
    timing_studies.append_TimingResults("AlphaParticles class definition", timing_studies.end_ClassDefinition_AlphaParticles - timing_studies.start_ClassDefinition_AlphaParticles, "Once")

    timing_studies.start_ClassDefinition_StatisticalAnalysis = time.time()


class StatisticalAnalysis(AlphaParticles): # This class is for running a simulation multiple times as multiple instances and calculating the average of the results of all of the simulation instances.
    def __init__(self, InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity, SimInstances):
        super().__init__(InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity)

        # REFERENCES:
            # Fayek, H (2020). Week 6 Object-Oriented Programming, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
    
       
    def process_SimulationInstance(self, instance): # This method was added for use in multiprocessing Pool and is parallelised. The last argument is for the pool.map() function.
        # Run each simulation instance.
        self.alpha_beam_dict[instance].process_Simulation(instance) # Run the simulation instances and have the results of each instance ready for collection.
        
        ### Output the results.
        print("Analysing the data from Simulation Instance {} ...".format(instance + 1)) # Tell the user what is happening. This process can take some time because of the large amount of data that must be processed, especially for producing a plot of the number of alpha particles in the beam as a function of penetration distance into the medium.
        self.alpha_beam_dict[instance].calculate_Data() # Calculate the results.

        return self.alpha_beam_dict[instance] # It is actually necessary that the multiprocessing pool return something.

        # REFERENCES:
            # PhysicistAbroad (2017). Multiprocessing in Python returns None unexpectedly, https://stackoverflow.com/questions/44052594/multiprocessing-in-python-returns-none-unexpectedly.
        
                
    def get_DataFromSimulationInstances(self): # Gather the results of each simulation instance.
        if __name__ == "__main__":
            ### Output the results.
            for instance in range(0, self.SimInstances):
                self.MaximumRanges_Dict[instance], self.ParticleNumDict_Distance_Dict[instance], self.MeanRanges_Dict[instance] = self.alpha_beam_dict[instance].get_Results() # Collect the results of the simulation instance.


    def calculate_and_get_Average(self, Dictionary):
        if __name__ == "__main__":
            timing_studies.start_StatAnalysis_CalculateAngGetAverage = time.time()
        
        self.Average = stat.mean(Dictionary[instance] for instance in range(0, len(Dictionary)))
        
        if __name__ == "__main__":
            timing_studies.end_StatAnalysis_CalculateAngGetAverage = time.time()
            timing_studies.StatAnalysis_calculate_and_get_Average_List.append(timing_studies.end_StatAnalysis_CalculateAngGetAverage - timing_studies.start_StatAnalysis_CalculateAngGetAverage)

        return self.Average

        # REFERENCES:
            # Python Software Foundation (2020). statistics — Mathematical statistics functions, https://docs.python.org/3/library/statistics.html.
    
    
    def calculate_and_get_PopulationStandardDeviation(self, Dictionary):
        if __name__ == "__main__":
            timing_studies.start_StatAnalysis_CalculateAndGetPSD = time.time()
        
        self.PopulationStandardDeviation = stat.pstdev(Dictionary[instance] for instance in range(0, len(Dictionary)))
        
        if __name__ == "__main__":
            timing_studies.end_StatAnalysis_CalculateAndGetPSD = time.time()
            timing_studies.StatAnalysis_calculate_and_get_PopulationStandardDeviation_List.append(timing_studies.end_StatAnalysis_CalculateAndGetPSD - timing_studies.start_StatAnalysis_CalculateAndGetPSD)
        
        return self.PopulationStandardDeviation

        # REFERENCES:
            # GeeksforGeeks stdev() method in Python statistics module, https://www.geeksforgeeks.org/python-statistics-stdev/.
    
    
    def plot_ParticleNum(self, SimInstances, alpha_beam_dict): # Plot the number of alpha particles in the beam as a function of simulation step.
        if __name__ == "__main__":
            timing_studies.start_StatAnalysis_plot_ParticleNum = time.time()
        
            plt.figure(figsize = (17, 7)) # We want the data to be shown clearly, so we make the figure wide and sufficiently big.
        
            for instance in range(0, SimInstances): # Plot all of the plots in the same figure.
                plt.scatter(np.array(alpha_beam_dict[instance].DistancesToCheck), np.array(alpha_beam_dict[instance].ParticleNumList_Distance), marker = ".", alpha = 0.5) # Using an "alpha" less than 1 means that we can see the plot from each instance of the simulation. While using numpy arrays does not make any significant improvement in how much time is spent making the plots compared to when using lists, using numpy arrays here are for consistency with other plt.scatter() calls.
        
            plt.xlabel("Distance /m") # The units of distance are m.
            plt.ylabel("Number of alpha particles in the beam") # We are plotting the number of alpha particles remaining in the beam as a function of distance.
            plt.savefig(DirectoryToSaveTo + "AlphaRange_" + timestamp + ".png") # Save the plot externally from AlphaParticles2.py so that the user can refer to it later. Give it a unique name that will cause the file to probably never be overwritten by the program unless another run of the simulation ends in the same second as the previous run.

            timing_studies.end_StatAnalysis_plot_ParticleNum = time.time()
            timing_studies.append_TimingResults("StatisticalAnalysis plot_ParticleNum()", timing_studies.end_StatAnalysis_plot_ParticleNum - timing_studies.start_StatAnalysis_plot_ParticleNum, "Once")

        # REFERENCES:
            # Hunter, J, Dale, D, Firing, E, Droettboom, M & The Matplotlib development team matplotlib.pyplot.figure, https://matplotlib.org/3.3.1/api/_as_gen/matplotlib.pyplot.figure.html.
            # Hunter, J., Dale, D., Firing, E., Droettboom, M., & The Matplotlib development team. matplotlib.markers. Retrieved from https://matplotlib.org/3.1.1/api/markers_api.html#module-matplotlib.markers
            # Welch, A. J. How to Save a Plot to a File Using Matplotlib. Retrieved from https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
            # Hunter, J., Dale, D., Firing, E., Droettboom, M., & The Matplotlib development team. matplotlib.pyplot.savefig. Retrieved from https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html
            # Knoll, G. F. (2010). Radiation Detection and Measurement (4th ed.). 111 River Street, Hoboken, NJ 07030-5774: John Wiley & Sons, Inc.
            # Hofmann, F. Creating and Deleting Directories with Python. Retrieved from https://stackabuse.com/creating-and-deleting-directories-with-python/

    
    def plot_RandomMatrixOffDiagonal(self, DataList, OffDiagonalElement, x_axis_ScaleFactor, hist_NumberOfBins): # The code in this method is repeated for each off-diagonal element of the randomised 3x3 matrix (RandomMatrix).
        if __name__ == "__main__":
            self.RandomNumList_C_All_np_rescaled = np.array(DataList) * x_axis_ScaleFactor # Apply the x-axis scale factor to the random numbers to make the x-axis label of the plot be more readable.
            plt.figure() # Initialise a new matplotlib.pyplot (plt) figure so that the histogram defined in the next line does not get added to any plt figure already in the computer's memory.
            plt.hist(self.RandomNumList_C_All_np_rescaled, bins = hist_NumberOfBins) # This histogram is now in the computer's memory.
            plt.xlim(0.0, max(self.RandomNumList_C_All_np_rescaled)) # This line of code solved the situation where the x-axis ranged from 0 to a few thousand. A scale factor of 1e5 would not scale the values of the off-diagonal elements that high because the sum of the off-diagonal values in each column of the randomised 3x3 matrix is 1 - C_xx.
            plt.xlabel("{} /{:.0e}".format(OffDiagonalElement, x_axis_ScaleFactor ** -1)) # Tell the user what the values they are seeing on the x-axis mean.
            plt.ylabel(self.plt_ylabel)
    
    
    def plot_RandomMatrixOffDiagonals_All(self, SimInstances, alpha_beam_dict): # The user would benefit from seeing what the values of the off-diagonal elements of the randomised 3x3 matrix (RandomMatrix) were because these values directly influence the results.
        if __name__ == "__main__":
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals = time.time()
        
            ### Concatenate all of the lists into one set of lists.
            # Initialise a set of lists.
            self.RandomNumList_C_xy_All = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
            self.RandomNumList_C_xz_All = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
            self.RandomNumList_C_yx_All = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
            self.RandomNumList_C_yz_All = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
            self.RandomNumList_C_zx_All = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
            self.RandomNumList_C_zy_All = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.

            # Concatenate ...
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Concatenation = time.time()
        
            for instance in range(0, SimInstances):
                self.RandomNumList_C_xy_All = self.RandomNumList_C_xy_All + alpha_beam_dict[instance].RandomNumList_C_xy # List concatenation.
                self.RandomNumList_C_xz_All = self.RandomNumList_C_xz_All + alpha_beam_dict[instance].RandomNumList_C_xz # List concatenation.
                self.RandomNumList_C_yx_All = self.RandomNumList_C_yx_All + alpha_beam_dict[instance].RandomNumList_C_yx # List concatenation.
                self.RandomNumList_C_yz_All = self.RandomNumList_C_yz_All + alpha_beam_dict[instance].RandomNumList_C_yz # List concatenation.
                self.RandomNumList_C_zx_All = self.RandomNumList_C_zx_All + alpha_beam_dict[instance].RandomNumList_C_zx # List concatenation.
                self.RandomNumList_C_zy_All = self.RandomNumList_C_zy_All + alpha_beam_dict[instance].RandomNumList_C_zy # List concatenation.
        
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Concatenation = time.time()
            timing_studies.append_TimingResults_ParticularLines("StatisticalAnalysis plot_RandomMatrixOffDiagonals() ConcatenationForRandomNumHistograms (once)", timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Concatenation - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Concatenation)

            ### Define some parameters and other things that are going to be used for all of the plots defined in this function.
            self.hist_NumberOfBins_Default = 500 # Define a default number of bins for the histograms that are going to be plotted so that the number of bins in the histograms is always defined. The user may have invested considerable time and computer resources for running the simulation. They must get its results.
        
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Input = time.time() # ... for subtracting the time spent waiting for a user input.
            try:
                self.hist_NumberOfBins = int(self.check_FloatingPointInput(float(input("\tHow many bins should the histograms of the off-diagonal elements of the randomised 3x3 matrix have? Please specify an integer greater than 0. (Default: {}) ".format(self.hist_NumberOfBins_Default))))) # The frequencies of the values can become quite large when the initial kinetic energy of the alpha particles is high and/or the initial number of particles in the beam is high. This message is indented to show the user it is part of the process of saving the data. The previous message during runtime would have been a message saying that the data is being saved.
                
                if self.hist_NumberOfBins <= 0:
                    print("Error: A histogram cannot have 0 or a negative number of bins. Please specify a positive number.") # The user must get the data of the simulation.
                    self.hist_NumberOfBins = self.hist_NumberOfBins_Default

                print("\t...") # Show the user that the program is still running.
            
            except:
                print("Error: You did not input a valid value for the number of bins in the histograms. The default number of bins will be used, i.e., {} bins.".format(self.hist_NumberOfBins_Default))
                self.hist_NumberOfBins = self.hist_NumberOfBins_Default # The user may have invested considerable time and computer resources for running the simulation. They must get its results. Exiting the program would not be suitable.

            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Input = time.time()
        
            self.x_axis_ScaleFactor = 1e5 # The values of the off-diagonal elements are so small that too many leading 0s appear in the x-axis values of the plots. This scale factor is specified in the x-axis label so that the user knows what values they are seeing mean.
            self.plt_ylabel = "Frequency" # This line of code ties the y-axis label of all of the histograms defined below together so that any changes in the name defined in this line affect the y-axis labels of the histograms all at once.

            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot = time.time()

        
            ## Plot the distribution of C_xy values.
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xy = time.time()
            self.plot_RandomMatrixOffDiagonal(self.RandomNumList_C_xy_All, "C_xy", self.x_axis_ScaleFactor, self.hist_NumberOfBins)
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xy = time.time()

            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xy = time.time()
            plt.savefig(DirectoryToSaveTo + "C_xy_Histogram_" + timestamp + ".png") # The data files outputted from each simulation is put into their own folder. If the user ran multiple simulations and the files were outputted into the directory in which the program file is, that directory would get flooded quite quickly.
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xy = time.time()

            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xy - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xy)
            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xy - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xy)

        
            ## Plot the distribution of C_xz values.
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xz = time.time()
            self.plot_RandomMatrixOffDiagonal(self.RandomNumList_C_xz_All, "C_xz", self.x_axis_ScaleFactor, self.hist_NumberOfBins)
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xz = time.time()

            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xz = time.time()
            plt.savefig(DirectoryToSaveTo + "C_xz_Histogram_" + timestamp + ".png") # The data files outputted from each simulation is put into their own folder. If the user ran multiple simulations and the files were outputted into the directory in which the program file is, that directory would get flooded quite quickly.
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xz = time.time()

            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xz - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_xz)
            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xz - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_xz)


            ## Plot the distribution of C_yx values.
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yx = time.time()
            self.plot_RandomMatrixOffDiagonal(self.RandomNumList_C_yx_All, "C_yx", self.x_axis_ScaleFactor, self.hist_NumberOfBins)
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yx = time.time()

            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yx = time.time()
            plt.savefig(DirectoryToSaveTo + "C_yx_Histogram_" + timestamp + ".png") # The data files outputted from each simulation is put into their own folder. If the user ran multiple simulations and the files were outputted into the directory in which the program file is, that directory would get flooded quite quickly.
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yx = time.time()

            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yx - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yx)
            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yx - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yx)

            ## Plot the distribution of C_yz values.
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yz = time.time()
            self.plot_RandomMatrixOffDiagonal(self.RandomNumList_C_yz_All, "C_yz", self.x_axis_ScaleFactor, self.hist_NumberOfBins)
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yz = time.time()

            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yz = time.time()
            plt.savefig(DirectoryToSaveTo + "C_yz_Histogram_" + timestamp + ".png") # The data files outputted from each simulation is put into their own folder. If the user ran multiple simulations and the files were outputted into the directory in which the program file is, that directory would get flooded quite quickly.
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yz = time.time()

            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yz - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_yz)
            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yz - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_yz)


            ## Plot the distribution of C_zx values.
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zx = time.time()
            self.plot_RandomMatrixOffDiagonal(self.RandomNumList_C_zx_All, "C_zx", self.x_axis_ScaleFactor, self.hist_NumberOfBins)
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zx = time.time()

            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zx = time.time()
            plt.savefig(DirectoryToSaveTo + "C_zx_Histogram_" + timestamp + ".png") # The data files outputted from each simulation is put into their own folder. If the user ran multiple simulations and the files were outputted into the directory in which the program file is, that directory would get flooded quite quickly.
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zx = time.time()

            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zx - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zx)
            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zx - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zx)


            ## Plot the distribution of C_zy values.
            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zy = time.time()
            self.plot_RandomMatrixOffDiagonal(self.RandomNumList_C_zy_All, "C_zy", self.x_axis_ScaleFactor, self.hist_NumberOfBins)
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zy = time.time()

            timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zy = time.time()
            plt.savefig(DirectoryToSaveTo + "C_zy_Histogram_" + timestamp + ".png") # The data files outputted from each simulation is put into their own folder. If the user ran multiple simulations and the files were outputted into the directory in which the program file is, that directory would get flooded quite quickly.
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zy = time.time()

            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zy - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_C_zy)
            timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List.append(timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zy - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_C_zy)


            ## Record timing data for the code above.
            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot = time.time()
            timing_studies.append_TimingResults_ParticularLines("StatisticalAnalysis plot_RandomMatrixOffDiagonals_All() PlotAndExportRandomNumHistograms (sum)", timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot)

            timing_studies.append_TimingResults_ParticularLines("StatisticalAnalysis plot_RandomMatrixOffDiagonals_All() PlotRandomNumHistograms (average)", np.array(timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List).mean())
            timing_studies.append_TimingResults_ParticularLines("StatisticalAnalysis plot_RandomMatrixOffDiagonals_All() ExportRandomNumHistograms (average)", np.array(timing_studies.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List).mean())

            timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals = time.time()
            timing_studies.append_TimingResults("StatisticalAnalysis plot_RandomMatrixOffDiagonals_All()", (timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals) - (timing_studies.end_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Input - timing_studies.start_StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Input), "Once")

        # REFERENCES:
            # grassworm, & Cees Timmerman. (2020, 16 May 2020). Display a decimal in scientific notation. Retrieved from https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
            # Devert, A. (2014). Setting an axis range. Retrieved from https://subscription.packtpub.com/book/big_data_and_business_intelligence/9781849513265/4/ch04lvl1sec53/setting-an-axis-range
            # Hunter, J., Dale, D., Firing, E., Droettboom, M., & The Matplotlib development team. (14 August 2020). matplotlib.pyplot.figure. Retrieved from https://matplotlib.org/3.3.1/api/_as_gen/matplotlib.pyplot.figure.html
            # Hunter, J., Dale, D., Firing, E., Droettboom, M., & The Matplotlib development team. (14 August 2020). matplotlib.pyplot.hist. Retrieved from https://matplotlib.org/3.3.1/api/_as_gen/matplotlib.pyplot.hist.html
            # Hofmann, F. Creating and Deleting Directories with Python. Retrieved from https://stackabuse.com/creating-and-deleting-directories-with-python/


    def save_Data(self, Seed, MeanRange_Average, MeanRange_Uncertainty, MaximumRange_Average, MaximumRange_Uncertainty, SimInstances, SimDistance_Option): # Let the user have a separate data file for each simulation they run. They do not have to rename the files before running another simulation after at least one second of the previous simulation finishing because the files will not be overwritten.
        if __name__ == "__main__":
            timing_studies.start_StatAnalysis_save_Data = time.time()
        
            if self.RandomDistribution == "basic":
                self.RandomDistribution_description = "Python 3's basic distribution, where random numbers between 0 and 1 were randomly generated, and where 0 but not 1 were included in the set of numbers that could have been generated"
            
            elif self.RandomDistribution == "discrete": # Let the user know as much detail about the simulation they ran as they need to for documenting their research.
                self.RandomDistribution_description = "discrete, with {0:.0e} random numbers between and including 0 and 1 that could have been generated with equal probability".format(self.AmountOfNumbers + 1) # AmountOfNumbers is actually the end value of the random.randint() function. Therefore, AmountOfNumbers + 1 numbers can be randomly generated because the start value is included in the set of values that can be generated.

                # REFERENCE: grassworm, & Cees Timmerman. (2020, 16 May 2020). Display a decimal in scientific notation. Retrieved from https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
            
            elif self.RandomDistribution == "triangular":
                self.RandomDistribution_description = "triangular, where random numbers between and including 0 and 1 were generated and where 0 was the mode. The probability for generating larger random numbers decreased linearly as a function of the number that could have been generated. 1 had a zero probability of being generated" # Let the user know as much detail about the simulation they ran as they need to for documenting their research.
            
            elif self.RandomDistribution == "uniform":
                self.RandomDistribution_description = "uniform, where random numbers between and including 0 and 1 were generated with equal probability" # Let the user know as much detail about the simulation they ran as they need to for documenting their research.
        
            # REFERENCE: Python Software Foundation. (2020, 11 September 2020). random — Generate pseudo-random numbers. Retrieved from https://docs.python.org/3/library/random.html
        
            # Describe which simulation mode the user chose.
            if SimDistance_Option in set(["a", "A"]):
                self.SimDistance_Option_Description = "Analysis of an alpha particle beam"
            
            elif SimDistance_Option in set(["g", "G"]):
                self.SimDistance_Option_Description = "Radiotherapy game"
            
            elif SimDistance_Option in set(["q", "Q"]):
                self.SimDistance_Option_Description = "Attenuation quiz"
        
            # Make the data file.
            self.DataFile = open(DirectoryToSaveTo + "data_" + timestamp + ".txt", "w") # Give the outputted file a useful name to make it easier for the user to document their work/research. The file will probably be overwritten if the user starts more than one simulation in the same second. However, this will be very rare, if not impossible, because it takes some time for the user to input values and more time for the simulation to run.
            
            self.DataFileContents_Intro = "Program: AlphaParticles2.py\nAuthor: Kyrollos Iskandar\n\nTimestamp (YYYY-MM-DD_hh-mm-ss): {}\n\n".format(timestamp)
            self.DataFileContents_Mode = "Simulation mode: {}\n\n".format(self.SimDistance_Option_Description)
            self.DataFileContents_AlphaBeamInputs = "### Inputs about the alpha particles ###\nInitial kinetic energy = {} MeV\nInitial number of alpha particles = {}\nProbability density function used for random number generation: {}\nSeed for the random number generators = {}\n\n".format(self.InitialKineticEnergy, self.InitialParticleNumber, self.RandomDistribution_description, Seed)
            self.DataFileContents_MediumInputs = "### Inputs about the medium ###\nAtomic number = {}\nAtomic weight = {} g/mol\nMass density = {} g/cm^3\n\n".format(self.AtomicNumber, self.AtomicWeight, self.MassDensity)
            self.DataFileContents_SimulationInputs = "### Inputs about the simulation ###\nNumber of simulation instances: {}\n\n".format(SimInstances)
            self.DataFileContents_Results = "### Results ###\nMean range = {} +/- {} m (Average +/- 3 * Population standard deviation){}\nMaximum range = {} +/- {} m (Average +/- 3 * Population standard deviation){}\n\n".format(MeanRange_Average, MeanRange_Uncertainty, self.MeanRange_Description, MaximumRange_Average, MaximumRange_Uncertainty, self.MaximumRange_Description)
            self.DataFileContents_AdditionalInfo = "### Information about the randomised 3x3 matrix that was used to generate the data ###\n# Diagonal elements:\nC_xx = {}\nC_yy = {}\nC_zz = {}\n\n# The values of the off-diagonal elements of the randomised 3x3 matrix are shown in the accompanying histograms.\n\n### End of the data file ###".format(self.C_xx, self.C_yy, self.C_zz)

            self.DataFileContents = self.DataFileContents_Intro + self.DataFileContents_Mode + self.DataFileContents_AlphaBeamInputs + self.DataFileContents_MediumInputs + self.DataFileContents_SimulationInputs + self.DataFileContents_Results + self.DataFileContents_AdditionalInfo # Breaking up the contents of the data file as shown immediately above makes changing the file's contents easier.
            
            self.DataFile.write(self.DataFileContents) # It seems that the write() method cannot accept more than one argument, unlike the print() function. However, the technique used here works, though it may be difficult to use when there are a lot of {}s.
            
            self.DataFile.close() # We must close an opened file when we are finished working with it.
        
            timing_studies.end_StatAnalysis_save_Data = time.time()
            timing_studies.append_TimingResults("StatisticalAnalysis save_Data()", timing_studies.end_StatAnalysis_save_Data - timing_studies.start_StatAnalysis_save_Data, "Once")

        # REFERENCES:
            # Fayek, H. (2020). Week 4 I/O. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Python Software Foundation. (2020, 9 September 2020). 7. Input and Output. Retrieved from https://docs.python.org/3/tutorial/inputoutput.html
            # Hofmann, F. Creating and Deleting Directories with Python. Retrieved from https://stackabuse.com/creating-and-deleting-directories-with-python/
            # Mehdi Nellen, Acorn, & gavstar. (2014, 23 January 2014). Telling Python to save a .txt file to a certain directory on Windows and Mac. Retrieved from https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
            # Programiz. Python Exception Handling Using try, except and finally statement. Retrieved from https://www.programiz.com/python-programming/exception-handling

    # REFERENCES:
        # Community & kennytm (2017). How can I assign the value of a variable using eval in python?, https://stackoverflow.com/questions/5599283/how-can-i-assign-the-value-of-a-variable-using-eval-in-python.
        # Programiz Python exec(), https://www.programiz.com/python-programming/methods/built-in/exec.
if __name__ == "__main__":
    timing_studies.end_ClassDefinition_StatisticalAnalysis = time.time()
    timing_studies.append_TimingResults("StatisticalAnalysis class definition", timing_studies.end_ClassDefinition_StatisticalAnalysis - timing_studies.start_ClassDefinition_StatisticalAnalysis, "Once")

    timing_studies.start_ClassDefinition_AlphaRTGame = time.time()


class AlphaRTGame(AlphaParticles): # This class is for making a game related to radiotherapy (RT) in which an alpha particle beam is used to deliver a particular dose to human tissue. The dose we are interested in is equivalent dose, which, for alpha particles, is defined as 20 times the absorbed dose. The absorbed dose is simply the amount of energy absorbed by the medium per unit mass of the medium. The factor of 20 is the radiation weighting factor that means that, compared to photons, alpha particles do 20 times the damage to biological tissue. This class is a child class of AlphaParticles because an alpha particle beam is simulated in the game.
    # REFERENCES:
        # International Commission on Radiological Protection (2007). The 2007 Recommendations of the International Commission on Radiological Protection. Orlando, Amsterdam, Tokyo, Singapore: Elsevier Ltd.
    
    def __init__(self, InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity): # The arguments of the __init__() method, except the "self" argument, are what the user inputs when the program is run.
        super().__init__(InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity)
        # self.AlphaParticleMomentumMagnitudes = np.array([]) # Initialise a numpy array for keeping track of the momentum magnitude of each alpha particle per collision with an electron.
        
        self.InitialiseAlphaParticleMomentumMagnitudes = 0 # ... for making a particular IF statement execute only once even though it is in the record_AlphaParticleMomentumMagnitude method, which is in a loop.
        
        self.CorrectMaterialThickness_Backwards = None # ... for error handling.
        self.CorrectMaterialThickness_Forwards = None # ... for error handling.
    
    
    def record_AlphaParticleMomentumMagnitude(self):
        if __name__ == "__main__":
            timing_studies.start_AlphaRTGame_record_AlphaParticleMomentumMagnitude = time.time()
        
        if self.InitialiseAlphaParticleMomentumMagnitudes != 1:
            self.AlphaParticleMomentumMagnitudes = np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 5]]).T # Initialise the AlphaParticleMomentumMagnitudes array, giving it the shape it needed for later concatenation operations.
            self.InitialiseAlphaParticleMomentumMagnitudes = 1 # The AlphaParticleMomentumMagnitudes array has been initialised.
        # NOTE: Before optimisation ... NOTE: The pre-optimised code below was in the __init__() method.
        # self.AlphaParticleMomentumMagnitudes_DF = pd.DataFrame() # Initialise an empty pandas DataFrame for keeping track of the momentum magnitude of each alpha particle per collision with an electron.
        
        
        # At this point, we have the AlphaParticlesInfoList_ID_X_Momentum array, which specifies the momentum of each alpha particle. Now we concatenate the new momentum magnitudes.
        if np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 5]]).T.shape[0] == self.AlphaParticleMomentumMagnitudes.shape[0]:
            self.AlphaParticleMomentumMagnitudes = np.concatenate((self.AlphaParticleMomentumMagnitudes, np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 5]]).T), axis = 1) # Record the momentum magnitude of each alpha particle for later being used to calculate how much kinetic energy was transferred to the electrons from the alpha particles.
        
        else:
            self.AlphaParticleMomentumMagnitudesOfPresentSimStep = np.concatenate((np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 5]]).T, np.zeros((self.AlphaParticleMomentumMagnitudes.shape[0] - np.array([self.AlphaParticlesInfoList_ID_X_Momentum[:, 5]]).T.shape[0], 1))), axis = 0) # Unlike pandas, numpy does not concatenate arrays that have an unequal number of rows. So we must make the array that is to be added have the same number of rows as the array to which it is to be added. Using 0s for this is suitable for the data analysis that is to be done after the simulation.
            self.AlphaParticleMomentumMagnitudes = np.concatenate((self.AlphaParticleMomentumMagnitudes, self.AlphaParticleMomentumMagnitudesOfPresentSimStep), axis = 1)
        # NOTE: Before optimisation ...
        # self.AlphaParticleMomentumMagnitudes_DF = pd.concat([self.AlphaParticleMomentumMagnitudes_DF, self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[:, 5]], axis = 1) # Record the momentum magnitude of each alpha particle for later being used to calculate how much kinetic energy was transferred to the electrons from the alpha particles. MomentumMagnitudeList_DF is calculated in the update_AlphaParticlePosition() method.

        
        if __name__ == "__main__":    
            timing_studies.end_AlphaRTGame_record_AlphaParticleMomentumMagnitude = time.time()
            timing_studies.record_AlphaParticleMomentumMagnitude_List.append(timing_studies.end_AlphaRTGame_record_AlphaParticleMomentumMagnitude - timing_studies.start_AlphaRTGame_record_AlphaParticleMomentumMagnitude)

        # REFERENCES:
            # The SciPy community (2020). numpy.concatenate, https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html.
    
    
    def calculate_MaximumRange(self): # At the end of the simulation, we have a large DataFrame that has information about the x-position of each alpha particle in each simulation step. We want to make a histogram of the number of particles in the beam as a function of distance out of this DataFrame.
        if __name__ == "__main__":
            timing_studies.start_AlphaRTGame_calculate_MaximumRange = time.time()
        
        print("Analysing the data ...")

        ## Calculate the maximum range of the alpha particles. NOTE: The x-positions are in the same units as the mean free path, which has units of m.
        self.MaximumRange = self.PositionXArray.max().max() # The maximum range is the largest number in the DataFrame. It is the furthest distance an alpha particle in the beam has travelled. It is the easiest value to calculate out of the ones we are interested in. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method.
        # NOTE: Before optimisation ...
        # self.PositionXList_DF = ((self.PositionXList_DF.T).reset_index(drop = True)).T # First, we make sure its columns are labelled by the simulation steps rather than all having the same label due to having been concatenated together. The reset_index() method works row-wise, so we transpose the DataFrame first. Then we reset the row labels and transpose the DataFrame back to its original shape. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method. However, we use parentheses to make reading the code easier.
        # self.MaximumRange = self.PositionXList_DF.max().max() # The maximum range is the largest number in the DataFrame. It is the furthest distance an alpha particle in the beam has travelled. It is the easiest value to calculate out of the ones we are interested in. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method.

        if __name__ == "__main__":
            timing_studies.end_AlphaRTGame_calculate_MaximumRange = time.time()
        
        # REFERENCES:
            # Fayek, H (2020). Week 9 Scientific Python, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # the pandas development team (2014). pandas.DataFrame.reset_index, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html.
            # the pandas development team (2014). pandas.DataFrame.max, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.max.html.
            # Fayek, H (2020). Week 2 Data Types, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Krane, K S (2014). Introductory Nuclear Physics, Reprint ed. Durga Printo Graphics, Delhi: John Wiley & Sons, Inc.

    
    def calculate_MomentumTransferArraySum1(self, step): # This method is for the multiprocessing section of code in the calculate_DoseToMedium() method below.
        return (np.array([self.AlphaParticleMomentumMagnitudes[:, step]]).T - np.array([self.AlphaParticleMomentumMagnitudes[:, step + 1]]).T).sum()
        
    
    def calculate_DoseToMedium(self, BeamHeight, BeamWidth): # In the game, the kinetic energy that the alpha particles transfer to the electrons in the medium must be calculated. However, this kinetic energy is equal to the total kinetic energy that the alpha particles lose due to conservation of energy. We are assuming that all of the energy that the alpha particles lose is deposited into the medium.
        if __name__ == "__main__":
            timing_studies.start_AlphaRTGame_calculate_DoseToMedium = time.time()
        
            timing_studies.start_AlphaRTGame_calculate_DoseToMedium_MaximumRange = time.time()

        # At this point, we have a large AlphaParticleMomentumMagnitudes_DF DataFrame with some NaNs due to alpha particles leaving the beam.
        # NOTE: Before multiprocessing ...
        # self.MomentumTransfer_Array = np.zeros(shape = (self.InitialParticleNumber, 1)) # The array must have the same dimensions as the array that is to be concatenated to it before the concatenation happens. 0s will not affect the upcoming summation over the entire array.
        # NOTE: Before optimisation ...
        # self.AlphaParticleMomentumMagnitudes_DF = self.AlphaParticleMomentumMagnitudes_DF.fillna(value = 0.0).T.reset_index(drop = True).T # Replacing the NaNs with 0.0 means that the calculation of the momentum transfer from the alpha particle to the electrons will be done even when dealing with particles that leave the beam in the next simulation step. Reseting the indices of the columns means that the columns can be indexed correctly. Having all of these methods in one line means that only one object, rather than two objects, get stored in memory.
        # self.MomentumTransfer_DF = pd.DataFrame()

        if __name__ == "__main__":
            timing_studies.end_AlphaRTGame_calculate_DoseToMedium_MaximumRange = time.time()
            timing_studies.append_TimingResults_ParticularLines("AlphaRTGame calculate_DoseToMedium() MaximumRange calculation", timing_studies.end_AlphaRTGame_calculate_DoseToMedium_MaximumRange - timing_studies.start_AlphaRTGame_calculate_DoseToMedium_MaximumRange)


            timing_studies.start_AlphaRTGame_calculate_DoseToMedium_MomentumTransferArray = time.time()
        # Now we have a DataFrame ready for analysis. We want to extract the total kinetic energy transferred to the electrons in the medium. This value is a scalar.
        ################################### Do the MomentumTransfer_Array calculation using multiprocessing ###################################
        if __name__ == "__main__":
            pool_MomentumTransferArray = mp.Pool(processes = int(MaxCPUCoresToUse)) # Make sure that MaxCPUCoresToUse is an integer.

            self.MomentumTransfer_Array = np.array(pool_MomentumTransferArray.map(self.calculate_MomentumTransferArraySum1, list(range(0, self.AlphaParticleMomentumMagnitudes.shape[1] - 1))))

            pool_MomentumTransferArray.close()
            pool_MomentumTransferArray.join()
        
        # REFERENCES:
            # Python Software Foundation (2020). multiprocessing — Process-based parallelism, https://docs.python.org/3/library/multiprocessing.html.
            # 0612 TV w/ NERDfirst (2018). Python's Multiprocess Pool - Friday Minis 267, https://www.youtube.com/watch?v=WdorgAKWbns.
            # When Maths meets coding (2020). Multiprocessing in python complete tutorial, https://www.youtube.com/watch?v=rZ5CSsgv5hs.
        
        #######################################################################################################################################
        # NOTE: Before multiprocessing ... The multiprocessing code above replaced this code. However, a few methods were taken out of the process_Simulation() method while implementing multiprocessing.
        # for step in range(0, self.AlphaParticleMomentumMagnitudes.shape[1] - 1):
        #     self.MomentumTransfer_Array = np.concatenate((self.MomentumTransfer_Array, np.array([self.AlphaParticleMomentumMagnitudes[:, step]]).T - np.array([self.AlphaParticleMomentumMagnitudes[:, step + 1]]).T), axis = 1)
        # NOTE: Before optimisation ...
        # for step in range(0, self.AlphaParticleMomentumMagnitudes_DF.shape[1] - 1):
        #     self.MomentumTransfer_DF = pd.concat([self.MomentumTransfer_DF, pd.DataFrame(self.AlphaParticleMomentumMagnitudes_DF.iloc[:, step] - self.AlphaParticleMomentumMagnitudes_DF.iloc[:, step + 1])], axis = 1)
        
        if __name__ == "__main__":
            timing_studies.end_AlphaRTGame_calculate_DoseToMedium_MomentumTransferArray = time.time()
            timing_studies.append_TimingResults_ParticularLines("AlphaRTGame calculate_DoseToMedium() MomentumTransfer_Array calculation", timing_studies.end_AlphaRTGame_calculate_DoseToMedium_MomentumTransferArray - timing_studies.start_AlphaRTGame_calculate_DoseToMedium_MomentumTransferArray)


            timing_studies.start_AlphaRTGame_calculate_DoseToMedium_AbsoredDose = time.time()
        # The kinetic energy transferred to an electron from an alpha particle is given by the equation in the next line below. The total kinetic energy transferred to the electrons in the medium is just the sum of the kinetic energies transferred to each electron. Therefore, it is valid to calculate the momentum transfers first and leave the conversion of momentum into kinetic energy until later.
        # Kinetic energy transferred = (Initial momentum magnitude of the alpha particle - Final momentum magnitude of the alpha particle) / (2 * Electron mass)
        self.MomentumTransferred_Total = self.MomentumTransfer_Array.sum()
        # NOTE: Before multiprocessing
        # self.MomentumTransferred_Total = self.MomentumTransfer_Array.sum().sum() # Units: kg m/s.
        # NOTE: Before optimisation ...
        # self.MomentumTransferred_Total = self.MomentumTransfer_DF.sum().sum() # Units: kg m/s.

        self.KineticEnergyTransferred_Total = self.MomentumTransferred_Total ** 2 / (2 * self.ElectronMass_kg) # Units: J. The transferred momentum equals the momentum gained by the electrons in the medium.

        # Absorbed radiation dose is defined as the energy absorbed by the medium per unit mass. We can calculate the mass of irradiated medium from the volume of irradiated medium. We know the alpha beam's cross-sectional area. Its penetration depth, which is the 3rd spatial dimension, can be the maximum range of the beam.
        self.VolumeIrradiated = BeamHeight * BeamWidth * (self.MaximumRange * 1e2) # Units: cm^3. The 1.0s are there as placeholders in case I choose to let the user specify the cross-sectional area of the beam. However, changing the beam's cross-sectional area changes the number of alpha particles per unit volume. I.e., increasing the cross-sectional area of the beam while keeping the number of alpha particles in the beam constant means that the beam is less intense.
        self.MassIrradiated = self.VolumeIrradiated * self.MassDensity # Units: g.
        self.AbsorbedDose = self.KineticEnergyTransferred_Total / (self.MassIrradiated * 1e-3) # Units: J/kg = Gy.

        if __name__ == "__main__":
            timing_studies.end_AlphaRTGame_calculate_DoseToMedium_AbsoredDose = time.time()
            
            timing_studies.end_AlphaRTGame_calculate_DoseToMedium = time.time() # End this timer before appending the timing results of the AbsorbedDose calculation so that the appending is not included in the measured execution time.

            timing_studies.append_TimingResults_ParticularLines("AlphaRTGame calculate_DoseToMedium() AbsorbedDose calculation", timing_studies.end_AlphaRTGame_calculate_DoseToMedium_AbsoredDose - timing_studies.start_AlphaRTGame_calculate_DoseToMedium_AbsoredDose)

        
        # REFERENCES:
            # The SciPy community (2020). numpy.concatenate, https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html.

    
    def show_Progress(self, process): # This method prints a slightly different message compared to the method with the same name in the AlphaParticles class.
        if __name__ == "__main__":
            timing_studies.start_AlphaRTGame_ShowProgress = time.time()
        
        try:
            ### Calculate the progress.
            if self.ParticleNumber != 0: # Keep showing the maximum alpha particle kinetic energy in the beam until there are no more particles in the beam. The maximum kinetic energy decreases throughout the entire simulation. However, the number of alpha particles in the beam stays constant until near the end of the simulation where it rapidly decreases to 0. Thus, letting the user see the maximum alpha particle kinetic energy rather than how many particles remain in the beam gives them a better measure of the progress of the simulation.
                self.MaximumAlphaMomentum_now = max(((self.AlphaParticlesInfoList_ID_X_Momentum[:, 2:5] ** 2).sum(axis = 1) ** (1/2))) # Given the momentum vectors of all of the alpha particles in the beam, I want to pick out the one that has the highest magnitude. *In the same simulation step*, use the pandas DataFrame of the list of momentum vectors to calculate the magnitudes of the vectors all at once. Then pick out the maximum magnitude.
                self.MaximumAlphaEnergy_now = ((self.MaximumAlphaMomentum_now ** 2 / (2 * self.AlphaMass_kg)) / self.J_eV_ConversionFactor) * 1e-6 # This is the equation E_alpha = p_alpha ** 2 / (2 * AlphaMass), where E_alpha and p_alpha are the kinetic energy and momentum magnitude of the alpha particle, respectively. I want the kinetic energy in MeV.

                self.Progress_Percentage = (1.0 - self.MaximumAlphaEnergy_now / (self.InitialKineticEnergy - self.MinimumAlphaEnergy_eV * 1e-6)) ** (10) * 100 # The maximum alpha particle kinetic energy does not decrease linearly, but approximately proportionally to the specified power, which was chosen through trial and error. The "* 100" is for converting the fraction to a percentage.

            
            ### Show the progress.
            self.EndDelayTimer = time.time()

            if (self.StartDelayTimer is None) or (self.DelayTimer > self.DelayForShowingProgress):
                self.StartDelayTimer = time.time() # Give this variable a value.

            self.DelayTimer = self.EndDelayTimer - self.StartDelayTimer
            
            if self.DelayTimer > self.DelayForShowingProgress: # This time period is how much to wait before showing another message of the progress of each simulation instance.
                print("\tThe progress of Pooled Process {}".format(process + 1) + " is {0:0.2f}% ...".format(self.Progress_Percentage)) # It seems that all or none of the {}s must have a specification of the formatting to avoid the "ValueError: cannot switch from automatic field numbering to manual field specification" error. (I tried it myself, so there is no reference to cite.) Alternatively, I can separate the strings and use string concatenation.
              
        except AttributeError: # AttributeError is the error I saw in the command terminal when I specified an initial alpha particle kinetic energy less than the minimum energy required for a particle to stay in the beam.
            print("Error: You must specify an initial alpha particle kinetic energy greater than {} eV. The program will now exit.".format(self.MinimumAlphaEnergy_eV))
            exit() # This is what I want to happen in this case.
        
        except:
            print("Unknown Error: The program will now exit. Please restart the program and try again.") # An error besides AttributeError may be raised for some reason. I want the program to catch the error rather than crash.
            exit() # This is what I want to happen in this case.
        
        if __name__ == "__main__":
            timing_studies.end_AlphaRTGame_ShowProgress = time.time()
            timing_studies.AlphaRTGame_show_Progress_List.append(timing_studies.end_AlphaRTGame_ShowProgress - timing_studies.start_AlphaRTGame_ShowProgress) # This is the execution time for one execution of the update_ParticleNum() method.
        
    
    def process_SimulationForAlphaParticles(self, process): # The FOR in the update_AlphaParticleMomentum() of the AlphaParticles class over the number of alpha particles is made smaller by the parallelisation of this method, meaning that more particles may be simulated in a given time.
        print("Pooled process", process + 1, "has started with __name__ ==", __name__, "...")
        
        # The two variables below need to be redefined for each pooled process because the AlphaParticlesInfoList_ID_X_Momentum has less rows in it. Each row represents an alpha particle.
        self.AlphaParticlesInfoList_ID_X_Momentum = self.AlphaParticlesInfoList_ID_X_Momentum_ForProcesses[process]
        self.ParticleNumber = self.AlphaParticlesInfoList_ID_X_Momentum.shape[0] # Redefining this variable fixes an IndexError in the FOR loop of the update_AlphaParticleMomentum() method.
        
        
        ### Process the data. This WHILE loop is the simulation.
        while self.ParticleNumber > 0: # Use the ParticleNumber variable directly instead of using a method to retrieve it. I prefer this style.
            # We need something to take the alpha particles through each simulation step.
            self.update_AlphaParticlePosition() # Move each particle some distance until its location of collision with an electron.
            self.record_AlphaParticlePosition() # Record the new x-position of each alpha particle.
            self.update_AlphaParticleMomentum() # Simulate the collision of each alpha particle with an electron. Recalculate each alpha particle's momentum vector and position along the x-axis after the alpha particles collide with atomic electrons.
            self.record_AlphaParticleMomentumMagnitude()
            self.update_ParticleNum() # *Manage* how many alpha particles remain in the beam. Alpha particles leave the beam when they lose too much energy due to colliding with too many atomic electrons. When their energy is extremely low, they capture atomic electrons and become helium atoms, thus leaving the beam. This method does the removing.
            
            self.show_Progress(process) # Show the user the progress of each pooled process so that they may know whether the program is running or frozen. The argument of 0 is present because the show_Progress() method is inherited from the AlphaParticles class, which is used to run multiple instances of a simulation when the program is run in beam analysis mode. However, in the radiotherapy game mode, only one instance of a simulation is run. When the WHILE loop in main() is running, the would not see any update about whether the program is running or frozen if the show_Progress() method did not exist.
        
        return self.PositionXArray, self.AlphaParticleMomentumMagnitudes # Collect PositionXArray to calculate the maximnum range, and AlphaParticleMomentumMagnitudes to calculate absorbed dose. 
        
        # REFERENCES:
            # Fayek, H. (2020). Week 6 Object-Oriented Programming. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
    
    
    # NOTE: Before multiprocessing .... The process_SimulationForAlphaParticles() method above replaced this method when multiprocessing was implemented for for simulation in the radiotherapy game mode of the program.
    # def process_Simulation(self, instance): # Pass the "particle" argument to the show_Progress() method.
    #     self.make_Medium()
    #     self.initialise_Simulation(instance) # Prepare the arrays, lists and other variables that are to be used in the simulation using what was defined in the class's __init__() method.
        
    #     ### Process the data. This WHILE loop is the simulation.
    #     while self.ParticleNumber > 0: # Use the ParticleNumber variable directly instead of using a method to retrieve it. I prefer this style.
    #     # while alpha_beam.get_ParticleNum() > 0: # Keep taking the alpha particles away from the source until no alpha particles remain. **Each loop of this WHILE loop is a simulation step.**
    #         # We need something to take the alpha particles through each simulation step.
    #         self.update_AlphaParticlePosition() # Move each particle some distance until its location of collision with an electron.
    #         self.record_AlphaParticlePosition() # Record the new x-position of each alpha particle.
    #         self.update_AlphaParticleMomentum() # Simulate the collision of each alpha particle with an electron. Recalculate each alpha particle's momentum vector and position along the x-axis after the alpha particles collide with atomic electrons.
    #         self.record_AlphaParticleMomentumMagnitude()
    #         self.update_ParticleNum() # *Manage* how many alpha particles remain in the beam. Alpha particles leave the beam when they lose too much energy due to colliding with too many atomic electrons. When their energy is extremely low, they capture atomic electrons and become helium atoms, thus leaving the beam. This method does the removing.
            
    #         self.show_Progress(instance) # Show the user the progress of the simulation so that they may know whether the program is running or frozen. The "instance" argument is present because the show_Progress() method is inherited from the AlphaParticles class, which is used to run multiple instances of a simulation when the program is run in beam analysis mode. However, in the radiotherapy game mode, only one instance of a simulation is run. When the WHILE loop in main() is running, the would not see any update about whether the program is running or frozen if the show_Progress() method did not exist.
        
    #     # REFERENCES:
    #         # Fayek, H. (2020). Week 6 Object-Oriented Programming. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
    #         # Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
        

    def game_Outcome(self, DoseToDeposit_Gy): # Assess whether or not the user won the game.
        if __name__ == "__main__":
            timing_studies.start_AlphaRTGame_game_Outcome = time.time()
        
        self.DoseMargin_Fraction = 0.05 # The dose margin allows for some leniency due to the randomisation involved in the simulation.
        self.AbsorbedDose_LowerLimit = DoseToDeposit_Gy * (1.0 - self.DoseMargin_Fraction)
        self.AbsorbedDose_UpperLimit = DoseToDeposit_Gy * (1.0 + self.DoseMargin_Fraction)

        if self.AbsorbedDose_LowerLimit < self.AbsorbedDose < self.AbsorbedDose_UpperLimit:
            print("Well done! A dose between {} and {} Gy was delivered.".format(self.AbsorbedDose_LowerLimit, self.AbsorbedDose_UpperLimit))
        
        elif self.AbsorbedDose > self.AbsorbedDose_UpperLimit:
            print("Too much dose was delivered! Please try delivering {} Gy again.".format(DoseToDeposit_Gy))
        
        elif self.AbsorbedDose < self.AbsorbedDose_LowerLimit:
            print("Too little dose was delivered! Please try delivering {} Gy again.".format(DoseToDeposit_Gy))
        
        if __name__ == "__main__":
            timing_studies.end_AlphaRTGame_game_Outcome = time.time()

    # REFERENCES:
        # Zelle, J M (2017). Python Programming: An Introduction to Computer Science, 3rd ed. 2154 NE Broadway, Suite 100, Portland, Oregon 97232: Franklin, Beedle & Associates Inc.
        # Fayek, H (2020). Week 6 Object-Oriented Programming, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
if __name__ == "__main__":
    timing_studies.end_ClassDefinition_AlphaRTGame = time.time()
    timing_studies.append_TimingResults("AlphaRTGame class definition", timing_studies.end_ClassDefinition_AlphaRTGame - timing_studies.start_ClassDefinition_AlphaRTGame, "Once")

    timing_studies.start_ClassDefinition_AttenuationQuiz = time.time()


class AttenuationQuiz(AlphaParticles): # This class is for quizzing the user about what thickness of material is required to transmit a particular fraction of a randomly generated alpha particle beam.
    def __init__(self, InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity, ChosenMaterials_DF):
        super().__init__(InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity)

        self.ChosenMaterials_DF = ChosenMaterials_DF
        
        self.CorrectMaterialThickness = None # Initialise this variable for use in an IF statement.

    
    def ask_QuizQuestion(self):
        self.TransmissionFraction = round(random.random(), 3) # It is easier for the user to deal with a transmission fraction that has less decimal places than one than has more. Also, there is a very large range over which all particles are transmitted, meaning that there are many correct thicknesses for 100% transmission. Therefore, we omit 1.0 from being randomly chosen by using the random.random() random number generator. Rounding error is *not* a concern here.
        
        print("What thickness(es) of the chosen material(s), *together*, in m, will transmit {}% of a beam of {} alpha particles of energy {:.3e} MeV? ".format(self.TransmissionFraction * 1e2, self.InitialParticleNumber, self.InitialKineticEnergy))
        print("Note that the thickness of the last material you specify will be extended if it is too thin.") # The last material is too thin when there are still alpha particles to simulate. The particles must go through a medium, whichever one it is.
        print("Also note that you may add more materials to the 'AttenuationQuiz_MaterialLibrary.csv' file if you want the quiz to possibly consider other materials. However, you must adhere to the format of that file.")
        print()
        ### Ask whether or not the user would like to read material thicknesses from a file. We ask the user this question after they have seen which materials have been randomly selected. This is so that they may update the file before submitting it to the program.
        self.WhetherOrNotReadInputsFromFile_AttenuationQuiz = input("Would you like to read material thicknesses from the input file named 'InputsForAttenuationQuiz.txt'? (y/n) ")
        
        try: # Make sure the user gives a valid answer before proceeding with the quiz.
            assert self.WhetherOrNotReadInputsFromFile_AttenuationQuiz in set(["y", "Y", "n", "N"])
        
        except: # The user may restart the program. This is different to the case where a simulation has already run. The program is more lenient with invalid inputs and will deal with them in such a way that the it continues to run to the end. An example of such a case is when the program provides a default input, such as with the number of bins in the histograms of the off-diagonal elements of the randomised 3x3 matrix that is used to update alpha particles' momentum vectors.
            print("Error: You did not provide a valid answer. The program will now exit.")
            exit()
        
        if self.WhetherOrNotReadInputsFromFile_AttenuationQuiz in set(["y", "Y"]): # Read the material thicknesses from the input file.
            print("\n### You have chosen to let the program read the material thicknesses from a file. ###")
            print("The program will read from a file named 'InputsForAttenuationQuiz.txt' in the same directory as the script file of this program. Please make sure it is formatted as shown by example below ...")
            print("Ignore this line:", "#" * 10, "Input file for the attenuation quiz", "#" * 10)
            print("Medium 1 thickness = 1e-9 m")
            print("Medium 2 thickness = 1e-9 m")
            print("Medium 3 thickness = 1e-9 m")
            print("Medium 4 thickness = 1e-9 m")
            print("Medium 5 thickness = 1e-9 m")
            print("Medium 6 thickness = 1e-9 m")
            print("Medium 7 thickness = 1e-9 m")
            print("Medium 8 thickness = 1e-9 m")
            print("Medium 9 thickness = 1e-9 m")
            print("Medium 10 thickness = 1e-9 m")
            print("Ignore this line:", "#" * 4, "End of Input file for the attenuation quiz", "#" * 5)
            print()
            print("The only contents of the file you are permitted to change are *the numbers* at the right side of the '=' signs. This excludes the units.")
            print("You may also add more 'Medium [number] thickness ...' lines if you wish to. Please make sure the numbers are ordered and each line is formatted as shown above.")
            print("When you are ready for the program to read the input file, please say so ...")
            
            self.IsReadyToContinueWithFileInputs = input("\tAre you ready for the program to read the input file? Do not answer if you are not yet ready. (y) ")

            try: # Make sure the user gives a valid answer.
                assert self.IsReadyToContinueWithFileInputs in set(["y", "Y"]) # The program thinks the user answers "No" if they do not give an answer. In this case, it just keeps waiting for the user to say they are ready.
            
            except: # The user may restart the program. This is different to the case where a simulation has already run. The program is more lenient with invalid inputs and will deal with them in such a way that the it continues to run to the end. An example of such a case is when the program provides a default input, such as with the number of bins in the histograms of the off-diagonal elements of the randomised 3x3 matrix that is used to update alpha particles' momentum vectors.
                print("Error: You did not provide a valid answer. The program will now exit.")
                exit()
            
            if self.IsReadyToContinueWithFileInputs in set(["y", "Y"]):
                print("The program will now read as many of your inputs from the input file named 'InputsForAttenuationQuiz.txt' as the number of media you said you wanted to consider ...")
                
                try: # Make sure that the file exists.
                    self.InputFile_AttenuationQuiz = open("InputsForAttenuationQuiz.txt", "r")
                    self.InputFileLines_AttenuationQuiz = self.InputFile_AttenuationQuiz.readlines()
                    self.InputFile_AttenuationQuiz.close()
                
                except FileNotFoundError:
                    print("Error: The text file named 'InputsForAttenuationQuiz' was not found. Please make sure that there is such a file in the same directory as the script file of this program and try again. The program will now exit.")
                    exit()
                
                except: # ... in case the error is not a FileNotFoundError error.
                    print("Error: For some reason, the program could not read the input file. Please restart the program and input the material thicknesses via the command terminal. The program will now exit.")
                    exit()
                
                print("\n### The program has read the following thicknesses and replaced invalid inputs with valid ones where appropriate ... ###") # This line is to be shown to the user in preparation for the execution of the FOR loop below.
            
        elif self.WhetherOrNotReadInputsFromFile_AttenuationQuiz in set(["n", "N"]):
            print("\nOk. Please provide your inputs via the command terminal.\n")


        for medium in range(0, self.ChosenMaterials_DF.shape[0]): # Feed the inputs into the program whether the user provided them via the input file or the command terminal.
            if self.WhetherOrNotReadInputsFromFile_AttenuationQuiz in set(["y", "Y"]):
                try: # Make sure the format of the input file is correct.
                    self.ChosenMaterials_DF.iloc[medium, 4] = self.check_FloatingPointInput(float(self.InputFileLines_AttenuationQuiz[medium].replace("Medium {} thickness = ".format(medium + 1), "").replace(" m", "")))
                
                except ValueError:
                    print("Error: The input file was not formatted at line {} as specified earlier. Please fix the format of the file and try again. The program will now exit.".format(medium + 1)) # Help the user locate errors in the formatting of the input file.
                    exit()

                except IndexError:
                    print("Error: There are not enough material thicknesses specified in the input file. Please specify more material thicknesses and try again. The program will now exit.")
                    exit()
                
                except:
                    print("Error: An unknown error occurred. Please restart the program and input the material thicknesses via the command terminal. The program will now exit.")
                    exit()

                print(self.InputFileLines_AttenuationQuiz[medium].replace("\n", ""))
                
            elif self.WhetherOrNotReadInputsFromFile_AttenuationQuiz in set(["n", "N"]):
                try:
                    self.ChosenMaterials_DF.iloc[medium, 4] = self.check_FloatingPointInput(float(input("Thickness of {} as Medium {}, in m = ".format(self.ChosenMaterials_DF.iloc[medium, 0].lower(), medium + 1))))
                
                except:
                    print("Error: You must specify a number greater than or equal to 0.0. The program will now exit.")
                    exit()
                
                while self.ChosenMaterials_DF.iloc[medium, 4] < 0.0:
                    print("Error: A thickness cannot be negative. Please try again.")
                    try:
                        self.ChosenMaterials_DF.iloc[medium, 4] = self.check_FloatingPointInput(float(input("Thickness of {} as Medium {} = ".format(self.ChosenMaterials_DF.iloc[medium, 0].lower(), medium + 1))))
                    
                    except:
                        print("Error: You must specify a number greater than or equal to 0.0. The program will now exit.")
                        exit()

                print()
        
        print("\n### Let us test your prediction ... ###") # At this point, the simulation is going to be started.

        # REFERENCES:
            # Programiz Python Exception Handling Using try, except and finally statement, https://www.programiz.com/python-programming/exception-handling.

    
    def initialise_Simulation(self, instance): # Prepare the arrays, lists and other variables that are to be used in the simulation using what was defined in the class's __init__() method.
        print("Simulation Instance", instance + 1, "has been started with __name__ ==", __name__, "...")
        
        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__": # All of these time.time() calls must be protected with this IF statement so that the slave processes do not raise the "NameError: name 'timing_studies' is not defined" error.
        #     timing_studies.start_InitialiseSimulation = time.time()
        
        # All of the alpha particles in the beam are going to be kept track of using a pandas DataFrame. We want to keep track of each particle's momentum vector and x-position.
        self.AlphaParticleIDsList = np.array(list([range(0, self.InitialParticleNumber)])).T # Initialise a list for making a list of identification (ID) numbers for the alpha particles.
        
        # Now we initialise their x-positions, i.e., their positions along the x-axis.
        self.PositionXArray = np.array([[self.InitialPositionX]] * self.InitialParticleNumber) # Now there is one position along the x-axis for each alpha particle. We want a column vector, not a row vector.
        # NOTE: Before optimisation ...
        # self.PositionXList_DF = pd.DataFrame([self.InitialPositionX] * self.InitialParticleNumber) # Now there is one position along the x-axis for each alpha particle.

        ## Now we initialise their momentum vectors.
        # Initialise a general momentum vector for the alpha particles.
        self.MomentumVectorList = np.array([[self.InitialMomentumX, 0.0, 0.0]] * self.InitialParticleNumber)  # This is the list of inital momentum vectors of the alpha particle, in units of kg m/s. At the start of the first simulation step, every alpha particle has this momentum vector. *Initialise* a list of momentum vectors to keep track of each alpha particle's momentum. Now there is one momentum vector for each alpha particle. The [] around each individual momentum vector makes sure that each momentum vector is its own list. Treating the list of momentum vectors as a numpy array is necessary for making the calculations in the simulation involving vectors and matrices work properly.
        # NOTE: Before optimisation ...
        # self.MomentumVectorList_DF = pd.DataFrame([self.MomentumVector] * self.InitialParticleNumber) # *Initialise* a list of momentum vectors to keep track of each alpha particle's momentum. Now there is one momentum vector for each alpha particle. The [] around "MomentumVector" makes sure that each momentum vector is its own list. Treating the list of momentum vectors as a numpy array is necessary for making the calculations in the simulation involving vectors and matrices work properly.

        ## Now we calculate the cross-sections, which is a function of the alpha particle's energy. Consequently, each alpha particle will have its own mean free path.
        # We are going to need to know the momentum magnitude of each alpha particle. Also, the magnitude is used in other parts of the program. So, we might as well put it into the information DataFrame so that it does not have to be recalculated unnecessarily.
        self.MomentumMagnitudeList = np.array([((self.MomentumVectorList ** 2).sum(axis = 1)) ** (1/2)]).T # Momentum magnitudes. We need the arrays to be in columns for the upcoming concatenation into the info list.
        self.CrossSectionList = (2 * math.pi * self.AlphaMass_kg * (self.ClassicalElectronRadius_m) ** 2) / self.MomentumMagnitudeList ** 2 # Cross-section for each alpha particle. The pandas Series supports an element-wise operation.
        self.MeanFreePathInMediumList = (self.ElectronSpatialDensity * self.CrossSectionList) ** -1 # Mean free path in the medium for each alpha particle.
        # NOTE: Before optimisation ...
        # self.MomentumMagnitudeList_DF = ((self.MomentumVectorList_DF ** 2).sum(axis = 1)) ** (1/2) # Momentum magnitudes.
        # self.CrossSectionList_DF = (2 * math.pi * self.AlphaMass_kg * (self.ClassicalElectronRadius_m) ** 2) / self.MomentumMagnitudeList_DF ** 2 # Cross-section for each alpha particle. The pandas Series supports an element-wise operation.
        # self.MeanFreePathInMediumList_DF = (self.ElectronSpatialDensity * self.CrossSectionList_DF) ** -1 # Mean free path in the medium for each alpha particle.

        ### We are also going to define a medium for each alpha particle. Start with the first one.
        self.AtomicNumberList = np.array([[self.ChosenMaterials_DF.iloc[0, 1]]] * self.InitialParticleNumber)
        self.AtomicWeightList = np.array([[self.ChosenMaterials_DF.iloc[0, 2]]] * self.InitialParticleNumber)
        self.MassDensityList = np.array([[self.ChosenMaterials_DF.iloc[0, 3]]] * self.InitialParticleNumber)
        self.WhichMedium = np.array([[0]] * self.InitialParticleNumber)
        self.NextThicknessCheckPoint = np.array([[self.ChosenMaterials_DF.iloc[0, 4]]] * self.InitialParticleNumber)

        # Now we put all the above information into one pandas DataFrame.
        self.AlphaParticlesInfoList_ID_X_Momentum = np.concatenate((self.AlphaParticleIDsList, self.PositionXArray, self.MomentumVectorList, self.MomentumMagnitudeList, self.CrossSectionList, self.MeanFreePathInMediumList, self.AtomicNumberList, self.AtomicWeightList, self.MassDensityList, self.WhichMedium, self.NextThicknessCheckPoint), axis = 1) # This DataFrame will be useful for keeping each alpha particle's momentum vector attached to its x-position, especially when particles get removed from the beam when they have sufficiently low momentum.
        # NOTE: Before optimisation ...
        # self.AlphaParticlesInfoList_ID_X_Momentum_DF = pd.concat([pd.DataFrame(self.AlphaParticleIDsList), self.PositionXList_DF, self.MomentumVectorList_DF, self.MomentumMagnitudeList_DF, self.CrossSectionList_DF, self.MeanFreePathInMediumList_DF], axis = 1).T.reset_index(drop = True).T # This DataFrame will be useful for keeping each alpha particle's momentum vector attached to its x-position, especially when particles get removed from the beam when they have sufficiently low momentum.

        
        # *Initialise* a list for recording the number of alpha particles in the beam at each simulation step. Energy and range straggling of the particles does *not* affect the number of particles in the beam. Energy straggling is when all of the alpha particles start off with the same kinetic energy but lose different amounts of energy per collision with atomic electrons. Each particle has its own history of collisions and energy transfers. Particles with more energy travel further. Thus, energy straggling causes range straggling. Energy straggling is what causes the sigmoid curve at the end of the plot of the relationship between the number of particles in the beam and the simulation step. This plot is output from the program as a .png file.
        self.NumberParticlesInBeam = [self.InitialParticleNumber] # It is not necessary to treat this list as a numpy array because it is not used in any vector or matrix calculations.

        # Initialise a list for recording the numbers of the off-diagonal elements of the randomised 3x3 matrix (RandomMatrix). They are generated from the random numbers generated using the randomNum_0to1() method. The frequency of the occurrence of each RandomMatrix random number is going to be plotted to get an idea of the probability density function that was used to generate the numbers. The plot will be useful for the user for understanding the results of the simulation because which random numbers are generated affects the results.
        self.RandomNumList_C_xy = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_xz = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_yx = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_yz = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_zx = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        self.RandomNumList_C_zy = [] # Initialise a list for each off-diagonal element of the randomised 3x3 matrix.
        
        self.DelayForShowingProgress = 2.5 # Units: s. Do not print the progress of each simulation instance to the command terminal at each simulation step, which would flood the terminal with text.
        self.DelayTimer = 0.0
        self.StartDelayTimer = None # This is one of my typical solutions for avoiding the error of a variable being referenced in an IF statement before being defined.
        
        if instance == 0: # Print this message only once.
            print("Alpha particles will be removed from the beam when their kinetic energies fall below {0:0.3f} eV.".format(self.MinimumAlphaEnergy_eV)) # At which kinetic energy alpha particles are removed from the beam affects the results that the program outputs. The user must know what is affecting their results so that they may document it in their work/research. The minimum alpha kinetic energy may not be 1 eV, but may be expressed by a demical number in the future. Using the format() method keeps such numbers neatly presented.
            print() # Separate the above print() statement from text that is going to be printed to the screen later.


        # NOTE: Before multiprocessing ...
        # if __name__ == "__main__":
        #     timing_studies.end_InitialiseSimulation = time.time()
        #     timing_studies.initialise_Simulation_List.append(timing_studies.end_InitialiseSimulation - timing_studies.start_InitialiseSimulation)
        
        # REFERENCES:
            # grassworm, & Cees Timmerman. (2020, 16 May 2020). Display a decimal in scientific notation. Retrieved from https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
            # The SciPy community (2020). numpy.concatenate, https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html.
    
    
    def update_MediumForEachParticle(self):
        self.AlphaParticlesInfoList_ID_X_Momentum_DF = pd.DataFrame(self.AlphaParticlesInfoList_ID_X_Momentum) # Maybe we will avoid shape or index errors if we use a pandas DataFrame rather than a numpy array.
        
        for particle in range(0, self.AlphaParticlesInfoList_ID_X_Momentum.shape[0]):
            if self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 1] >= self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 12]:
                if self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11] < self.ChosenMaterials_DF.shape[0] - 1: # The beam has to go through a medium, whichever one it is. AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11] is an index for use with the ChosenMaterials_DF DataFrame.
                    self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11] = self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11] + 1

                    ## Recalculate the mean free path of the alpha particle.
                    self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 8] = self.ChosenMaterials_DF.iloc[int(self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11]), 1] # Recalculate the atomic number.
                    self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 9] = self.ChosenMaterials_DF.iloc[int(self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11]), 2] # Recalculate the atomic weight.
                    self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 10] = self.ChosenMaterials_DF.iloc[int(self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11]), 3] # Recalculate the mass density.

                    ## Recalculate the mean free path for the particle based on the medium it is in.
                    self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 7] = ((self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 8] * (self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 10] * self.AvogadrosNum / self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 9])) * self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 6]) ** -1

                    ## Update the NextThicknessCheckPoint variable for the particle.
                    self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 12] = self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 12] + self.ChosenMaterials_DF.iloc[int(self.AlphaParticlesInfoList_ID_X_Momentum_DF.iloc[particle, 11]), 4]

                   
        self.AlphaParticlesInfoList_ID_X_Momentum = np.array(self.AlphaParticlesInfoList_ID_X_Momentum_DF)
    
    
    def process_Simulation(self, instance): # Pass the "instance" argument to the show_Progress() method.
        self.make_Medium()
        self.initialise_Simulation(instance) # Prepare the arrays, lists and other variables that are to be used in the simulation using what was defined in the class's __init__() method.
            
        ### Process the data. This WHILE loop is the simulation.
        while self.ParticleNumber > 0: # Use the ParticleNumber variable directly instead of using a method to retrieve it. I prefer this style.
            # We need something to take the alpha particles through each simulation step.
            self.update_AlphaParticlePosition() # Move each particle some distance until its location of collision with an electron.
            self.update_MediumForEachParticle()
            self.record_AlphaParticlePosition() # Record the new x-position of each alpha particle.
            self.update_AlphaParticleMomentum() # Simulate the collision of each alpha particle with an electron. Recalculate each alpha particle's momentum vector and position along the x-axis after the alpha particles collide with atomic electrons.
            self.update_ParticleNum() # *Manage* how many alpha particles remain in the beam. Alpha particles leave the beam when they lose too much energy due to colliding with too many atomic electrons. When their energy is extremely low, they capture atomic electrons and become helium atoms, thus leaving the beam. This method does the removing.
            
            self.show_Progress(instance) # Show the user the progress of the simulation so that they may know whether the program is running or frozen. When the WHILE loop in main() is running, the would not see any update about whether the program is running or frozen if the show_Progress() method did not exist.
        
        # REFERENCES:
            # Fayek, H. (2020). Week 6 Object-Oriented Programming. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.

    
    
    def calculate_Data(self): # At the end of the simulation, we have a large DataFrame that has information about the x-position of each alpha particle in each simulation step. We want to make a histogram of the number of particles in the beam as a function of distance out of this DataFrame.
        if __name__ == "__main__":
            timing_studies.start_AttenuationQuiz_calculate_Data = time.time()
        
        ## Calculate the maximum range of the alpha particles. This is necessary for defining the upper limit of the distances to check for calculating the number of particles remaining in the beam as a function of distance. NOTE: The x-positions are in the same units as the mean free path, which has units of m.
        self.MaximumRange = self.PositionXArray.max().max() # The maximum range is the largest number in the DataFrame. It is the furthest distance an alpha particle in the beam has travelled. It is the easiest value to calculate out of the ones we are interested in. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method.
        # NOTE: Before optimisation ...
        ## Prepare the PositionXList_DF DataFrame for data analysis. 
        # self.PositionXList_DF = ((self.PositionXList_DF.T).reset_index(drop = True)).T # First, we make sure its columns are labelled by the simulation steps rather than all having the same label due to having been concatenated together. The reset_index() method works row-wise, so we transpose the DataFrame first. Then we reset the row labels and transpose the DataFrame back to its original shape. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method. However, we use parentheses to make reading the code easier.
        # self.MaximumRange = self.PositionXList_DF.max().max() # The maximum range is the largest number in the DataFrame. It is the furthest distance an alpha particle in the beam has travelled. It is the easiest value to calculate out of the ones we are interested in. The methods are evaluated one after the other, each one being applied to the result of the use of the previous method.


        ## Calculate the number of alpha particles remaining in the beam as a function of distance.
        self.NumOfDistancesToCheck = 5e2 # This variable is for specifying the number of points to be created using the np.linspace() method.
        self.DistancesToCheck = list(np.linspace(start = 0.0, stop = self.MaximumRange, num = int(self.NumOfDistancesToCheck), endpoint = True)) # Create the DistancesToCheckList to be zipped into a dictionary as values.
        
        self.NumbersList = list(range(0, len(self.DistancesToCheck))) # The list created here will be zipped into the dictionary for the DistancesToCheck list as keys.
        
        self.DistancesToCheck_Dict = dict(zip(self.NumbersList, self.DistancesToCheck))

        self.ParticleNumList_Distance = [] # This list is going to have the number of alpha particles remaining in the beam at each distance of interest.
        for distance_Key in range(0, len(self.DistancesToCheck_Dict)): # Use a nested FOR loop for now. Nested FOR loops are known to be relatively slow, but they get the job done in this case.
            self.ParticleNumber_DistanceCheck = self.InitialParticleNumber # Reset this variable for use in the FOR loop below.
            
            for particle in range(0, self.PositionXArray.shape[0]): # Check how many particles passed the distance of interest.
                if self.PositionXArray[particle,:].max() <= self.DistancesToCheck_Dict[distance_Key]: # For each particle that did not pass the distance of interest, decrement the ParticleNum variable by 1.
                    self.ParticleNumber_DistanceCheck = self.ParticleNumber_DistanceCheck - 1
            # NOTE: Before optimisation ...
            # for particle in range(0, self.PositionXList_DF.shape[0]): # Check how many particles passed the distance of interest.
            #     if self.PositionXList_DF.iloc[particle,:].max() <= self.DistancesToCheck_Dict[distance_Key]: # For each particle that did not pass the distance of interest, decrement the ParticleNum variable by 1.
            #         self.ParticleNumber_DistanceCheck = self.ParticleNumber_DistanceCheck - 1
            

            self.ParticleNumList_Distance.append(self.ParticleNumber_DistanceCheck)
       
        
        ## Calculate the thickness of material that transmitted the specified fraction of alpha particles.
        try: 
            self.ParticleNumberTransmitted = round(self.TransmissionFraction * self.InitialParticleNumber) # The number of particles transmitted is an integer. round() gives a better answer than int().
            self.CorrectMaterialThickness = self.DistancesToCheck[self.ParticleNumList_Distance.index(self.ParticleNumberTransmitted)]
        
        except: # Unlike for the MeanRange, either CorrectMaterialThickness_Backwards or CorrectMaterialThickness_Forwards may not be defined at all if they are in the same FOR loop because the FOR loop may end before both of them get assigned a value. Thus, they must be in separate FOR loops. However, this will affect the result, but it is better than having an error raised.
            for num in range(1, self.InitialParticleNumber - self.ParticleNumberTransmitted + 1): # Calculate a value for CorrectMaterialThickness_Backwards.
                try: # The code below can actually raise a ValueError error if a particular value is not found in the ParticleNumList_Distance list. Therefore, we include a TRY-EXCEPT code block in the FOR loop.
                    if self.ParticleNumberTransmitted + num >= self.InitialParticleNumber: # If this is the case, search for the furthest distance that *all* of the particles travelled just before the first particle left the beam.
                        self.CorrectMaterialThickness_Backwards = self.DistancesToCheck_Dict[self.ParticleNumList_Distance.index(len(self.ParticleNumList_Distance) - 1 - self.ParticleNumList_Distance[::-1].index(self.InitialParticleNumber))] # The index() method searches for the specified element from the start of the list. However, we want the index of the *last* element, so we flip the list. Having found the index of the last element in the flipped list, we want to know its index in the original list, so we calculate the original index.
                    
                    else:
                        self.CorrectMaterialThickness_Backwards = self.DistancesToCheck_Dict[self.ParticleNumList_Distance.index(self.ParticleNumberTransmitted + num)]
                    
                    if self.CorrectMaterialThickness_Backwards is not None:
                        break # Now that we have assigned a value to each of the two variables above, we do not need to iterate "num" anymore. We have what we wanted.
                    
                    else:
                        continue

                except:
                    continue # We want to use the normal behaviour of a FOR loop in that it goes to its next iteration. It is because of the ValueError error that we use a TRY-EXCEPT code block.
            
            for num in range(1, self.ParticleNumberTransmitted + 1): # Calculate a value for CorrectMaterialThickness_Forwards.
                try: # The code below can actually raise a ValueError error if a particular value is not found in the ParticleNumList_Distance list. Therefore, we include a TRY-EXCEPT code block in the FOR loop.
                    if self.ParticleNumberTransmitted - num <= 0: # We do not want self.ParticleNumberTransmitted - num being negative, so we stop it from being so.
                        self.CorrectMaterialThickness_Forwards = self.DistancesToCheck[-1] # Unlike with CorrectMaterialThickness_Backwards when the condition in the IF statement just above is True, we want the index of the first occurrence of 0 particles. The simulation stops when the number of particles in the beam is 0, meaning that there is only one occurrence of 0 in the list of the number of particles in the beam. We use the list version rather than the dictionary version of DistancesToCheck because [-1] for a dictionary means "the key named '-1'", which is not what we want, while for a list it refers to the last element, which is what we want.
                    
                    else:
                        self.CorrectMaterialThickness_Forwards = self.DistancesToCheck_Dict[self.ParticleNumList_Distance.index(self.ParticleNumberTransmitted - num)]
                    
                    if self.CorrectMaterialThickness_Forwards is not None:
                        break # Now that we have assigned a value to each of the two variables above, we do not need to iterate "num" anymore. We have what we wanted.
                    
                    else:
                        continue

                except:
                    continue # We want to use the normal behaviour of a FOR loop in that it goes to its next iteration. It is because of the ValueError error that we use a TRY-EXCEPT code block.

           
            self.CorrectMaterialThickness = np.array(self.CorrectMaterialThickness_Backwards, self.CorrectMaterialThickness_Forwards).mean() # The slope at the descending end of the plot of the number of particles in the beam as a function of distance is approximately linear. So we do linear interpolation. I prefer to use a numpy array and the mean() method instead of doing (a + b)/2, because the latter option seems a bit hard-coded to me.

        if __name__ == "__main__":
            timing_studies.end_AttenuationQuiz_calculate_Data = time.time()
        
        # REFERENCES:
            # Fayek, H (2020). Week 9 Scientific Python, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # the pandas development team (2014). pandas.DataFrame.reset_index, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html.
            # the pandas development team (2014). pandas.DataFrame.max, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.max.html.
            # The SciPy community (2020). numpy.linspace, https://numpy.org/doc/stable/reference/generated/numpy.linspace.html.
            # GeeksforGeeks Python | Convert two lists into a dictionary, https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/.
            # Fayek, H (2020). Week 2 Data Types, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
            # Programiz Python List index(), https://www.programiz.com/python-programming/methods/list/index.
            # Anand S Kumar (2015). What is the meaning of “int(a[::-1])” in Python? [duplicate], https://stackoverflow.com/questions/31633635/what-is-the-meaning-of-inta-1-in-python.
            # Programiz Python break and continue, https://www.programiz.com/python-programming/break-continue.
            # Krane, K S (2014). Introductory Nuclear Physics, Reprint ed. Durga Printo Graphics, Delhi: John Wiley & Sons, Inc.
        
    
    def quiz_Outcome(self):
        print("The simulation has ended.\n")
        print("### Results ###")

        self.TotalPredictedThickness = self.ChosenMaterials_DF.iloc[:, 4].sum()
        self.ThicknessMargin_Fraction = 0.10

        if self.TotalPredictedThickness < self.CorrectMaterialThickness:
            self.RequiredMaterialThicknesses = {medium : 0.0 for medium in range(0, self.ChosenMaterials_DF.shape[0])}
            
            for medium in range(0, self.ChosenMaterials_DF.shape[0] - 1):
                self.RequiredMaterialThicknesses[medium] = self.ChosenMaterials_DF.iloc[medium, 4] # There are infinitely many combinations of correct material thicknesses when there are multiple media to consider. Thus, we choose one solution, which is the one in which we let the thickness of only the last medium vary.
            
            self.RequiredMaterialThicknesses[self.ChosenMaterials_DF.shape[0] - 1] = self.CorrectMaterialThickness - self.ChosenMaterials_DF.iloc[0:(self.ChosenMaterials_DF.shape[0] - 1), 4].sum() # The thickness of the last material is extended if it is too thin. It is too thin when there are still alpha particles to simulate.
        
        elif self.TotalPredictedThickness > self.CorrectMaterialThickness:
            # Scale down the predicted thicknesses. Otherwise, the program will specify a negative required thickness for the last medium.
            self.RequiredMaterialThicknesses = {medium : (self.ChosenMaterials_DF.iloc[medium, 4] / (self.TotalPredictedThickness / self.CorrectMaterialThickness)) for medium in range(0, self.ChosenMaterials_DF.shape[0])}


        if self.CorrectMaterialThickness * (1.0 - self.ThicknessMargin_Fraction) < self.TotalPredictedThickness < self.CorrectMaterialThickness * (1.0 + self.ThicknessMargin_Fraction):
            print("Well done! Your prediction was correct.")
        
        elif self.TotalPredictedThickness < self.CorrectMaterialThickness * (1.0 - self.ThicknessMargin_Fraction):
            print("You predicted incorrectly. Too many alpha particles would be transmitted! With the given media, a total thickness of {:.3e} m was required. Please try again.".format(self.CorrectMaterialThickness))

            print("Here is one combination of correct material thicknesses ...")
            for medium in range(0, self.ChosenMaterials_DF.shape[0]):
                print("\tRequired thickness of Medium {} =".format(medium + 1), "{:.3e}".format(self.RequiredMaterialThicknesses[medium]), "m") 

        elif self.TotalPredictedThickness > self.CorrectMaterialThickness * (1.0 + self.ThicknessMargin_Fraction):
            print("You predicted incorrectly. Too few alpha particles would be transmitted! With the given media, a total thickness of {:.3e} m was required. Please try again.".format(self.CorrectMaterialThickness))

            print("Here is one combination of correct material thicknesses ...")
            for medium in range(0, self.ChosenMaterials_DF.shape[0]):
                print("\tRequired thickness of Medium {} =".format(medium + 1), "{:.3e}".format(self.RequiredMaterialThicknesses[medium]), "m") 
    
    
if __name__ == "__main__":
    timing_studies.end_ClassDefinition_AttenuationQuiz = time.time()
    timing_studies.append_TimingResults("AttenuationQuiz class definition", timing_studies.end_ClassDefinition_AttenuationQuiz - timing_studies.start_ClassDefinition_AttenuationQuiz, "Once")
    
    timing_studies.start_FunctionDefinition_main = time.time()


def main(): # This function is one of the functions that are at the highest level of the program. And it is the first function that actually gets *executed*. Writing the code for this function first helped me to write the code for defining the classes and their methods above.
    program_admin = ProgramAdmin()
    program_admin.show_AboutTheProgram() # This notice is for telling the user basic information about the program.
    program_admin.show_Instructions() # This notice tells the user intructions for how to use the program.
    
    if __name__ == "__main__":
        timing_studies.ExecutionTime_main_SimDistance_Option_Input, timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input, timing_studies.ExecutionTime_program_admin_get_InputsForAlphaBeam, timing_studies.ExecutionTime_program_admin_get_InputsForMedium, timing_studies.ExecutionTime_main_SimInstances_Input, timing_studies.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input, timing_studies.ExecutionTime_main_AnalyseBeam_AppendTimingResults = program_admin.initialise_TimersForMain() # ... in case any of these variables are not defined depending on which mode of the program is run. These variables are to be subtracted from the execution time of the main() function.
    
    ### Ask the user which mode they want to use the program in.
        timing_studies.start_main_SimDistance_Option_Input = time.time()
    
    SimDistance_Option = input("Would you like to analyse an alpha particle beam (a), play the radiotherapy game (g), or do the beam attenuation quiz (q)? ") # It is not likely that incorrect user input here will raise an error because all of their inputs are treated as a string.
    
    if __name__ == "__main__":
        timing_studies.end_main_SimDistance_Option_Input = time.time()
        timing_studies.ExecutionTime_main_SimDistance_Option_Input = timing_studies.end_main_SimDistance_Option_Input - timing_studies.start_main_SimDistance_Option_Input
    
    
    try:
        assert SimDistance_Option in set(["a", "A", "g", "G", "q", "Q"]) # The assertion here is an alternative to the code shown below. Using ASSERT instead of the IF-ELSE statement makes the purpose of the code more apparent, which is to make sure that the user provided a valid input for the question they were asked.
        # Alternative code:
            # if SimDistance_Option in ["a", "A", "g", "G"]:
            #     pass
            # else:
            #     print("Error: You did not input a valid answer for choosing whether or not you wanted to play the radiotherapy game. The program will now exit.")
            #     exit()
        
        # REFERENCES:
            # W3Schools (2020). Python assert Keyword, https://www.w3schools.com/python/ref_keyword_assert.asp.
            # W3Schools Python pass Statement, https://www.w3schools.com/python/ref_keyword_pass.asp.

    except:
        print("Error: You did not input a valid answer for choosing whether or not you wanted to play the radiotherapy game. The program will now exit.")
        exit()

    if SimDistance_Option in set(["a", "A"]): # Analyse an alpha particle beam.
        print("You have chosen to analyse an alpha particle beam.\n") # Using \n instead of print() on the next line is a way of reducing the number of lines of code in the file.

        if __name__ == "__main__":
            timing_studies.start_main_WhetherOrNotReadInputsFromFile_Input = time.time()
        
        WhetherOrNotReadInputsFromFile = input("Would you like to read inputs from InputsForBeamAnalysis.txt? (y/n) ")
        
        if __name__ == "__main__":
            timing_studies.end_main_WhetherOrNotReadInputsFromFile_Input = time.time()
            timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input = timing_studies.end_main_WhetherOrNotReadInputsFromFile_Input - timing_studies.start_main_WhetherOrNotReadInputsFromFile_Input

        try:
            assert WhetherOrNotReadInputsFromFile in set(["y", "Y", "n", "N"])
        
            # REFERENCES:
                # W3Schools (2020). Python assert Keyword, https://www.w3schools.com/python/ref_keyword_assert.asp.
        

        except:
            print("Error: You did not provide a valid answer. The program will now exit.")
            exit()
        
        
        if WhetherOrNotReadInputsFromFile in set(["y", "Y"]):
            InitialKineticEnergy, InitialParticleNumber, RandomDistribution, WhetherOrNotToSeed, AtomicNumber, AtomicWeight, MassDensity, SimInstances = program_admin.get_InputsForBeamAnalysisFromFile()
            
            try:
                program_admin.Seed = int(program_admin.InputFileLines_BeamAnalysis[4].replace("Seed = ", ""))
                
                if WhetherOrNotToSeed in set(["y", "Y"]):
                    random.seed(a = program_admin.Seed, version = 2) # These inputs are not accessed directly via the main() function as are the other inputs in the line above.
                
                elif WhetherOrNotToSeed in set(["n", "N"]):
                    print("The random number generators will *not* be seeded.")
            
            except:
                print("Error: Either an invalid answer was given for whether or not to seed or an invalid seed was given. Please give a valid seed. The program will now exit.")
                exit()
            
            
            ### Check whether or not the inputs are valid after they have been checked for whether or not they are in the correct data types.
            if InitialKineticEnergy <= program_admin.MinimumAlphaEnergy_eV * 1e-6:
                print("Error: The initial kinetic energy must be greater than {0:0.3f} eV".format(program_admin.MinimumAlphaEnergy_eV))
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif InitialParticleNumber <= 0:
                print("Error: The initial number of alpha particles must be at least 1.")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif RandomDistribution not in set(["basic", "discrete", "triangular", "uniform"]):
                print("Error: The random distribution must be one of the following options: basic, discrete, triangular, uniform.")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif WhetherOrNotToSeed not in set(["y", "Y", "n", "N"]):
                print("Error: An invalid answer was given for whether or not to seed the random number generators. The valid answers are yes (y or Y) and no (n or N).")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif AtomicNumber <= 0.0:
                print("Error: The atomic number cannot be zero or a negative number. Please try again.")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif AtomicWeight <= 0.0:
                print("Error: The atomic weight cannot be zero or a negative number. Please try again.")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif MassDensity <= 0.0:
                print("Error: The mass density cannot be zero or a negative number. Please try again.")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif SimInstances <= 0:
                print("Error: The number of simulation instances must be at least 1. Please try again.")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()


            # Tell me what the program read from the input file so that I know whether or not the program is doing what I expect it to be doing.
            print("### Inputs ###")
            print("Initial kinetic energy = {:.3e} MeV".format(InitialKineticEnergy))
            print("Initial particle number = {}".format(InitialParticleNumber))
            print("Random distribution = {}".format(RandomDistribution))
            print("Whether or not to seed = {}".format(WhetherOrNotToSeed))
            print("Seed for the random number generators = {}".format(program_admin.Seed))
            print("Atomic number of the medium = {}".format(AtomicNumber))
            print("Atomic weight of the medium = {} g/mol".format(AtomicWeight))
            print("Mass density of the medium = {} g/cm^3".format(MassDensity))
            print("Number of simulation instances = {}".format(SimInstances))
            print("#" * len("### Inputs ###"))

        elif WhetherOrNotReadInputsFromFile in set(["n", "N"]):
            ### Get the inputs.
            ## Define the alpha particle beam.
            if __name__ == "__main__":
                timing_studies.start_program_admin_get_InputsForAlphaBeam = time.time()
            
            InitialKineticEnergy, InitialParticleNumber, RandomDistribution = program_admin.get_InputsForAlphaBeam() # Here, we ask the user for the inputs. Due to the get_Inputs() function's return statement, it is a mere sequence in this line that is equivalent to x, y = 1, 2.
            
            if __name__ == "__main__":
                timing_studies.end_program_admin_get_InputsForAlphaBeam = time.time()
                timing_studies.ExecutionTime_program_admin_get_InputsForAlphaBeam = timing_studies.end_program_admin_get_InputsForAlphaBeam - timing_studies.start_program_admin_get_InputsForAlphaBeam

            ## Define the medium.
                timing_studies.start_program_admin_get_InputsForMedium = time.time()
            
            AtomicNumber, AtomicWeight, MassDensity = program_admin.get_InputsForMedium()
            
            if __name__ == "__main__":
                timing_studies.end_program_admin_get_InputsForMedium = time.time()
                timing_studies.ExecutionTime_program_admin_get_InputsForMedium = timing_studies.end_program_admin_get_InputsForMedium - timing_studies.start_program_admin_get_InputsForMedium

            ## Define the number of instances for the simulation.
            print() # Make the text in the command terminal more organised.
            
            if __name__ == "__main__":
                timing_studies.start_main_SimInstances_Input = time.time()
            
            try:
                SimInstances = int(program_admin.check_FloatingPointInput(float(input("How many instances of the simulation would you like to run? "))))
                
                while SimInstances <= 0:
                    print("Error: The number of simulation instances must be at least 1. Please try again.")
                    SimInstances = int(program_admin.check_FloatingPointInput(float(input("How many instances of the simulation would you like to run? "))))
            
            except:
                print("Error: You did not provide a valid answer. The program will now exit.")
                exit()
            
            if __name__ == "__main__":
                timing_studies.end_main_SimInstances_Input = time.time()
                timing_studies.ExecutionTime_main_SimInstances_Input = timing_studies.end_main_SimInstances_Input - timing_studies.start_main_SimInstances_Input
            
            print() # Separate the print-to-screen output of the alpha_beam.initialise_Simulation() method from the print-to-screen output of the alpha_beam.randomNum_0to1(alpha_beam.RandomDistribution) method. This makes the messages printed to the command terminal easier to see for the user.
        
        
        ### Initialise dictionaries for the simulation.
        alpha_beam_dict = {instance : AlphaParticles(InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity) for instance in range(0, SimInstances)} # Create the alpha particle beam. Transfer the MeanFreePath variable into the AlphaParticles() class.
        MaximumRanges_Dict = {instance : 0 for instance in range(0, SimInstances)} # ... for collecting the maximum range from each simulation instance.
        ParticleNumDict_Distance_Dict = {instance : 0 for instance in range(0, SimInstances)} # ... for collecting the relationship between the number of alpha particles in the beam as a function of distance that the beam travelled from each simulation instance.
        MeanRanges_Dict = {instance : 0 for instance in range(0, SimInstances)} # ... for collecting the mean range from each simulation instance.

        statistical_analyser = StatisticalAnalysis(InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity, SimInstances) # This is the object for statistically analysing the simulation's results.
        
        statistical_analyser.SimInstances, statistical_analyser.alpha_beam_dict, statistical_analyser.MaximumRanges_Dict, statistical_analyser.ParticleNumDict_Distance_Dict, statistical_analyser.MeanRanges_Dict = SimInstances, alpha_beam_dict, MaximumRanges_Dict, ParticleNumDict_Distance_Dict, MeanRanges_Dict # Simplify the code for multiprocessing by passing the arguments of the statistical_analyser.process_MultipleInstancesOfSimulation() into the StatisticalAnalysis class before the multiprocessing code is executed.
        
        
        ################################### Run the simulation instances using multiprocessing ###################################
        ### The uncommented code in this multiprocessing section of the program file is a multiprocessing version of the commented out code shown just below, which was used as intermediate code for implementing multiprocessing.
        # for instance in range(0, self.SimInstances):
        #     self.alpha_beam_dict[instance].process_Simulation(instance) # Run the simulation instances and have the results of each instance ready for collection.  # Run each simulation instance.
        #     print("Analysing the data from Simulation Instance {} ...".format(instance + 1)) # Tell the user what is happening. This process can take some time because of the large amount of data that must be processed, especially for producing a plot of the number of alpha particles in the beam as a function of penetration distance into the medium.
        #     self.alpha_beam_dict[instance].calculate_Data() # Calculate the results.

        if __name__ == "__main__":
            statistical_analyser.SimInstances_List = list(range(0, statistical_analyser.SimInstances)) # Store the list as a variable so that the program does not have to recreate the list each time it is needed. Doing this may let the program run slightly faster.
            
            pool_BeamAnalysis = mp.Pool(processes = min(int(MaxCPUCoresToUse), statistical_analyser.SimInstances)) # The min() function is used to make sure that there is always one process per simulation instance but not more than the specified fraction of the total number of CPU cores the computer has.

            timing_studies.start_PooledProcesses = time.time()  # Determine the execution time of the method that is being parallelised.
            PoolResult_BeamAnalysis = pool_BeamAnalysis.map(statistical_analyser.process_SimulationInstance, statistical_analyser.SimInstances_List) # A list is input into the map() method and another list is output. This means that we can treat "PoolResult_BeamAnalysis" as a list.

            pool_BeamAnalysis.close() # These two methods are required to end the pool.
            pool_BeamAnalysis.join()

            timing_studies.end_PooledProcesses = time.time()
            
            print()
            print("Execution time of all pooled processes as a whole =", timing_studies.end_PooledProcesses - timing_studies.start_PooledProcesses, "s")
            print()

            statistical_analyser.alpha_beam_dict = dict(zip(statistical_analyser.SimInstances_List, PoolResult_BeamAnalysis)) # The output of the map() method was a list, so we can cast it back into the alpha_beam_dict dictionary.
       
        # REFERENCES:
            # Python Software Foundation (2020). multiprocessing — Process-based parallelism, https://docs.python.org/3/library/multiprocessing.html.
            # 0612 TV w/ NERDfirst (2018). Python's Multiprocess Pool - Friday Minis 267, https://www.youtube.com/watch?v=WdorgAKWbns.
            # When Maths meets coding (2020). Multiprocessing in python complete tutorial, https://www.youtube.com/watch?v=rZ5CSsgv5hs.
        
        ##########################################################################################################################
        # NOTE: Before multiprocessing ... The multiprocessing code above replaced this code. However, a few methods were taken out of the process_Simulation() method while implementing multiprocessing.
        # for instance in range(0, SimInstances):
        #     # Run each simulation instance.
        #     alpha_beam_dict[instance].process_Simulation(instance) # Run the simulation instances and have the results of each instance ready for collection.
            
        #     # Gather the results of each simulation instance.
        #     MaximumRanges_Dict[instance], ParticleNumDict_Distance_Dict[instance], MeanRanges_Dict[instance] = alpha_beam_dict[instance].get_Results() # Collect the results of the simulation instance.


        if __name__ == "__main__":
            ### Calculate the results.
            statistical_analyser.get_DataFromSimulationInstances()
            
            ### Now that we have the results we need, we must analyse them statistically.
            # Mean range = Average +/- 3 * Standard deviation, assuming normal distribution.
            MeanRange_Average = statistical_analyser.calculate_and_get_Average(statistical_analyser.MeanRanges_Dict)
            MeanRange_Uncertainty = 3 * statistical_analyser.calculate_and_get_PopulationStandardDeviation(statistical_analyser.MeanRanges_Dict) # The uncertainty should be a 99.7% confidence interval, assuming that the values are normally distributed.

            # Maximum range = Average +/- 3 * Standard deviation, assuming normal distribution.
            MaximumRange_Average = statistical_analyser.calculate_and_get_Average(statistical_analyser.MaximumRanges_Dict)
            MaximumRange_Uncertainty = 3 * statistical_analyser.calculate_and_get_PopulationStandardDeviation(statistical_analyser.MaximumRanges_Dict) # The uncertainty should be a 99.7% confidence interval, assuming that the values are normally distributed.

            # Plot the numbers of particles in the beam as functions of distance all in one figure. NOTE: If it is possible to deal with the varying lengths of the ParticleNum_Distance lists and calculate the average and standard deviation in the number of particles for each distance, I do not know how to do it. The distances are randomly generated, and the number of data points for each simulation instance varies.
            statistical_analyser.plot_ParticleNum(statistical_analyser.SimInstances, statistical_analyser.alpha_beam_dict)
            
            # Save the data.
            statistical_analyser.save_Data(program_admin.Seed, MeanRange_Average, MeanRange_Uncertainty, MaximumRange_Average, MaximumRange_Uncertainty, statistical_analyser.SimInstances, SimDistance_Option)

            # Plot a histogram for the off-diagonal random elements of the randomised 3x3 matrix from all instances of the simulation.
            if __name__ == "__main__":
                timing_studies.start_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input = time.time()
            
            statistical_analyser.plot_RandomMatrixOffDiagonals_All(statistical_analyser.SimInstances, statistical_analyser.alpha_beam_dict)
            
            if __name__ == "__main__":
                timing_studies.end_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input = time.time()
                timing_studies.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input = timing_studies.end_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input - timing_studies.start_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input

        # Append the timing data from the methods used above.
        if __name__ == "__main__":
            try:
                timing_studies.start_main_AnalyseBeam_AppendTimingResults = time.time()
                
                # NOTE: Before multiprocessing ... However, there is still some code in this section that was not commented out.
                # if np.array(timing_studies.initialise_Simulation_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles initialise_Simulation() (average)", np.array(timing_studies.initialise_Simulation_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles initialise_Simulation() (sum)", np.array(timing_studies.initialise_Simulation_List).sum(), "Sum")
                
                # if np.array(timing_studies.randomNum_0to1_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles randomNum_0to1() (average)", np.array(timing_studies.randomNum_0to1_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles randomNum_0to1() (sum)", np.array(timing_studies.randomNum_0to1_List).sum(), "Sum")
                    
                # if np.array(timing_studies.update_AlphaParticlePosition_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles update_AlphaParticlePosition() (average)", np.array(timing_studies.update_AlphaParticlePosition_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles update_AlphaParticlePosition() (sum)", np.array(timing_studies.update_AlphaParticlePosition_List).sum(), "Sum")
                
                # if np.array(timing_studies.record_AlphaParticlePosition_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles record_AlphaParticlePosition() (average)", np.array(timing_studies.record_AlphaParticlePosition_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles record_AlphaParticlePosition() (sum)", np.array(timing_studies.record_AlphaParticlePosition_List).sum(), "Sum")
                
                # if np.array(timing_studies.generate_RandomMatrix_Momentum_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles generate_RandomMatrix_Momentum() (average)", np.array(timing_studies.generate_RandomMatrix_Momentum_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles generate_RandomMatrix_Momentum() (sum)", np.array(timing_studies.generate_RandomMatrix_Momentum_List).sum(), "Sum")
                
                # if np.array(timing_studies.generate_RandomMatrix_Momentum_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles update_AlphaParticleMomentum() (average)", np.array(timing_studies.update_AlphaParticleMomentum_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles update_AlphaParticleMomentum() (sum)", np.array(timing_studies.update_AlphaParticleMomentum_List).sum(), "Sum")
                
                # if np.array(timing_studies.update_ParticleNum_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles update_ParticleNum() (average)", np.array(timing_studies.update_ParticleNum_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles update_ParticleNum() (sum)", np.array(timing_studies.update_ParticleNum_List).sum(), "Sum")
                
                # if np.array(timing_studies.show_Progress_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles show_Progress() (average)", np.array(timing_studies.show_Progress_List).mean(), "Average")
                #     timing_studies.append_TimingResults("AlphaParticles show_Progress() (sum)", np.array(timing_studies.show_Progress_List).sum(), "Sum")

                # if np.array(timing_studies.show_Progress_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults("AlphaParticles calculate_Data() (average)", np.array(timing_studies.calculate_Data_List).mean(), "Average")
                #     if np.array(timing_studies.calculate_Data_List).mean() > 0.0: # ... for avoiding a RuntimeWarning error about dividing by 0. The warning message that is raised if the program tries to do this is "RuntimeWarning: invalid value encountered in double_scalars".
                #         timing_studies.append_TimingResults("AlphaParticles calculate_Data() (sum)", np.array(timing_studies.calculate_Data_List).sum(), "Sum")
                
                timing_studies.append_TimingResults("AlphaParticles get_Results() (average)", np.array(timing_studies.get_Results_List).mean(), "Average")
                if np.array(timing_studies.get_Results_List).mean() > 0.0: # ... for avoiding a RuntimeWarning error about dividing by 0. The warning message that is raised if the program tries to do this is "RuntimeWarning: invalid value encountered in double_scalars".
                    timing_studies.append_TimingResults("AlphaParticles get_Results() (sum)", np.array(timing_studies.get_Results_List).sum(), "Sum")
                
                timing_studies.append_TimingResults("StatisticalAnalysis calculate_and_get_Average() (average)", np.array(timing_studies.StatAnalysis_calculate_and_get_Average_List).mean(), "Average")
                if np.array(timing_studies.StatAnalysis_calculate_and_get_Average_List).mean() > 0.0: # ... for avoiding a RuntimeWarning error about dividing by 0. The warning message that is raised if the program tries to do this is "RuntimeWarning: invalid value encountered in double_scalars".
                    timing_studies.append_TimingResults("StatisticalAnalysis calculate_and_get_Average() (sum)", np.array(timing_studies.StatAnalysis_calculate_and_get_Average_List).sum(), "Sum")
                
                timing_studies.append_TimingResults("StatisticalAnalysis calculate_and_get_PopulationStandardDeviation() (average)", np.array(timing_studies.StatAnalysis_calculate_and_get_PopulationStandardDeviation_List).mean(), "Average")
                if np.array(timing_studies.StatAnalysis_calculate_and_get_PopulationStandardDeviation_List).mean() > 0.0: # ... for avoiding a RuntimeWarning error about dividing by 0. The warning message that is raised if the program tries to do this is "RuntimeWarning: invalid value encountered in double_scalars".
                    timing_studies.append_TimingResults("StatisticalAnalysis calculate_and_get_PopulationStandardDeviation() (sum)", np.array(timing_studies.StatAnalysis_calculate_and_get_PopulationStandardDeviation_List).sum(), "Sum")
            
                # NOTE: Before multiprocessing ...
                # if np.array(timing_studies.update_ParticleNum_MomentumMagnitudeCalculation_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults_ParticularLines("AlphaParticles update_ParticleNum() MomentumMagnitudeCalculation (average)", np.array(timing_studies.update_ParticleNum_MomentumMagnitudeCalculation_List).mean())
                    
                # if np.array(timing_studies.update_ParticleNum_NumpyArrayMask_List).shape[0] > 0: # ... for avoiding a RuntimeWarning error about calculating the mean of an empty slice.
                #     timing_studies.append_TimingResults_ParticularLines("AlphaParticles update_ParticleNum() NumpyArrayMask (average)", np.array(timing_studies.update_ParticleNum_NumpyArrayMask_List).mean())

                timing_studies.end_main_AnalyseBeam_AppendTimingResults = time.time()
                timing_studies.ExecutionTime_main_AnalyseBeam_AppendTimingResults = timing_studies.end_main_AnalyseBeam_AppendTimingResults - timing_studies.start_main_AnalyseBeam_AppendTimingResults
            
            except:
                print("Error: Sorry, the timing experiments currently do not work to their full extent when doing multiprocessing.")
        
        return SimDistance_Option, SimInstances, timing_studies.ExecutionTime_main_SimDistance_Option_Input, timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input, timing_studies.ExecutionTime_program_admin_get_InputsForAlphaBeam, timing_studies.ExecutionTime_program_admin_get_InputsForMedium, timing_studies.ExecutionTime_main_SimInstances_Input, timing_studies.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input, timing_studies.ExecutionTime_main_AnalyseBeam_AppendTimingResults # These variables must be used outside of the main() function by the timing_studies object.

        # REFERENCES:
                # Fayek, H. (2020). Week 2 Data Types. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
                # Fayek, H. (2020). Week 5 Functions and Modularity. 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
                # Zelle, J M (2017). Python Programming: An Introduction to Computer Science, 3rd ed. 2154 NE Broadway, Suite 100, Portland, Oregon 97232: Franklin, Beedle & Associates Inc.
                
    
    elif SimDistance_Option in set(["g", "G"]): # Play the radiotherapy game.
        print("You have chosen to play the radiotherapy game.\n")
        
        ### Present the problem to the user.
        program_admin.specify_MediumForRTGame() # Initialise some values for presenting the problem of the game to the user.
        DoseToDeposit_Gy = program_admin.present_RTGameProblem() # Introduce the problem of the game to the user.

        ### Get the inputs for defining the alpha particle beam.
        AtomicNumber, AtomicWeight, MassDensity = program_admin.get_MediumCharacteristicsForRTGame() # Transfer the parameters of the medium to the AlphaRTGame class.

        if __name__ == "__main__":
            timing_studies.start_main_WhetherOrNotReadInputsFromFile_Input = time.time()

        WhetherOrNotReadInputsFromFile = input("Would you like to read inputs from InputsForRTGame.txt? (y/n) ")
        
        if __name__ == "__main__":
            timing_studies.end_main_WhetherOrNotReadInputsFromFile_Input = time.time()
            timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input = timing_studies.end_main_WhetherOrNotReadInputsFromFile_Input - timing_studies.start_main_WhetherOrNotReadInputsFromFile_Input

        try:
            assert WhetherOrNotReadInputsFromFile in set(["y", "Y", "n", "N"])
        
            # REFERENCES:
                # W3Schools (2020). Python assert Keyword, https://www.w3schools.com/python/ref_keyword_assert.asp.
        

        except:
            print("Error: You did not provide a valid answer. The program will now exit.")
            exit()
        
        if WhetherOrNotReadInputsFromFile in set(["y", "Y"]):
            InitialKineticEnergy, InitialParticleNumber, RandomDistribution, WhetherOrNotToSeed, BeamHeight, BeamWidth = program_admin.get_InputsForRTGameFromFile()
            
            try:
                program_admin.Seed = int(program_admin.InputFileLines_RTGame[4].replace("Seed = ", ""))
                
                if WhetherOrNotToSeed in set(["y", "Y"]):
                    random.seed(a = program_admin.Seed, version = 2) # These inputs are not accessed directly via the main() function as are the other inputs in the line above.
                
                elif WhetherOrNotToSeed in set(["n", "N"]):
                    print("The random number generators will *not* be seeded.")
            
            except:
                print("Error: An invalid seed was given. Please give a valid seed. The program will now exit.")
                exit()
            
            SimInstances = 1 # Give this variable a value so that the SimDistance_Option, SimInstances = main() line at the end of this program file works. 

            ### Check whether or not the inputs are valid after they have been checked for whether or not they are in the correct data types.
            if InitialKineticEnergy <= program_admin.MinimumAlphaEnergy_eV * 1e-6:
                print("Error: The initial kinetic energy must be greater than {0:0.3f} eV".format(program_admin.MinimumAlphaEnergy_eV))
                print("Please check the input file named 'InputsForRTGame.txt'. The program will now exit.")
                exit()
            
            elif InitialParticleNumber <= 0:
                print("Error: The initial number of alpha particles must be at least 1.")
                print("Please check the input file named 'InputsForRTGame.txt'. The program will now exit.")
                exit()
            
            elif RandomDistribution not in set(["basic", "discrete", "triangular", "uniform"]):
                print("Error: The random distribution must be one of the following options: basic, discrete, triangular, uniform.")
                print("Please check the input file named 'InputsForRTGame.txt'. The program will now exit.")
                exit()
            
            elif WhetherOrNotToSeed not in set(["y", "Y", "n", "N"]):
                print("Error: An invalid answer was given for whether or not to seed the random number generators. The valid answers are yes (y or Y) and no (n or N).")
                print("Please check the input file named 'InputsForBeamAnalysis.txt'. The program will now exit.")
                exit()
            
            elif BeamHeight <= 0.0:
                print("Error: The beam's height must be greater than 0.0 cm.")
                print("Please check the input file named 'InputsForRTGame.txt'. The program will now exit.")
                exit()
            
            elif BeamWidth <= 0.0:
                print("Error: The beam's width must be greater than 0.0 cm.")
                print("Please check the input file named 'InputsForRTGame.txt'. The program will now exit.")
                exit()
            

            ### Tell me what the program read from the input file so that I know whether or not the program is doing what I expect it to be doing.
            print("### Inputs ###")
            print("Initial kinetic energy = {:.3e} MeV".format(InitialKineticEnergy))
            print("Initial particle number = {}".format(InitialParticleNumber))
            print("Random distribution = {}".format(RandomDistribution))
            print("Seed for the random number generators = {}".format(program_admin.Seed))
            print("Beam height = {} cm".format(BeamHeight))
            print("Beam width = {} cm".format(BeamWidth))
            print("Atomic number of the medium = {}".format(AtomicNumber))
            print("Atomic weight of the medium = {} g/mol".format(AtomicWeight))
            print("Mass density of the medium = {} g/cm^3".format(MassDensity))
            print("Number of simulation instances = {}".format(SimInstances))
            print("#" * len("### Inputs ###"))
        
        elif WhetherOrNotReadInputsFromFile in set(["n", "N"]): 
            InitialKineticEnergy, InitialParticleNumber, RandomDistribution = program_admin.get_InputsForAlphaBeam() # Here, we ask the user for the inputs. Due to the get_Inputs() function's return statement, it is a mere sequence in this line that is equivalent to x, y = 1, 2.
            BeamHeight, BeamWidth = program_admin.get_InputsForAlphaBeam_CrossSectionalArea()

        
        alpha_RT_game = AlphaRTGame(InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity)

        
        ## Make the medium. Simulate the alpha beam travelling through the tissue and depositing energy into it.
        alpha_RT_game.make_Medium()
        alpha_RT_game.initialise_Simulation(0) # Prepare the arrays, lists and other variables that are to be used in the simulation using what was defined in the class's __init__() method.

        ################################### Simulate the alpha particles using multiprocessing ###################################
        if __name__ == "__main__":
            ### Divide the number of alpha particles equally amongst all of the pooled processes that are going to be made.
            NumOfProcesses = min(int(MaxCPUCoresToUse), alpha_RT_game.InitialParticleNumber)
            
            print("The simulation of the total number of alpha particles in the beam will be equally distributed to", NumOfProcesses, "pooled processes.\n")
            
            ProcessList = list(range(0, NumOfProcesses))
            ProcessDict_InfoList = {process : [] for process in ProcessList}

            for StartParticle in range(0, NumOfProcesses):
                for particle in range(StartParticle, alpha_RT_game.InitialParticleNumber, NumOfProcesses):
                    ProcessDict_InfoList[StartParticle].append(particle) # Get the indices that are going to be used to extract particles from alpha_RT_game.AlphaParticlesInfoList_ID_X_Momentum for each pooled process.

                ProcessDict_InfoList[StartParticle] = np.array(ProcessDict_InfoList[StartParticle])

            
            alpha_RT_game.AlphaParticlesInfoList_ID_X_Momentum_ForProcesses = {process : [] for process in ProcessList} # Initialise a dictionary for use as the iterable in the mp.Pool().map() method.
            
            for process in ProcessList:
                alpha_RT_game.AlphaParticlesInfoList_ID_X_Momentum_ForProcesses[process] = alpha_RT_game.AlphaParticlesInfoList_ID_X_Momentum[ProcessDict_InfoList[process], :]
            
            
            ### Make and run the pooled processes.
            pool_SimulateAlphaParticles = mp.Pool(processes = NumOfProcesses)

            PoolResult_AlphaRTGame_Particles = pool_SimulateAlphaParticles.map(alpha_RT_game.process_SimulationForAlphaParticles, ProcessList) # Each pooled process takes a subset of all the alpha particles and simulates them.
            # PoolResult_AlphaRTGame_Particles is a list of tuples of numpy arrays: [(np.array(), np.array()), (np.array(), np.array()), (np.array(), np.array()), ...].

            pool_SimulateAlphaParticles.close()
            pool_SimulateAlphaParticles.join()

            ### The mp.Pool().map() method above returns a list of NumOfProcesses tuples. Each tuple has an alpha_RT_game.PositionXArray array and an alpha_RT_game.AlphaParticleMomentumMagnitudes_List array. We must extract them from each tuple and merge them into one alpha_RT_game.PositionXArray array and one alpha_RT_game.AlphaParticleMomentumMagnitudes_List array.
            # Initialise the numpy arrays because numpy concatenation requires that the arrays being concatenated have the same shape along the axis of concatenation.
            alpha_RT_game.PositionXArray = PoolResult_AlphaRTGame_Particles[0][0][0:(len(PoolResult_AlphaRTGame_Particles[0][1]))] # For some reason, a row of 0's appears in this array. However, the array for the AlphaParticleMomentumMagnitudes variable has the correct shape.
            alpha_RT_game.AlphaParticleMomentumMagnitudes = PoolResult_AlphaRTGame_Particles[0][1]
            
            
            for process in range(1, NumOfProcesses):
                ### Merge the PositionXArray arrays from all pooled processes together. We had split the total number of alpha particles amongst pooled processes. Now we are bringing them back together. The IF-ELIF statements below are for making sure that the numpy arrays being concatenated have the same shape along the axis of concatenation.
                if PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))].shape[1] == alpha_RT_game.PositionXArray.shape[1]:
                    alpha_RT_game.PositionXArray = np.concatenate((alpha_RT_game.PositionXArray, PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))]), axis = 0)
                
                elif PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))].shape[1] < alpha_RT_game.PositionXArray.shape[1]:
                    _ = np.concatenate((PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))], np.zeros((PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))].shape[0], alpha_RT_game.PositionXArray.shape[1] - PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))].shape[1]))), axis = 1)
                    alpha_RT_game.PositionXArray = np.concatenate((alpha_RT_game.PositionXArray, _), axis = 0)
                
                elif PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))].shape[1] > alpha_RT_game.PositionXArray.shape[1]:
                    _ = np.concatenate((alpha_RT_game.PositionXArray, np.zeros((alpha_RT_game.PositionXArray.shape[0], PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))].shape[1] - alpha_RT_game.PositionXArray.shape[1]))), axis = 1)
                    alpha_RT_game.PositionXArray = np.concatenate((_, PoolResult_AlphaRTGame_Particles[process][0][0:(len(PoolResult_AlphaRTGame_Particles[process][1]))]), axis = 0)
                
                
                ### Merge the AlphaParticleMomentumMagnitudes arrays from all pooled processes together. We had split the total number of alpha particles amongst pooled processes. Now we are bringing them back together. The IF-ELIF statements below are for making sure that the numpy arrays being concatenated have the same shape along the axis of concatenation.
                if PoolResult_AlphaRTGame_Particles[process][1].shape[1] == alpha_RT_game.AlphaParticleMomentumMagnitudes.shape[1]:
                    alpha_RT_game.AlphaParticleMomentumMagnitudes = np.concatenate((alpha_RT_game.AlphaParticleMomentumMagnitudes, PoolResult_AlphaRTGame_Particles[process][1]), axis = 0)
                
                elif PoolResult_AlphaRTGame_Particles[process][1].shape[1] < alpha_RT_game.AlphaParticleMomentumMagnitudes.shape[1]:
                    _ = np.concatenate((PoolResult_AlphaRTGame_Particles[process][1], np.zeros((PoolResult_AlphaRTGame_Particles[process][1].shape[0], alpha_RT_game.AlphaParticleMomentumMagnitudes.shape[1] - PoolResult_AlphaRTGame_Particles[process][1].shape[1]))), axis = 1)
                    alpha_RT_game.AlphaParticleMomentumMagnitudes = np.concatenate((alpha_RT_game.AlphaParticleMomentumMagnitudes, _), axis = 0)
                
                elif PoolResult_AlphaRTGame_Particles[process][1].shape[1] > alpha_RT_game.AlphaParticleMomentumMagnitudes.shape[1]:
                    _ = np.concatenate((alpha_RT_game.AlphaParticleMomentumMagnitudes, np.zeros((alpha_RT_game.AlphaParticleMomentumMagnitudes.shape[0], PoolResult_AlphaRTGame_Particles[process][1].shape[1] - alpha_RT_game.AlphaParticleMomentumMagnitudes.shape[1]))), axis = 1)
                    alpha_RT_game.AlphaParticleMomentumMagnitudes = np.concatenate((_, PoolResult_AlphaRTGame_Particles[process][1]), axis = 0)

            
        # REFERENCES:
            # Python Software Foundation (2020). multiprocessing — Process-based parallelism, https://docs.python.org/3/library/multiprocessing.html.
            # 0612 TV w/ NERDfirst (2018). Python's Multiprocess Pool - Friday Minis 267, https://www.youtube.com/watch?v=WdorgAKWbns.
            # When Maths meets coding (2020). Multiprocessing in python complete tutorial, https://www.youtube.com/watch?v=rZ5CSsgv5hs.
            # Fayek, H (2020). Week 8 Optimization and Multiprocessing, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.
        
        ##########################################################################################################################
        # NOTE: Before multiprocessing
        # alpha_RT_game.process_Simulation(0)
        

        ### Output the results.
        alpha_RT_game.calculate_MaximumRange() # Calculate the maximum range.
        alpha_RT_game.calculate_DoseToMedium(BeamHeight, BeamWidth)
    
        print("Absorbed dose =", alpha_RT_game.AbsorbedDose, "Gy")

        alpha_RT_game.game_Outcome(DoseToDeposit_Gy)

        
        # Append the timing data from the methods used above.
        if __name__ == "__main__":
            # NOTE: Before multiprocessing ... However, there is still some code in this section that was not commented out.
            # timing_studies.append_TimingResults("AlphaParticles initialise_Simulation() (average)", np.array(timing_studies.initialise_Simulation_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles initialise_Simulation() (sum)", np.array(timing_studies.initialise_Simulation_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles randomNum_0to1() (average)", np.array(timing_studies.randomNum_0to1_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles randomNum_0to1() (sum)", np.array(timing_studies.randomNum_0to1_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticlePosition() (average)", np.array(timing_studies.update_AlphaParticlePosition_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticlePosition() (sum)", np.array(timing_studies.update_AlphaParticlePosition_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles record_AlphaParticlePosition() (average)", np.array(timing_studies.record_AlphaParticlePosition_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles record_AlphaParticlePosition() (sum)", np.array(timing_studies.record_AlphaParticlePosition_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles generate_RandomMatrix_Momentum() (average)", np.array(timing_studies.generate_RandomMatrix_Momentum_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles generate_RandomMatrix_Momentum() (sum)", np.array(timing_studies.generate_RandomMatrix_Momentum_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticleMomentum() (average)", np.array(timing_studies.update_AlphaParticleMomentum_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticleMomentum() (sum)", np.array(timing_studies.update_AlphaParticleMomentum_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaRTGame record_AlphaParticleMomentumMagnitude() (average)", np.array(timing_studies.record_AlphaParticleMomentumMagnitude_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaRTGame record_AlphaParticleMomentumMagnitude() (sum)", np.array(timing_studies.record_AlphaParticleMomentumMagnitude_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles update_ParticleNum() (average)", np.array(timing_studies.update_ParticleNum_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles update_ParticleNum() (sum)", np.array(timing_studies.update_ParticleNum_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles show_Progress() (average)", np.array(timing_studies.show_Progress_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles show_Progress() (sum)", np.array(timing_studies.show_Progress_List).sum(), "Sum")

            timing_studies.append_TimingResults("AlphaRTGame calculate_MaximumRange()", timing_studies.end_AlphaRTGame_calculate_MaximumRange - timing_studies.start_AlphaRTGame_calculate_MaximumRange, "Once")

            timing_studies.append_TimingResults("AlphaRTGame calculate_DoseToMedium()", timing_studies.end_AlphaRTGame_calculate_DoseToMedium - timing_studies.start_AlphaRTGame_calculate_DoseToMedium, "Once")

            timing_studies.append_TimingResults("AlphaRTGame game_Outcome()", timing_studies.end_AlphaRTGame_game_Outcome - timing_studies.start_AlphaRTGame_game_Outcome, "Once")

        return SimDistance_Option, SimInstances, timing_studies.ExecutionTime_main_SimDistance_Option_Input, timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input, timing_studies.ExecutionTime_program_admin_get_InputsForAlphaBeam, timing_studies.ExecutionTime_program_admin_get_InputsForMedium, timing_studies.ExecutionTime_main_SimInstances_Input, timing_studies.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input, timing_studies.ExecutionTime_main_AnalyseBeam_AppendTimingResults # These variables must be used outside of the main() function by the timing_studies object.
        
        
    elif SimDistance_Option in set(["q", "Q"]):
        print("You have chosen to do the beam attenuation quiz.\n")
        
        ### Describe the quiz to the user.
        program_admin.present_AttenuationQuizDetails()
        
        ### Prepare the quiz.
        ChosenMaterials_DF = program_admin.choose_MediaForAttenuationQuiz()
        InitialKineticEnergy, InitialParticleNumber, RandomDistribution = program_admin.choose_AlphaBeamCharacteristicsForAttenuationQuiz()
        SimInstances = 1

        AtomicNumber, AtomicWeight, MassDensity = 1, 1, 1 # Dummy variables just for letting the AttenuationQuiz class inherit the constructor of the AlphaParticles class. These variables are not needed in the AttenuationQuiz class.

        attenuation_quiz = AttenuationQuiz(InitialKineticEnergy, InitialParticleNumber, RandomDistribution, AtomicNumber, AtomicWeight, MassDensity, ChosenMaterials_DF)

        ### Ask the user the quiz question.
        # attenuation_quiz.ask_QuizQuestion(program_admin.get_ChosenMaterialName())
        attenuation_quiz.ask_QuizQuestion()
        
        ### Run the simulation and calculate the correct thickness needed to transmit the specified number of alpha particles.
        attenuation_quiz.process_Simulation(0)
        attenuation_quiz.calculate_Data() # The AttenuationQuiz class inherits the process_Simuation() method in the previous line. The AlphaParticles's class's calculate_Data() method was removed from its process_Simulation() method for implementing multiprocessing Pool. Thus, a separate class of the calculate_Data() method for the AttenuationQuiz class must be done.

        ### Tell the user the outcome of the quiz.
        attenuation_quiz.quiz_Outcome()

        ### Plot the number of alpha particles in the beam as a function of distance through the medium so the user can verify the outcome of the quiz.
        attenuation_quiz.plot_ParticleNum()
        print("Please check {} for a plot of the number of alpha particle remaining in the beam as a function of distance penetrated through the medium.".format(DirectoryToSaveTo))


        # Append the timing data from the methods used above.
        if __name__ == "__main__":
            # NOTE: Before multiprocessing ... However, there is still some code in this section that was not commented out.
            # timing_studies.append_TimingResults("AlphaParticles initialise_Simulation() (average)", np.array(timing_studies.initialise_Simulation_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles initialise_Simulation() (sum)", np.array(timing_studies.initialise_Simulation_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles randomNum_0to1() (average)", np.array(timing_studies.randomNum_0to1_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles randomNum_0to1() (sum)", np.array(timing_studies.randomNum_0to1_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticlePosition() (average)", np.array(timing_studies.update_AlphaParticlePosition_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticlePosition() (sum)", np.array(timing_studies.update_AlphaParticlePosition_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles record_AlphaParticlePosition() (average)", np.array(timing_studies.record_AlphaParticlePosition_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles record_AlphaParticlePosition() (sum)", np.array(timing_studies.record_AlphaParticlePosition_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles generate_RandomMatrix_Momentum() (average)", np.array(timing_studies.generate_RandomMatrix_Momentum_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles generate_RandomMatrix_Momentum() (sum)", np.array(timing_studies.generate_RandomMatrix_Momentum_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticleMomentum() (average)", np.array(timing_studies.update_AlphaParticleMomentum_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles update_AlphaParticleMomentum() (sum)", np.array(timing_studies.update_AlphaParticleMomentum_List).sum(), "Sum")
            
            # timing_studies.append_TimingResults("AlphaParticles update_ParticleNum() (average)", np.array(timing_studies.update_ParticleNum_List).mean(), "Average")
            # timing_studies.append_TimingResults("AlphaParticles update_ParticleNum() (sum)", np.array(timing_studies.update_ParticleNum_List).sum(), "Sum")
            
            timing_studies.append_TimingResults("AlphaParticles show_Progress() (average)", np.array(timing_studies.show_Progress_List).mean(), "Average")
            timing_studies.append_TimingResults("AlphaParticles show_Progress() (sum)", np.array(timing_studies.show_Progress_List).sum(), "Sum")

            timing_studies.append_TimingResults("AttenuationQuiz calculate_Data()", timing_studies.end_AttenuationQuiz_calculate_Data - timing_studies.start_AttenuationQuiz_calculate_Data, "Once")

        return SimDistance_Option, SimInstances, timing_studies.ExecutionTime_main_SimDistance_Option_Input, timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input, timing_studies.ExecutionTime_program_admin_get_InputsForAlphaBeam, timing_studies.ExecutionTime_program_admin_get_InputsForMedium, timing_studies.ExecutionTime_main_SimInstances_Input, timing_studies.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input, timing_studies.ExecutionTime_main_AnalyseBeam_AppendTimingResults # These variables must be used outside of the main() function by the timing_studies object.
                
        
if __name__ == "__main__": # This IF statement allows the program to be run by Python only if it is called by Python directly. The program will not run if it is called within another Python program.
    timing_studies.end_FunctionDefinition_main = time.time()
    timing_studies.append_TimingResults("main() function definition", timing_studies.end_FunctionDefinition_main - timing_studies.start_FunctionDefinition_main, "Once")
    
    timing_studies.start_main = time.time()
    # NOTE: The main() function is called in the next line.
    SimDistance_Option, SimInstances, timing_studies.ExecutionTime_main_SimDistance_Option_Input, timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input, timing_studies.ExecutionTime_program_admin_get_InputsForAlphaBeam, timing_studies.ExecutionTime_program_admin_get_InputsForMedium, timing_studies.ExecutionTime_main_SimInstances_Input, timing_studies.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input, timing_studies.ExecutionTime_main_AnalyseBeam_AppendTimingResults = main() # The SimInstances variable must be used by the timing_studies object, which is outside of the main() funciton. Here is where code actually starts to be *executed*. The key to running the program is that the program's __name__ must be "__main__".
    timing_studies.end_main = time.time()
    timing_studies.ExecutionTime_main = (timing_studies.end_main - timing_studies.start_main) - np.array([timing_studies.ExecutionTime_main_SimDistance_Option_Input, timing_studies.ExecutionTime_main_WhetherOrNotReadInputsFromFile_Input, timing_studies.ExecutionTime_program_admin_get_InputsForAlphaBeam, timing_studies.ExecutionTime_program_admin_get_InputsForMedium, timing_studies.ExecutionTime_main_SimInstances_Input, timing_studies.ExecutionTime_statistical_analyser_plot_RandomMatrixOffDiagonals_All_HistogramBins_Input, timing_studies.ExecutionTime_main_AnalyseBeam_AppendTimingResults]).sum() # Use np.array([]).sum() instead of typing a + b + c + ....
    
    if SimDistance_Option in set(["a", "A", "g", "G"]): # Neither optimisation nor multiprocessing was done for the attenuation quiz directly. Any optimisation for the attenuation quiz was a result of optimisations done to the beam analysis mode.
        print()
        print("Execution time of the program minus the time spent waiting for user inputs =", timing_studies.ExecutionTime_main, "s")
        print()

    
    if SimDistance_Option in set(["a", "A"]): # Each mode has its own timers.
        timing_studies.calculate_NumberOfTimeExecuted_All_BeamAnalysis()
    
    elif SimDistance_Option in set(["g", "G"]):
        timing_studies.calculate_NumberOfTimeExecuted_All_RTGame()

    elif SimDistance_Option in set(["q", "Q"]): # I may optimise the attenuation quiz mode in a future version of the program.
        timing_studies.calculate_NumberOfTimeExecuted_All_AttenuationQuiz()
    
    timing_studies.calculate_AverageTotalExecutionTimePerSimInstance(SimInstances)
    timing_studies.export_TimingResults()
    timing_studies.export_TimingResults_ParticularLines()

    print("The simulation is done! Please check the outputted files. They are in a folder named {} in the same directory as the program file.".format(DirectoryToSaveTo)) # This message must be the last message to be shown. Thus, it is placed here in the script rather than in one of the methods in the AlphaParticles class.
   
    # REFERENCES:
        # the pandas development team (2014). pandas.DataFrame.to_csv, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html.

elif __name__ == os.path.basename(__file__).replace(".py", ""): # Do not let Python confuse when the user tries to import AlphaParticles2.py and when multiprocessing Pool is being done. os.path.basename(__file__).replace(".py", "") instead of "AlphaParticles2_Main" is used here so that the if statement's condition does not have to be changed if the script file's name is changed.
    print("Error: This program is not supposed to be run in another program. Please run it directly rather than importing it.") # If the user tries to call the program within another Python program, they must know why they cannot run the program. In this case, the __name__ of the program is "AlphaParticles2", because that is the value of AlphaParticles.__name__ in the Python shell in the command terminal. It is the name of the file minus its extension.

# REFERENCES:
    # Zelle, J M (2017). Python Programming: An Introduction to Computer Science, 3rd ed. 2154 NE Broadway, Suite 100, Portland, Oregon 97232: Franklin, Beedle & Associates Inc.
    # Programiz. Python Exception Handling Using try, except and finally statement. Retrieved from https://www.programiz.com/python-programming/exception-handling
    # Sven Marnach (2010). Get name of current script in Python, https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python.