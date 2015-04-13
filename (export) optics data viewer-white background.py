import pyodbc, time, numpy, matplotlib.dates, pandas, time, datetime, matplotlib, os.path
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates


matplotlib.rcParams.update({'font.size': 22})
try:
	today=input('for previous data, enter date as YYMMDD (otherwise defaults to today): ')
	today=str(today)
except SyntaxError:
	today=time.strftime("%y%m%d")
	
if 	today==time.strftime("%y%m%d"):
	istoday=True
	tries=30
else:
	istoday=False
	tries=1
	
def getdata(*args):
	'''if not firsttime:
		xlims=ax2.xlim()
		ylims=ax2.ylim()'''
		
	#import IR data
	# set up some constants
	MDB = 'C:\DLOG2\IR\IR' + today + '.mdb'; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = ''
	if os.path.isfile(MDB):
		pass
	else:
		MDB = 'C:\DLOG2\BackupIR\IR' + today + '.mdb'; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = ''
	OESMDB = 'C:\DLOG2\OES\OES' + today + '.mdb'; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = ''

	# connect to db
	filefound=False
	for i in range(tries):
		if os.path.isfile(MDB) and os.path.isfile(OESMDB):
			con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
			cur = con.cursor()
			filefound=True
		else:
			if istoday:
				print ""
				print "Data file not found (takes a few minutes for new data to register)...trying again in 20s..."
				time.sleep(20)
	if not filefound:
		if istoday:
			print ""
			print "hmm...something is wonky here...it...must be the apocalypse! RUN!"
			print ""
			time.sleep(1.6)
			print "Actually, wait.  Double check that the TCO Monitor program is open and you have \"Save Data\" checked, and try again."
			print ""
		else:
			print ""
			print "Data file not found.  Double check that you entered the date correctly."
			print ""
			time.sleep(2.5)
			print "self destructing in:"
			print ""
			time.sleep(1)
			for k in range(11):
				print 10-k
				time.sleep(2)
			print "BOOM!"
			time.sleep(2.7)
		try:
			input('press enter key to exit')
			exit()
		except SyntaxError:
			exit()

	# run a query and get the results 
	SQL = 'SELECT DT, IR_Reflection_0, IR_Reflection_1, ABSORPTION FROM IRLOG;' # your query goes here
	rows = cur.execute(SQL).fetchall()
	cur.close()
	con.close()
	data=numpy.array(rows)
	datetimes=data[:,0]
	IR_0=data[:,1]
	IR_1=data[:,2]
	ABSORPTION=data[:,3]
	abs_mvgavg=pandas.rolling_mean(ABSORPTION,20)

	IRdates = matplotlib.dates.date2num(datetimes)

	#import OES data

	# connect to db
	con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,OESMDB,PWD))
	cur = con.cursor()

	# run a query and get the results 
	SQL = 'SELECT DT, V2, FOS1, FOS2, FOS3, FOS4, FOS5, FOS6, FOS7, FOS8, FOS9, FOS10, FOS11, FOS12 FROM OESLOG;'
	rows = cur.execute(SQL).fetchall()
	cur.close()
	con.close()
	data=numpy.array(rows)
	datetimes=data[:,0]
	OESdates = matplotlib.dates.date2num(datetimes)

	Z1A=data[:,2]
	Z1B=data[:,3]
	Z2A=data[:,4]
	Z2B=data[:,5]
	Z3A=data[:,6]
	Z3B=data[:,7]
	Z4A=data[:,8]
	Z4B=data[:,9]
	Z5A=data[:,10]
	Z5B=data[:,11]
	Z6A=data[:,12]
	Z6B=data[:,13]

	In_OES=numpy.empty([len(Z1A)/8,12])
	In_OESdates=[]
	counter=0
	for each in range(len(Z1A)):
		if data[each,1]=='In_451':
			In_OESdates.append(datetimes[each])
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
			
	O2_OES=numpy.empty([len(Z1A)/8,12])
	counter=0
	for each in range(len(Z1A)):
		if data[each,1]=='O2_777':
			O2_OES[counter,0]=Z1A[each]
			O2_OES[counter,1]=Z1B[each]
			O2_OES[counter,2]=Z2A[each]
			O2_OES[counter,3]=Z2B[each]
			O2_OES[counter,4]=Z3A[each]
			O2_OES[counter,5]=Z3B[each]
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
		if data[each,1]=='H2_656':
			H2_OES[counter,0]=Z1A[each]
			H2_OES[counter,1]=Z1B[each]
			H2_OES[counter,2]=Z2A[each]
			H2_OES[counter,3]=Z2B[each]
			H2_OES[counter,4]=Z3A[each]
			H2_OES[counter,5]=Z3B[each]
			H2_OES[counter,6]=Z4A[each]
			H2_OES[counter,7]=Z4B[each]
			H2_OES[counter,8]=Z5A[each]
			H2_OES[counter,9]=Z5B[each]
			H2_OES[counter,10]=Z6A[each]
			H2_OES[counter,11]=Z6B[each]
			counter+=1
	
	OESdates=matplotlib.dates.date2num(In_OESdates)


	ax2 = plt.subplot2grid((4,4), (1,0), colspan=4)
	ax1 = plt.subplot2grid((4,4), (0,0), colspan=4, sharex=ax2)
	ax4 = plt.subplot2grid((4,4), (2, 2), colspan=2, sharex=ax2)
	ax5 = plt.subplot2grid((4,4), (3, 0), colspan=2, sharex=ax2)
	ax6 = plt.subplot2grid((4,4), (3, 2), colspan=2, sharex=ax2)
	ax3 = plt.subplot2grid((4,4), (2, 0), colspan=2, sharex=ax2)
	ax1.plot_date(IRdates, ABSORPTION, color='DarkMagenta')
	ax1.set_ylabel('Absorption')
	ax1.set_ylim([0,60])
	ax1.axhline(45,ls='--',color='Red',linewidth=4)
	ax1.plot_date(IRdates, abs_mvgavg,'-', color='Orange', linewidth=4)
	ax1.grid()
	ax2.grid()
	ax3.grid()
	ax4.grid()
	ax5.grid()
	ax6.grid()
	
	#start, end = ax1.get_xlim() #can be used to get axes min and max
	ax1.yaxis.set_ticks(numpy.arange(0, 70, 10))
	
	plt.setp(ax1.get_xticklabels(), visible=False)
	
	ax2.plot_date(IRdates, IR_0, color="Blue", label="IR0")#, fmt='-', linewidth=4)
	ax2.plot_date(IRdates, IR_1, color="Red", label="IR1")#, fmt='-', linewidth=4)
	ax2.set_ylabel('IR reflection')
	ax2.set_ylim([0,30])
	ax2.yaxis.set_ticks(numpy.arange(0, 30, 10))
	
	legend2 = ax2.legend(bbox_to_anchor=(1.1, -0.45), loc='lower right', borderaxespad=0., shadow=True, labelspacing=0, numpoints=1)
	# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
	frame2 = legend2.get_frame()
	frame2.set_facecolor('0.90')
		# Set the fontsize
	for label in legend2.get_texts():
		label.set_fontsize('25')
	
	
	ax3.plot_date(OESdates, O2_OES[:,0], color='DarkRed', fmt='-', linewidth=4, label='Z1A')
	ax3.plot_date(OESdates, O2_OES[:,1], color='Crimson', fmt='--', linewidth=4, label='Z1B')
	ax3.plot_date(OESdates, O2_OES[:,2], color='OrangeRed', fmt='-', linewidth=4, label='Z2A')
	ax3.plot_date(OESdates, O2_OES[:,3], color='DarkOrange', fmt='--', linewidth=4, label='Z2B')
	ax3.plot_date(OESdates, O2_OES[:,4], color='cadetblue', fmt='-', linewidth=4, label='Z3A')
	ax3.plot_date(OESdates, O2_OES[:,5], color='chartreuse', fmt='--', linewidth=4, label='Z3B')
	ax3.plot_date(OESdates, O2_OES[:,6], color='DarkGreen', fmt='-', linewidth=4, label='Z4A')
	ax3.plot_date(OESdates, O2_OES[:,7], color='ForestGreen', fmt='--', linewidth=4, label='Z4B')
	ax3.plot_date(OESdates, O2_OES[:,8], color='Navy', fmt='-', linewidth=4, label='Z5A')
	ax3.plot_date(OESdates, O2_OES[:,9], color='Blue', fmt='--', linewidth=4, label='Z5B')
	ax3.plot_date(OESdates, O2_OES[:,10], color='Purple', fmt='-', linewidth=4, label='Z6A')
	ax3.plot_date(OESdates, O2_OES[:,11], color='MediumPurple', fmt='--', linewidth=4, label='Z6B')
	
	ax3.yaxis.set_ticks(numpy.arange(0, 10, 2))
	ax3.set_ylabel('O2 OES')
	
	legend = ax3.legend(bbox_to_anchor=(2.3, 0.65), loc='upper right', borderaxespad=0., shadow=True, labelspacing=0, numpoints=1)
	# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
	frame = legend.get_frame()
	frame.set_facecolor('0.90')
		# Set the fontsize
	for label in legend.get_texts():
		label.set_fontsize('25')

	#ax4.plot_date(OESdates, In_OES[:,0], color='DarkRed', fmt='-', linewidth=4, label='Z1A')
	#ax4.plot_date(OESdates, In_OES[:,1], color='Crimson', fmt='--', linewidth=4, label='Z1B')
	#ax4.plot_date(OESdates, In_OES[:,2], color='OrangeRed', fmt='-', linewidth=4, label='Z2A')
	#ax4.plot_date(OESdates, In_OES[:,3], color='DarkOrange', fmt='--', linewidth=4, label='Z2B')
	#ax4.plot_date(OESdates, In_OES[:,4], color='cadetblue', fmt='-', linewidth=4, label='Z3A')
	#ax4.plot_date(OESdates, In_OES[:,5], color='chartreuse', fmt='--', linewidth=4, label='Z3B')	
	ax4.plot_date(OESdates, In_OES[:,6], color='DarkGreen', fmt='-', linewidth=4, label='Z4A')
	ax4.plot_date(OESdates, In_OES[:,7], color='ForestGreen', fmt='--', linewidth=4, label='Z4B')
	ax4.plot_date(OESdates, In_OES[:,8], color='Navy', fmt='-', linewidth=4, label='Z5A')
	ax4.plot_date(OESdates, In_OES[:,9], color='Blue', fmt='--', linewidth=4, label='Z5B')
	ax4.plot_date(OESdates, In_OES[:,10], color='Purple', fmt='-', linewidth=4, label='Z6A')
	ax4.plot_date(OESdates, In_OES[:,11], color='MediumPurple', fmt='--', linewidth=4, label='Z6B')
	ax4.yaxis.set_ticks(numpy.arange(0, 100, 20))
	ax4.set_ylabel('In OES')
	
	ax5.plot_date(OESdates, H2_OES[:,0], color='DarkRed', fmt='-', linewidth=4, label='Z1A')
	ax5.plot_date(OESdates, H2_OES[:,1], color='Crimson', fmt='-', linewidth=4, label='Z1B')
	ax5.plot_date(OESdates, H2_OES[:,2], color='OrangeRed', fmt='-', linewidth=4, label='Z2A')
	ax5.plot_date(OESdates, H2_OES[:,3], color='DarkOrange', fmt='-', linewidth=4, label='Z2B')
	ax5.plot_date(OESdates, H2_OES[:,4], color='cadetblue', fmt='-', linewidth=4, label='Z3A')
	ax5.plot_date(OESdates, H2_OES[:,5], color='chartreuse', fmt='--', linewidth=4, label='Z3B')	
	ax5.plot_date(OESdates, H2_OES[:,6], color='DarkGreen', fmt='-', linewidth=4, label='Z4A')
	ax5.plot_date(OESdates, H2_OES[:,7], color='ForestGreen', fmt='-', linewidth=4, label='Z4B')
	ax5.plot_date(OESdates, H2_OES[:,8], color='Navy', fmt='-', linewidth=4, label='Z5A')
	ax5.plot_date(OESdates, H2_OES[:,9], color='Blue', fmt='-', linewidth=4, label='Z5B')
	ax5.plot_date(OESdates, H2_OES[:,10], color='Purple', fmt='-', linewidth=4, label='Z6A')
	ax5.plot_date(OESdates, H2_OES[:,11], color='MediumPurple', fmt='-', linewidth=4, label='Z6B')
	ax5.yaxis.set_ticks(numpy.arange(0, 18, 2))
	ax5.set_ylabel('H2 OES')

	#ax6.plot_date(OESdates, In_OES[:,0]/O2_OES[:,0], color='DarkRed', fmt='-', linewidth=4, label='Z1A')
	#ax6.plot_date(OESdates, In_OES[:,1]/O2_OES[:,1], color='Crimson', fmt='--', linewidth=4, label='Z1B')
	#ax6.plot_date(OESdates, In_OES[:,2]/O2_OES[:,2], color='OrangeRed', fmt='-', linewidth=4, label='Z2A')
	#ax6.plot_date(OESdates, In_OES[:,3]/O2_OES[:,3], color='DarkOrange', fmt='--', linewidth=4, label='Z2B')
	#ax6.plot_date(OESdates, In_OES[:,4]/O2_OES[:,4], color='cadetblue', fmt='-', linewidth=4, label='Z3A')
	#ax6.plot_date(OESdates, In_OES[:,5]/O2_OES[:,5], color='chartreuse', fmt='--', linewidth=4, label='Z3B')	
	ax6.plot_date(OESdates, In_OES[:,6]/O2_OES[:,6], color='DarkGreen', fmt='-', linewidth=4, label='Z4A')
	ax6.plot_date(OESdates, In_OES[:,7]/O2_OES[:,7], color='ForestGreen', fmt='--', linewidth=4, label='Z4B')
	ax6.plot_date(OESdates, In_OES[:,8]/O2_OES[:,8], color='Navy', fmt='-', linewidth=4, label='Z5A')
	ax6.plot_date(OESdates, In_OES[:,9]/O2_OES[:,9], color='Blue', fmt='--', linewidth=4, label='Z5B')
	ax6.plot_date(OESdates, In_OES[:,10]/O2_OES[:,10], color='Purple', fmt='-', linewidth=4, label='Z6A')
	ax6.plot_date(OESdates, In_OES[:,11]/O2_OES[:,11], color='MediumPurple', fmt='--', linewidth=4, label='Z6B')
	ax6.set_ylabel('In:O2 OES')
	
	ax6.set_ylim([0,40])
	ax6.yaxis.set_ticks(numpy.arange(0, 50, 10))
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	plt.setp(ax3.get_xticklabels(), visible=False)
	plt.setp(ax4.get_xticklabels(), visible=False)
	ax5.set_xlabel('time')
	ax6.set_xlabel('time')
	'''if not firsttime:
		ax2.xlim(xlims)
		ax2.ylim(ylims)
	global firsttime
	firsttime=False'''
		

fig=plt.figure(facecolor='white')
fig.canvas.set_window_title('optics data monitor')
plt.xlabel('Time')
#global firsttime
firsttime=True
ani = animation.FuncAnimation(fig, getdata, interval=15000000000000000000000000000000000000000000000000)
fig.subplots_adjust(bottom=0.1, left=0.05, right=0.9, top=0.95)
plt.show()