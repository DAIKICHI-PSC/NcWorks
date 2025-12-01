# NcWorks
NC PROGRAM EDITOR, 2D SIMULATOR AND 2D CADCAM FOR SWISS-TYPE LATHE

[Overview]  
This program provides an editor, 2D simulator, and 2D CAD/CAM software for automatic lathes (Swiss-type lathes).  
Visually creating and checking programs will contribute to significant time (cost) savings.  
We created this program because commercially available CAD/CAM software is expensive and cannot simulate NC code.  
It only supports the XZ plane.  
Use it to standardize NC programs.  
  
[2D Simulator]  
Since it allows you to visually check NC programs, it is ideal for training new employees and preventing errors.  
The workflow is as follows:  
1. Create a program  
2. Create a cutting tool if one does not already exist (see the DXF file in [sample_tools] for reference).  
3. Register the cutting tool in the 2D simulator (only the first time for each program).  
4. Specify the material diameter in the 2D simulator (only the first time for each program).  
5. Set the [Display] and [Execution Speed] as needed, click the [Start] button to start the simulator, and then click the [Next] button to run the simulator (uncheck [Single Block] for fully automatic execution).  
6. After the simulation is complete, you can perform simple dimension measurements.  
Load the program from the [sample] folder in the editor and test it (the above settings are already configured).  
For internal machining tools such as drills, specify X0.  
General linear interpolation and R interpolation are implemented.  
G50 is also implemented.  
Cutting edge R compensation is not implemented.  
  
[2D CAD/CAM]  
Since it allows you to create NC programs visually, it is ideal for training new employees and preventing errors.  
Convert DXF files of tool paths drawn in CAD into NC programs.  
Draw each tool path on a separate [Layer] (a layer number is required).  
Draw a [CIRCLE] at the starting point (diameter does not matter).  
Movements within the same coordinate system cannot be converted (basically, draw in one stroke).  
Normally, you should select "No" when asked "Is the line data drawn in one stroke?"  
This has been confirmed with [Zounou CAD RAPID 2D] (although I haven't confirmed it, I think the free software JW_CAD can also be used).  
  
[File Description]  
sample folder: Contains the NC program [sample_NC_program.m] and settings file  
sample_cam folder: Contains sample CAD data for CADCAM [sample_CAM_file.dxf]  
sample_tools folder: Contains tool data (DXF) for the 2D simulator  
GUI_DXFtoNC.py: GUI program for 2D CADCAM (Python program)  
GUI_DXFtoNC.ui: GUI creation file (for QT Designer)  
GUI_EDITOR.py: GUI program for the editor (Python program)  
GUI_EDITOR.ui: GUI creation file (for QT Designer)  
GUI_SIM.py: GUI program for the 2D simulator (Python program)  
GUI_SIM.ui: GUI creation file (for QT Designer)  
NcWorks.py: Main program  
PLANET.ico: Icon file  
README.txt: Main file  
SETTINGS_DXFtoNC.ini: Settings file for CADCAM (normally generated automatically)  
SETTINGS_EDITOR.ini Editor settings file (normally generated automatically)  
SETTINGS_SIM.ini 2D simulator settings file (normally generated automatically)  
Sub_MathPlus.py Calculation module  
Sub_NcTools.py Calculation module  

