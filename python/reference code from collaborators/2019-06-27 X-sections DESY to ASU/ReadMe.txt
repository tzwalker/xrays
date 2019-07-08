This ReadMe was written by Christina Ossig on the 14.06.2019
The Data and scripts in these folders are confidential.

The ReadMe regards the cross section data taken at the ESRF in March 2018.
The Data has been processed and the original edf files have been fitted (XRF, and converted to cts/s) and converted (XBIC, ampere), finally they have been saved in a csv format and been plotted as PNG and SVG files.
The Data in the csv files is stored as a Matrix, where each field corresponds to a pixel in the map.
Furthermore is there one Metadata.csv file with information, like the size of the map, pixelnumbers, stepsize etc.
For each Scan the processed Data can be found in the Sample subfolder, which contains the folder ProcessedData.

An overview is presented in the PowerPoint presentation, CrossSectionsofCdTeSolarcells.pptx.

The list of taken scans per sample is listed here:
SampleName Scannumber
CdTe_X_TS58A 2
CdTe_X_TS58A 3
CdTe_X_TS58A 4
CdTe_X_TS58A 5
CdTe_X_NBL31 1
CdTe_X_NBL31 6
CdTe_X_NBL31 7
CdTe_X_NBL31 8
CdTe_X_NBL33 1
CdTe_X_NBL33 2
CdTe_X_NBL33 12
CdTe_X_NBL33 13
CdTe_X_NBL33 14
CdTe_X_NBL33 15
CdTe_X_NBL33 17
CdTe_X_NBL33 20


The current structure of the folders is as follows:
first layer: Python Scripts, Input File, align.spec, ReadMe, and the three Sample Folders,
Sample Folder: It contains two folders called: ProcessedData and RawData
						In ProcessedData all the output from the Python scripts is dumped.
						RawData holds the Raw XBIC data in one folder, for each scan one folder with the fluorescence data, and the configuration file for batchfitting the fluorescence data in PyMCA
						The Fluorescence Data has two subfolders, one containing the raw Fluorescence Data (Which is a summation of the data from three elements of the detector) and a folder with the output images of a PyMCA batchfit of the raw Fluo data with the aforementioned config file

-------------------- 

For those interested, the raw data is also saved for each Sample in a folder called RawData. There a config file is present, which has been used to fit the raw fluorescence data in PyMCA. A folder containing the already fitted Images is also stored in the RawData folder.

The postprocessing is done with python (Version 2.7).

The core programs for the postprocessing are: PackageDeal_XBIC_Fluo_Meta_function.py, which is the callable version of PackageDeal_XBIC_Fluo_Meta.py (the latter is the alternative which can be used alone).
These two programs are essentially the same. They read in the raw, or preprocessed (in case of Fluorescence Data) data and convert them to their SI units as well as plotting them. Additionally the not as easy readable edf files are transcripted into csv files.

To get them to run, you need to make sure that the align.spec file is in the same folder and that the paths hardcoded in the program are the correct ones (paths for where to load the data from or where to save the data to).

When just one Scan should be processed use: python2.7 PackageDeal_XBIC_Fluo_Meta.py 'SampleName' Scannumber 
as Terminal line

For processing more than one scan use the program called "WholeDeal.py".
WholeDeal.py needs an input file in the same folder: A sample input file is "Wrapping_input.txt".
The structure of the input file is similar to the listing of the Sample and RunNumber further up, without naming the columns. Make sure that no empty line is in the file.
Furthermore the __init__.py file has to be in the folder, to allow the import of PackageDeal_XBIC_Fluo_Meta_function.py into the program.

WholeDeal.py is used to loop over all the scans in the input file and execute the program "PackageDeal_XBIC_Fluo_Meta_function.py"
When using the WholeDeal.py the terminal will be updated with what it is doing currently. This is not done when using the PackageDeal_XBIC_Fluo_Meta.py


