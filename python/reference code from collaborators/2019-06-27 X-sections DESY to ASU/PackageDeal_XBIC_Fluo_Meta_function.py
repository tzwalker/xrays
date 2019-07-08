import fabio # for opening edf files
import numpy as np #for writing arrays
import math #for using square root
import csv #for writing the csv and reading them
import matplotlib as mpl
import matplotlib.pyplot as plt #for plotting the stuff
import os	#for working with paths 
import re	#for using regular expressions
import glob #for opening all files in a directory
import sys	#for getting Arguments when starting the script




def wrapping(SampleName,RunNumber):
	""" -----------------------Hardcoded, where the data is or where it is going----------------------"""
	#Places where the files are located, and where they shall be saved for XBIC:
	beam_dir='/asap3/petra3/gpfs/external/2018/data/50000209/processed/Crosssection_Fluo_and_XBIC/'
	sample_dir=SampleName
	Run= int(RunNumber)
	savedir='/asap3/petra3/gpfs/external/2018/data/50000209/processed/Crosssection_Fluo_and_XBIC/'+sample_dir+'/ProcessedData/'
	print 'This is sample: '+sample_dir
	print 'Currently processing Scan number: '+str(Run)
	
	
	
	
	
	#Name of the direct and lock-in amplified XBIC files:
	I0_name='_zap_p201_I0_'
	XBIC_name='_zap_p201_Xbic_'
	
	
	#Places where the files are located for Fluorescence:
	if sample_dir == 'CdTe_X_TS58A':
		f_image_dir = sample_dir+'/RawData/Scan'+str(Run)+'/Batchfitted_IMAGES_TS58A_20190309_config/' #The last part of the name, is also describing, which config file was used to fit the Fluorescence data
	elif sample_dir == 'CdTe_X_NBL33':
		f_image_dir = sample_dir+'/RawData/Scan'+str(Run)+'/Batchfitted_IMAGES_TS58A_20190309_config/'
	elif sample_dir == 'CdTe_X_NBL31':
		f_image_dir = sample_dir+'/RawData/Scan'+str(Run)+'/Batchfitted_IMAGES_TS58A_vom9March_background_angepasst_config/'
	
	
	
	
		
	
	#Metadata, and Run numbers (hardcoded)
	xbicS=10
	ioS=1
	Scale=10
	C_Range=10
	S_Range=50e06
	
	#Necessary Metadata for identifying the other metadata, first in the tuple is absolute scannumber, second is amplification value
	dict_CdTe_X_TS58A={'Run_2': (853,200e-09), 'Run_3': (854,200e-09),'Run_4': (855,200e-09),'Run_5': (856,200e-09)}
	dict_CdTe_X_NBL31={'Run_1': (857,200e-09), 'Run_6': (862,500e-09),'Run_7': (863,500e-09),'Run_8': (864,500e-09)}
	dict_CdTe_X_NBL33={'Run_1': (865,200e-09), 'Run_2': (866,200e-09),'Run_12': (876,200e-09),'Run_13': (877,200e-09),'Run_14': (882,200e-09), 'Run_15': (883,200e-09),'Run_17': (885,200e-09),'Run_20': (888,200e-09)}
	
	#Selecting Metadata for current scan:
	if sample_dir == 'CdTe_X_TS58A':
		key= 'Run_'+str(Run)
		values=dict_CdTe_X_TS58A.get(key,('There is no key'))
		absScan=values[0]
		Amp=values[1]
	elif sample_dir == 'CdTe_X_NBL33':
		key= 'Run_'+str(Run)
		values=dict_CdTe_X_NBL33.get(key,(0))
		absScan=values[0]
		Amp=values[1]
	elif sample_dir == 'CdTe_X_NBL31':
		key= 'Run_'+str(Run)
		values=dict_CdTe_X_NBL31.get(key,(0))
		absScan=values[0]
		Amp=values[1]
	
	pattern=re.compile('#S '+str(absScan) + '(.*)$')
	with open('align.spec') as a:
		for line in a:
			match=pattern.match(line)
			if match is not None:
				scanorder = line
	
	S_Befehl=scanorder.split()
	#Defining the necessary Metadata
	x_len=float(S_Befehl[5])-float(S_Befehl[4])
	y_len=float(S_Befehl[10])-float(S_Befehl[9])
	dwell=float(S_Befehl[7])/1000 #The divided by 1000 is to go from ms to s
	x_size=int(S_Befehl[6])
	y_size=int(S_Befehl[11])+1
	x_step=x_len/float(x_size)
	y_step=y_len/float(y_size)
	dnorm=1/dwell # Faktor um die counts auf 1 sekunde dwelltime zu normieren
	
				
	"""-----------------------------------------------------------------------"""
	
	"""
	How to convert from the numbers to a current
	Source    --> Current to Voltage Amplifier --> Lock-in Scaling -->    V2F converter     -->                      Recorded Signal
	Signal(nA)  /      Amplification(A/V)      *   Scaling (V/V)   /  Converter Range(V)    *  Range of Signal (Hz) = VALUE (Hz)
	
	Signal = Val(Hz)/Range(Hz)*Range(V)/Scaling(V/V)*Amplification(nA/V)
	"""
	def Hz2nALI(data,Amp=Amp,Scale=Scale,C_Range=C_Range,S_Range=S_Range,dnorm=dnorm): # The factor 2*sqrt(2) is due to the RMS which we output
		ConFactor=C_Range*Amp*2*math.sqrt(2)/(S_Range*Scale)*dnorm
		data.data=data.data*ConFactor
		return np.array(data.data)
	
	def Hz2nADirect(data,Amp=Amp,Scale=Scale,C_Range=C_Range,S_Range=S_Range,dnorm=dnorm):  #Direct but fed through the lock-in amplifier with very high low pass filter
		ConFactor=C_Range*Amp/(S_Range*Scale*math.sqrt(2))*dnorm    #the division by sqrt(2) is because we still output an RMS but actually do no lock-in amplification
		data.data=data.data*ConFactor
		return np.array(data.data)	
	"""
	Displaying or Saving of Data
	"""
	def showimage(im,cmap,xlab,ylab,clab,fil): 
		plt.imshow(im,interpolation=fil, cmap=cmap, alpha=1., extent=[0,x_len,0,y_len],origin='upper')
		plt.xlabel(xlab)
		plt.ylabel(ylab)
		cbar =plt.colorbar()
		cbar.ax.set_ylabel(clab)
		plt.show()
		
	def saveimage(im,cmap,xlab,ylab,clab,fil,name): 
		plt.imshow(im,interpolation=fil, cmap=cmap, alpha=1., extent=[0,x_len,0,y_len],origin='upper')
		plt.xlabel(xlab)
		plt.ylabel(ylab)
		cbar =plt.colorbar()
		cbar.ax.set_ylabel(clab)
		plt.savefig(savedir+name+'.svg',dpi=400)
		plt.savefig(savedir+name+'.png',dpi=400)
		plt.close()
		
	def saveMetadata(x_size=x_size,x_step=x_step,y_size=y_size,y_step=y_step,amp=Amp,xbicS=xbicS,ioS=ioS,dwell=dwell,Run=Run):
		MetaDaten = {'area_size (um,um)' : str(x_len)+'x'+str(y_len), 'ystep (um)': y_step, 'xstep (um)' : x_step, 'y_size (pixel Number)':y_size, 'x_size (pixel Number)': x_size, 'amplification (A/V)' : amp, 'XBIC_lockin_scaling' : xbicS , 'XBIC_direct_scaling': ioS, 'dwelltime (s)': dwell}
		w = csv.writer(open(savedir+sample_dir+'_Scan_'+str(Run)+'_'+"Metadata.csv", "w"))
		for key, val in MetaDaten.items():
			w.writerow([key, val])
			
			
	def saveData(daten, name):
		np.savetxt(savedir+sample_dir+'_Scan_'+str(Run)+name+'_data.csv', daten, delimiter = ',')	
	
	"""----------------------------------------------------------------"""
	"""--------------------- XBIC Data --------------------------------"""
	
	"""
	Loading in of Data for direct (named I0) or lock-in amplified (named Xbic) XBIC conversion
	"""
	
	I0_raw=fabio.open(beam_dir+sample_dir+"/RawData/XBIC/"+sample_dir+I0_name+str(Run).zfill(4)+'_0000.edf')
	Xbic_raw=fabio.open(beam_dir+sample_dir+"/RawData/XBIC/"+sample_dir+XBIC_name+str(Run).zfill(4)+'_0000.edf')
	print "Loading of XBIC data"
	
	#y_size,x_size = np.shape(I0_raw.data)
	
	"""
	Conversion of Data
	"""
	I0_con=Hz2nADirect(I0_raw,Scale=ioS)
	Xbic_con=Hz2nALI(Xbic_raw,Scale=xbicS)
	print "Conversion of counts to ampere"
	"""-----------------------Fluorescence Data ----------------------------"""
	
	directory = f_image_dir
	
	for file in os.listdir(directory):
		filename = str(file)
		if filename.endswith(".edf"): 
			fpath=os.path.join(directory, filename)
			fdata=fabio.open(fpath)
			imdata=np.array(fdata.data)*dnorm
			naming=str(filename)
			naming1=naming.replace('.','_')
			components=naming1.split('_')
			saveimage(imdata,'viridis','$X$ Position ($\mu$m)','$Y$ Position ($\mu$m)', 'Countrate (cts/s)','None',sample_dir+'_Scan_'+str(Run)+'_'+components[9]+'_'+components[10])
			print 'Saved svg and png of Fluorescence Channel: '+components[9]+'_'+components[10]
			saveData(imdata,'_'+components[9]+'_'+components[10])
			print 'Saved csv of Fluorescence Channel: '+components[9]+'_'+components[10]
		

	
	############################
	
	saveMetadata()
	print 'Saved Metadata'
	saveData(I0_con, '_XBIC_direct')
	print 'Saved direct XBIC data'
	saveData(Xbic_con, '_XBIC_lockin')
	print 'Saved lock-in XBIC data'
	
	saveimage(I0_con,'inferno','$X$ Position ($\mu$m)','$Y$ Position ($\mu$m)','Signal (A)','None',sample_dir+'_Scan_'+str(Run)+'_XBIC_direct')
	saveimage(Xbic_con,'inferno','$X$ Position ($\mu$m)','$Y$ Position ($\mu$m)','Signal (A)','None',sample_dir+'_Scan_'+str(Run)+'_XBIC_lockin')
	print 'Saved XBIC images'
	
