import time, os, csv, pyodbc, numpy, pandas, shutil, glob, re, wx
from scipy import sparse
import Tkinter as tk
import tkFileDialog as tkFD

def get_run_params(runnum,fullrunnum,rundate):
	foundfile=False
	runparams={}
	rundate=str(rundate)
	rootexpdir="Y:\Experiment Summaries\Year 20" + rundate[:2] + "\\"
	currentdir=rootexpdir+"S00" + str(runnum)+'\\'
	for f in glob.iglob(currentdir + 'MC03 Checklist-'+str(rundate)+'*'+str(fullrunnum)+'*.xlsx'):
		if os.path.isfile(f):
			foundfile=True
			print 'found file: ', f
			if re.search('\d\d-*\d\d-*\d\d',f).group(0)==rundate:	
				DWstart=float(re.search('-[DW]*\s*(\d+)\s*(to|-+)\s*(\d+)',f).group(1))
				DWend=float(re.search('-[DW]*\s*(\d+)\s*(to|-+)\s*(\d+)',f).group(3))
				print 'detected DW start: ', DWstart
				print 'detected DW end: ', DWend
				runparams['DWstart']=DWstart
				runparams['DWend']=DWend
				if DWstart>DWend:
					runparams['DWmax']=DWstart
					runparams['DWmin']=DWend
					runparams['processforward']=False
				else:
					runparams['DWmax']=DWend
					runparams['DWmin']=DWstart
					runparams['processforward']=True
	currentdir="Y:\Experiment Summaries\MC03\\"
	for f in glob.iglob(currentdir + 'MC03 Checklist-'+str(rundate)+'*'+str(fullrunnum)+'*.xlsx'):
		if os.path.isfile(f):
			foundfile=True
			print 'found file: ', f
			if re.search('\d\d-*\d\d-*\d\d',f).group(0)==rundate:	
				DWstart=float(re.search('-[DW]*\s*(\d+)\s*(to|-+)\s*(\d+)',f).group(1))
				DWend=float(re.search('-[DW]*\s*(\d+)\s*(to|-+)\s*(\d+)',f).group(3))
				print 'detected DW start: ', DWstart
				print 'detected DW end: ', DWend
				runparams['DWstart']=DWstart
				runparams['DWend']=DWend
				if DWstart>DWend:
					runparams['DWmax']=DWstart
					runparams['DWmin']=DWend
					runparams['processforward']=False
				else:
					runparams['DWmax']=DWend
					runparams['DWmin']=DWstart
					runparams['processforward']=True
	if not foundfile:
		print 'Could not find excel report file.  You need to enter DW positions by hand.'
		runparams['DWstart']=float(input('enter downweb starting position: '))
		runparams['DWend']=float(input('enter downweb ending position: '))
		if runparams['DWstart']>runparams['DWend']:
			runparams['DWmax']=runparams['DWstart']
			runparams['DWmin']=runparams['DWend']
			runparams['processforward']=False
		else:
			runparams['DWmax']=runparams['DWend']
			runparams['DWmin']=runparams['DWstart']
			runparams['processforward']=True
					
	return runparams


fullrunnumber=raw_input('enter run number (i.e. 365)')
runnumber=fullrunnumber[:3]

addSaveLabel=''
if re.search('R',fullrunnumber,re.IGNORECASE) or re.search('L',fullrunnumber,re.IGNORECASE):
	addSaveLabel = fullrunnumber + ' - ' 

try:
	todaysdate=input('for previous data, enter date as YYMMDD (otherwise defaults to today): ')
	todaysdate=str(todaysdate)
except SyntaxError:
	todaysdate=time.strftime("%y%m%d")
	
runparams=get_run_params(runnumber,fullrunnumber,todaysdate)
	
if os.path.isfile('C:\DLOG2\IR\IR'+todaysdate+'.mdb'):
	IRfilename='C:\DLOG2\IR\IR'+todaysdate+'.mdb'
elif os.path.isfile('C:\DLOG2\BackupIR\IR'+todaysdate+'.mdb'):
	IRfilename='C:\DLOG2\BackupIR\IR'+todaysdate+'.mdb'
else:
	print 'IR file not found...exiting program'
	time.sleep(6)
	exit()
OESfilename='C:\DLOG2\OES\OES'+todaysdate+'.mdb'
specmdbfilename='C:\DLOG2\SPEC\SP'+todaysdate+'.mdb'
spectxtfilename='C:\DLOG2\SPEC\SP'+todaysdate+'.txt'

savedir='Y:\Experiment Summaries\Year 20'+todaysdate[:2]+'\S00'+str(runnumber)

	
#import IR data
# set up some constants
MDB = IRfilename; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = ''

# connect to db
con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
cur = con.cursor()

# run a query and get the results 
SQL = 'SELECT DT, IR_Reflection_0, IR_Reflection_1, ABSORPTION FROM IRLOG;' # your query goes here
rows = cur.execute(SQL).fetchall()
cur.close()
con.close()
IRdata=numpy.array(rows)
IRdatetimes=IRdata[:,0]
IR_0=IRdata[:,1]
IR_1=IRdata[:,2]
ABSORPTION=IRdata[:,3]
abs_mvgavg=pandas.rolling_mean(ABSORPTION,20)

#import OES data
# set up some constants
MDB = OESfilename; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = ''

# connect to db
con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
cur = con.cursor()

# run a query and get the results 
SQL = 'SELECT DT, V2, FOS1, FOS2, FOS3, FOS4, FOS5, FOS6, FOS7, FOS8, FOS9, FOS10, FOS11, FOS12 FROM OESLOG;'
rows = cur.execute(SQL).fetchall()
cur.close()
con.close()
OESdata=numpy.array(rows)
OESdatetimes=OESdata[:,0]

Z1A=OESdata[:,2]
Z1B=OESdata[:,3]
Z2A=OESdata[:,4]
Z2B=OESdata[:,5]
Z3A=OESdata[:,6]
Z3B=OESdata[:,7]
Z4A=OESdata[:,8]
Z4B=OESdata[:,9]
Z5A=OESdata[:,10]
Z5B=OESdata[:,11]
Z6A=OESdata[:,12]
Z6B=OESdata[:,13]

In_OES=numpy.empty([len(Z1A)/8,12])
In_OESdates=[]
counter=0
for each in range(len(Z1A)):
	if OESdata[each,1]=='In_451':
		In_OESdates.append(OESdatetimes[each])
		In_OES[counter,0]=Z1A[each]
		In_OES[counter,1]=Z1B[each]
		In_OES[counter,2]=Z2A[each]
		In_OES[counter,3]=Z2B[each]
		In_OES[counter,4]=Z3A[each]
		In_OES[counter,5]=Z3B[each]
		In_OES[counter,6]=Z4A[each]
		In_OES[counter,7]=Z4B[each]
		In_OES[counter,8]=Z5A[each]
		In_OES[counter,9]=Z5B[each]
		In_OES[counter,10]=Z6A[each]
		In_OES[counter,11]=Z6B[each]
		counter+=1
In_OESdates=numpy.array(In_OESdates)


O2_OES=numpy.empty([len(Z1A)/8,12])
counter=0
for each in range(len(Z1A)):
	if OESdata[each,1]=='O2_777':
		O2_OES[counter,0]=Z1A[each]
		O2_OES[counter,1]=Z1B[each]
		O2_OES[counter,2]=Z2A[each]
		O2_OES[counter,3]=Z2B[each]
		O2_OES[counter,4]=Z2A[each]
		O2_OES[counter,5]=Z2B[each]
		O2_OES[counter,6]=Z4A[each]
		O2_OES[counter,7]=Z4B[each]
		O2_OES[counter,8]=Z5A[each]
		O2_OES[counter,9]=Z5B[each]
		O2_OES[counter,10]=Z6A[each]
		O2_OES[counter,11]=Z6B[each]
		counter+=1
		
H2_OES=numpy.empty([len(Z1A)/8,12])
counter=0
for each in range(len(Z1A)):
	if OESdata[each,1]=='H2_656':
		H2_OES[counter,0]=Z1A[each]
		H2_OES[counter,1]=Z1B[each]
		H2_OES[counter,2]=Z2A[each]
		H2_OES[counter,3]=Z2B[each]
		H2_OES[counter,4]=Z2A[each]
		H2_OES[counter,5]=Z2B[each]
		H2_OES[counter,6]=Z4A[each]
		H2_OES[counter,7]=Z4B[each]
		H2_OES[counter,8]=Z5A[each]
		H2_OES[counter,9]=Z5B[each]
		H2_OES[counter,10]=Z6A[each]
		H2_OES[counter,11]=Z6B[each]
		counter+=1

if not os.path.isdir(savedir):
	lastyear = str(int(todaysdate[:2])-1)
	savedir = savedir[:31] + lastyear +'\S00'+str(runnumber)
	if not os.path.isdir(savedir):
		'''app = wx.PySimpleApp()
		dialog = wx.DirDialog(None, "Choose directory to save IR and OES files", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
		dialog.ShowModal()
		dialog.Show(1)
		savedir = dialog.GetPath()
		print savedir
		if dialog.ShowModal() == wx.ID_OK:
			print dialog.GetPath()
		dialog.Destroy()'''
		print 'choose the directory to save the files in'
		root = tk.Tk()
		root.withdraw()
		root.wm_attributes("-topmost",1)
		savedir=tkFD.askdirectory(parent=root,initialdir='Y:\Experiment Summaries\\')

if savedir=='':
	raw_input('you didn\'t choose a directory.  press any key to exit, then try again')
	exit()

if not re.search('MC03\s+OES',savedir):
	savedir+='\MC03 OES\\'
if not os.path.exists(savedir): os.makedirs(savedir)

savedIRfilename = addSaveLabel+'MC03 OES --- IR and Abs --- DW ' + str(runparams['DWstart']) + '-' + str(runparams['DWend']) + '.csv'
with open(savedir+savedIRfilename, 'wb') as fp:
	a = csv.writer(fp, delimiter=',')
	IRlabels=['datetime','payoff IR reflection','takeup IR reflection','Absorption']
	a.writerow(IRlabels)
	a.writerows(IRdata)

savedOESH2filename = addSaveLabel+'MC03 OES --- H2 --- DW ' + str(runparams['DWstart']) + '-' + str(runparams['DWend']) + '.csv'
with open(savedir+savedOESH2filename, 'wb') as fp:
	a = csv.writer(fp, delimiter=',')
	H2labels=['datetime','1A','1B','2A','2B','3A','3B','4A','4B','5A','5B','6A','6B']
	a.writerow(H2labels)
	a.writerows(numpy.column_stack((In_OESdates,H2_OES)))

savedOESO2filename = addSaveLabel+'MC03 OES --- O2 --- DW ' + str(runparams['DWstart']) + '-' + str(runparams['DWend']) + '.csv'
with open(savedir+savedOESO2filename, 'wb') as fp:
	a = csv.writer(fp, delimiter=',')
	O2labels=['datetime','1A','1B','2A','2B','3A','3B','4A','4B','5A','5B','6A','6B']
	a.writerow(O2labels)
	a.writerows(numpy.column_stack((In_OESdates,O2_OES)))

savedOESInfilename = addSaveLabel+'MC03 OES --- In --- DW ' + str(runparams['DWstart']) + '-' + str(runparams['DWend']) + '.csv'
with open(savedir+savedOESInfilename, 'wb') as fp:
	a = csv.writer(fp, delimiter=',')
	Inlabels=['datetime','1A','1B','2A','2B','3A','3B','4A','4B','5A','5B','6A','6B']
	a.writerow(Inlabels)
	a.writerows(numpy.column_stack((In_OESdates,In_OES)))


shutil.copy2(IRfilename, 'Y:\Nate\MC03 optics program\IR\IR' + todaysdate+'.mdb')
shutil.copy2(OESfilename, 'Y:\Nate\MC03 optics program\OES\OES' + todaysdate+'.mdb')
shutil.copy2(specmdbfilename, 'Y:\Nate\MC03 optics program\SPEC\SP' + todaysdate+'.mdb')
shutil.copy2(spectxtfilename, 'Y:\Nate\MC03 optics program\SPEC\SP' + todaysdate+'.txt')

print 'saved files: '
print savedIRfilename
print savedOESH2filename
print savedOESO2filename
print savedOESInfilename
print 'in directory: ', savedir
raw_input('press any key to exit')