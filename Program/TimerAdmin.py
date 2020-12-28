######################################################################################################################
# The Alpha Particles 2.0 project was made by Kyrollos Iskandar.
######################################################################################################################

####################################### Notes about this program #########################################
# NOTE: This program was used for timing the execution of particular sections and lines of code in an attempt to optimise the program in terms of its runtime. All of its method calls in the AlphaParticles2_Main.py script worked successfully before multiprocessing was implemented. Now, only the method calls that are still outside multiprocessing sections work successfully. However, this is not a problem because the Alpha Particles 2.0 program still runs successfully. The TimerAdmin.py script is now mainly for record.
# This program is meant to be run by the Alpha Particles 2.0 program. It is not supposed to be run directly, hence the if __name__ == "__main__" code block at the start of the script.
##########################################################################################################
if __name__ == "__main__": # This statement is put at the start of the script so that no time and resources are spent defining classes and functions when not needed.
    print("Error: The TimerAdmin program is supposed to be imported into the Alpha Particles 2.0 program and run inside it.")
    exit() # The exit() function prevents the code below from being run in the case where the script is run directly.


# Below are the modules that the TimerAdmin program needs.
import pandas as pd

# REFERENCES:
    # the pandas development team. (2020). pandas. pandas. Retrieved from https://pandas.pydata.org/

class TimingStudies: # This class is not actually part of the program in terms of the program's purpose. It is for managing timing experiments for optimising the program.
    def __init__(self, DirectoryToSaveTo, timestamp):
        self.DirectoryToSaveTo = DirectoryToSaveTo
        self.timestamp = timestamp
        
        self.TimingsDict = {"Description" : [], "Execution time (end - start) /s" : [], "Measurement type" : [], "Number of times executed" : [], "Average total execution time per simulation instance /s" : []} # Initialise a table for recording execution times of methods. This dictionary is to be exported as a CSV file via becoming a pandas DataFrame. Data is to be appended to the lists in the dictionary. All of the appending is to be done at the end of each group of time.time() calls, or even at the end of the program file, to avoid appending data in the wrong order. Dictionaries keep things together, which is good for keeping things organised.
        self.TimingsDict_ParticularLines = {"Description" : [], "Execution time (end - start) /s" : []} # This dictionary is for the timing results of particular lines of code.

        # Initialise lists for collecting timing data for methods and other code that is executed multiple times per run of the program.
        self.initialise_Simulation_List = []
        self.randomNum_0to1_List = []
        self.update_AlphaParticlePosition_List = [] # ... for measuring the average execution time of the update_AlphaParticlePosition() method in the AlphaParticles class.
        self.record_AlphaParticlePosition_List = []
        self.generate_RandomMatrix_Momentum_List = []
        self.update_AlphaParticleMomentum_List = []
        self.record_AlphaParticleMomentumMagnitude_List = []
        self.update_ParticleNum_List = []
        self.show_Progress_List = []
        self.calculate_Data_List = []
        self.get_Results_List = []
        self.StatAnalysis_calculate_and_get_Average_List = []
        self.StatAnalysis_calculate_and_get_PopulationStandardDeviation_List = []
        self.AlphaRTGame_show_Progress_List = []

        # Initialise lists for collecting timing data for particular lines of code.
        self.update_ParticleNum_MomentumMagnitudeCalculation_List = []
        self.update_ParticleNum_NumpyArrayMask_List = []

        self.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_MakePlot_List = []
        self.StatisticalAnalysis_plot_RandomMatrixOffDiagonals_Plot_ExportPlot_List = []


    def append_TimingResults(self, Description, ExecutionTime, MeasurementType): # ... for appending the timing results to TimingsDict, which is the main display of the timings results.
        self.TimingsDict["Description"].append(Description)
        self.TimingsDict["Execution time (end - start) /s"].append(ExecutionTime)
        self.TimingsDict["Measurement type"].append(MeasurementType)

    
    def append_TimingResults_ParticularLines(self, Description, ExecutionTime): # ... for appending the timing results to TimingsDict, which is the main display of the timings results.
        self.TimingsDict_ParticularLines["Description"].append(Description)
        self.TimingsDict_ParticularLines["Execution time (end - start) /s"].append(ExecutionTime)


    def calculate_NumberOfTimeExecuted(self, Description_Sum, Description_Average):
        if Description_Sum in self.TimingsDict["Description"]: # It is not guaranteed that the code for which the number of times it has been executed is to be calculated has been profiled. The code for which this is not guaranteed to happen is the code that is executed within multiprocessing Pool processes.
            self.IndexForCalculation = self.TimingsDict["Description"].index(Description_Sum)
        
            try:
                self.TimingsDict["Number of times executed"][self.IndexForCalculation] = (self.TimingsDict["Execution time (end - start) /s"][self.IndexForCalculation]) / (self.TimingsDict["Execution time (end - start) /s"][self.TimingsDict["Description"].index(Description_Average)])
            
            except RuntimeWarning:
                print("Warning: At least one division by 0 occurred when calculating the number of times some code was executed. This happened because the average execution time of that code was so quick that Python approximated it to 0.0 s. This code is insignificant in terms of efforts to optimise the program.")
            
            except:
                print("Some other error occurred when trying to calculate the number of times some code was executed.")

    
    def calculate_NumberOfTimeExecuted_All_BeamAnalysis(self):
        self.TimingsDict["Number of times executed"] = [1] * len(self.TimingsDict["Description"]) # Initialise the list. 1 execution time is standard.

        self.calculate_NumberOfTimeExecuted("AlphaParticles initialise_Simulation() (sum)", "AlphaParticles initialise_Simulation() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles randomNum_0to1() (sum)", "AlphaParticles randomNum_0to1() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_AlphaParticlePosition() (sum)", "AlphaParticles update_AlphaParticlePosition() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles record_AlphaParticlePosition() (sum)", "AlphaParticles record_AlphaParticlePosition() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles generate_RandomMatrix_Momentum() (sum)", "AlphaParticles generate_RandomMatrix_Momentum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_AlphaParticleMomentum() (sum)", "AlphaParticles update_AlphaParticleMomentum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_ParticleNum() (sum)", "AlphaParticles update_ParticleNum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles show_Progress() (sum)", "AlphaParticles show_Progress() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles calculate_Data() (sum)", "AlphaParticles calculate_Data() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles get_Results() (sum)", "AlphaParticles get_Results() (average)")
        self.calculate_NumberOfTimeExecuted("StatisticalAnalysis calculate_and_get_Average() (sum)", "StatisticalAnalysis calculate_and_get_Average() (average)")
        self.calculate_NumberOfTimeExecuted("StatisticalAnalysis calculate_and_get_PopulationStandardDeviation() (sum)", "StatisticalAnalysis calculate_and_get_PopulationStandardDeviation() (average)")

    
    def calculate_NumberOfTimeExecuted_All_RTGame(self):
        self.TimingsDict["Number of times executed"] = [1] * len(self.TimingsDict["Description"]) # Initialise the list. 1 execution time is standard.

        self.calculate_NumberOfTimeExecuted("AlphaParticles initialise_Simulation() (sum)", "AlphaParticles initialise_Simulation() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles randomNum_0to1() (sum)", "AlphaParticles randomNum_0to1() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_AlphaParticlePosition() (sum)", "AlphaParticles update_AlphaParticlePosition() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles record_AlphaParticlePosition() (sum)", "AlphaParticles record_AlphaParticlePosition() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles generate_RandomMatrix_Momentum() (sum)", "AlphaParticles generate_RandomMatrix_Momentum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_AlphaParticleMomentum() (sum)", "AlphaParticles update_AlphaParticleMomentum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_ParticleNum() (sum)", "AlphaParticles update_ParticleNum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles show_Progress() (sum)", "AlphaParticles show_Progress() (average)")
        

    def calculate_NumberOfTimeExecuted_All_AttenuationQuiz(self):
        self.TimingsDict["Number of times executed"] = [1] * len(self.TimingsDict["Description"]) # Initialise the list. 1 execution time is standard.

        self.calculate_NumberOfTimeExecuted("AlphaParticles initialise_Simulation() (sum)", "AlphaParticles initialise_Simulation() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles randomNum_0to1() (sum)", "AlphaParticles randomNum_0to1() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_AlphaParticlePosition() (sum)", "AlphaParticles update_AlphaParticlePosition() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles record_AlphaParticlePosition() (sum)", "AlphaParticles record_AlphaParticlePosition() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles generate_RandomMatrix_Momentum() (sum)", "AlphaParticles generate_RandomMatrix_Momentum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_AlphaParticleMomentum() (sum)", "AlphaParticles update_AlphaParticleMomentum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles update_ParticleNum() (sum)", "AlphaParticles update_ParticleNum() (average)")
        self.calculate_NumberOfTimeExecuted("AlphaParticles show_Progress() (sum)", "AlphaParticles show_Progress() (average)")
        
    
    def calculate_AverageTotalExecutionTimePerSimInstance(self, SimInstances):
        self.TimingsDict["Average total execution time per simulation instance /s"] = [0.0] * len(self.TimingsDict["Description"]) # Initialise the list. 0.0 is a placeholder.

        for row in range(0, len(self.TimingsDict["Description"])):
            if self.TimingsDict["Measurement type"][row] == "Sum":
                self.TimingsDict["Average total execution time per simulation instance /s"][row] = self.TimingsDict["Execution time (end - start) /s"][row] / SimInstances
            
            elif self.TimingsDict["Measurement type"][row] in set(["Average", "Once"]):
                self.TimingsDict["Average total execution time per simulation instance /s"][row] = "N/A"
    
    
    def export_TimingResults(self): # Show me the results of the timing experiments. If the user is interested to see them, they can, too. We are going to export the results of the timing experiments to a CSV file.
        self.TimingsDF = pd.DataFrame(self.TimingsDict) # A pandas DataFrame can be exported as a CSV file. It is also easy to sort values in it like how rows are sorted in Microsoft Excel based on the values in one of the columns. See the sort_values() method of pandas DataFrames below.
        self.TimingsDF.sort_values(by = "Execution time (end - start) /s", axis = 0, ascending = False, kind = "mergesort", inplace = True) # Sort the execution times in descending order. Not sorting the indices means that we preserve the information about the order in which the methods were executed. mergesort was mentioned to be the only stable sorting algorithm, and it was suitable for sorting by one column, so I used it.
        self.TimingsDF.to_csv("{}TimingResults_{}.csv".format(self.DirectoryToSaveTo, self.timestamp)) # Name the file according to the timestamp of the run of the program so that all of the files that the program outputs are in one place.


    def export_TimingResults_ParticularLines(self): # Show me the results of the timing experiments for particular lines of code.
        self.TimingsDF_ParticularLines = pd.DataFrame(self.TimingsDict_ParticularLines)
        self.TimingsDF_ParticularLines.sort_values(by = "Execution time (end - start) /s", axis = 0, ascending = False, kind = "mergesort", inplace = True)
        self.TimingsDF_ParticularLines.to_csv("{}TimingResultsForParticularLines_{}.csv".format(self.DirectoryToSaveTo, self.timestamp))

    # REFERENCES:
        # the pandas development team (2014). pandas.DataFrame.sort_values, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html.
        # Fayek, H (2020). Week 2 Data Types, 124 La Trobe St, Melbourne VIC 3000: Haytham Fayek.