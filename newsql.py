
import minimalmodbus
import pandas as pd 
import datetime 
import requests
import json
import os
import pymysql
import time
import statistics




# initilize soil sensor-----------------------------------------------------
PORT='/dev/ttyUSB0' #on pi
#PORT="COM3" #on jeffs laptop

#register numbers based on rs458 protocol
N_reg= 30
P_reg=31
K_reg=32
PH_reg=6
humidity_reg=18
temp_reg=19
cond_reg=21



values=(N_reg,P_reg,K_reg,PH_reg,humidity_reg,temp_reg,cond_reg)

#Set up instrument
tries = 0
while tries<3:
	try:
		instrument = minimalmodbus.Instrument(PORT,1,mode=minimalmodbus.MODE_RTU)
		tries=4
	except: 
		print("not connecting to rs458")
		time.sleep(30)
		tries+=1



instrument.serial.baudrate = 9600

#Make the settings explicit
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.close_port_after_each_call = True
instrument.clear_buffers_before_each_transaction = True
n=instrument.read_register(30)
#--------------------------------------------------------------------

def soilsensor():
	global df
	tick=0
	templist=[]
	df = pd.DataFrame(templist, columns = ["N","P","K","PH","humidity","temp","cond"]) 

	while tick <10:
		tick+=1
		templist=[]
		for i in values:

			value = instrument.read_register(i)
			print(value)
			templist.append(value) #temporary list of all values

		
		
		print("templist",templist)
		print("df", df)
		df.loc[len(df)] = templist
		
	





#["N","P","K","PH","humidity","temp","cond","time"]
#Reading soil sensor and pushing to sql server-------------------------------
def sql():


	cursor.execute("CREATE TABLE IF NOT EXISTS soil_sensor (id INT(11) NOT NULL AUTO_INCREMENT, n FLOAT NOT NULL, p FLOAT NOT NULL, k FLOAT NOT NULL, ph FLOAT NOT NULL, humidity FLOAT NOT NULL, temp FLOAT NOT NULL, cond FLOAT NOT NULL, time TIMESTAMP NOT NULL, PRIMARY KEY (id))")

	#cursor.execute("SELECT * FROM soil_sensortest4")
	#myresult = cursor.fetchall()
	#print('printing soil_sensortest2 now')




	#for x in myresult:
  	#		print(x)

		
	sql="INSERT INTO soil_sensor (n,p,k,ph,humidity,temp,cond,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
	# tick=0
	# while tick <10:

			# a = a.ppend(instrument.read_register(N_reg))
			# b=b.append(instrument.read_register(P_reg))
			# c=c.append(instrument.read_register(K_reg))
			# d=d.append(instrument.read_register(PH_reg))
			# e=e.append(instrument.read_register(humidity_reg)/10)
			# f=f.append((instrument.read_register(temp_reg))/10)
			# g=g.append(instrument.read_register(cond_reg))
			# h=h.append(datetime.datetime.now())
	soilsensor() #collect 10 values in temp table named df
		#["N","P","K","PH","humidity","temp","cond","time"]
	a=df["N"].mean() 
	b=df["P"].mean() 
	c=df["K"].mean() 
	d=df["PH"].mean() 
	e=df["humidity"].mean()
	f=df["temp"].mean() 
	g=df["cond"].mean() 
	
	h = datetime.datetime.now()
	 

	print('time',h)
	insert=(a,b,c,d,e,f,g,h)
	print("insert",insert)
	cursor.execute(sql,insert)
	connection.commit() 
		

	#cursor.execute("SELECT * FROM soil_sensor")
	#myresult = cursor.fetchall()
	#print('printing soil_sensortest now')
	#for x in myresult:
  	#		print(x)



#establish connection to mysql AWS databased--------------------------------------------------------
#def sqlconnect():
user = 'admin'
password = 'biobox2025'
host = 'verdant.c72smgcs44df.us-east-1.rds.amazonaws.com'
port = 3306
database = 'biobox'


connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

cursor = connection.cursor()
#-------------------------------------------------------------------------------------------------------




#control relays for soil sensor and air gradient --------------------------
#two 5v gpio pins on pi zero 2 w



#deal with exceptions - wait and try again
	#lack of network connectivity
	#rs458 not reading - to be tested


#-------------------------------------------------------------------------

#main loop with keyboard interupt----------------------------------------

print("starting")
#sqlconnect()
try:

	while True:
	    sql()
	    time.sleep(300) #take values every 5 min

except KeyboardInterrupt:
	print('interrupted!')

print("ending")
#---------------------------------------------------------------------------




#Previous Method of collecting soil sensor data. ---------------------------------------------------



	#Master=pd.concat([Master,df])
	#print('master',Master)

def requestairgradient():
		global Master_Air

		response=requests.get("https://api.airgradient.com/public/api/v1/locations/81542/measures/current?token=2932e6e4-a882-43d9-833c-ec57b87e49a7")
		jsona=response.json()
		dfresponse=pd.json_normalize(jsona) #getting json api response as data frame

		dfresponse=dfresponse[['pm01','pm02','pm10','pm003Count','atmp','rhum','rco2','tvoc','timestamp']] #sub smapling columns of interest

		dfresponse=dfresponse.iloc[0,:] #convert to string so it can be appended to data fram

		Master_Air.loc[len(Master_Air)] = dfresponse #adding last read to master air data frame

		print(Master_Air)





		return fig
		if __name__ == "__main__":
	   		 app2.run_server(debug=True)
