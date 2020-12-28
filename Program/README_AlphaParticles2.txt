### Readme for AlphaParticles2_Main.py ###
Author: Kyrollos Iskandar

The Alpha Particles 2.0 project was designed to be run on Windows 10. There is no guarantee that it will work on other operating systems.

Please run AlphaParticles2_Main.py via the command terminal.
First navigate to the directory in which the program file is and call it with Python. For Windows 10, type and ENTER python AlphaParticles2_Main.py

### Disclaimer ###
The program may not give correct answers. Please see Section 4 of the documentation for more information.


### Required software for running the program ###
This program uses Python 3.8.5.
Please also make sure you have the following Python standard libraries and external modules installed correctly before running the program:

Standard libraries:
> math
> statistics
> datetime
> os
> sys
> random
> multiprocessing
> time

External modules:
> numpy v1.19.1
> matplotlib v3.3.1
> pandas v1.1.1
> psutil v5.7.2


### Required script files ###
> TimerAdmin.py


### Required input files ###
> AttenuationQuiz_MaterialLibrary.csv
> InputsForBeamAnalysis.txt
> InputsForRTGame.txt
> InputsForAttenuationQuiz.txt


### Other information about files ###
> With the ExcelMacros.xlsm file open, press Ctrl + Shift + E to quickly format the Tables in the CSV files of the timing experiments. Please make sure that this file is the only macro-enabled Microsoft Excel file you have open.


### Information about the AlphaParticles2_Main.py script ###
The code that I had used before optimising the script and implementing multiprocessing has been kept in commented form for record. The code that is not commented out is optimised for runtime and has multiprocessing implemented where appropriate.