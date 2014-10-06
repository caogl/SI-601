import csv, sqlite3

#connect to the database
conn=sqlite3.connect(r'si-601-hw4_caogl.db')
c=conn.cursor();

#create two tables
c.execute('CREATE TABLE FRIEND_PROFILE (friend_id INT, gender TEXT, birthyear INT, hometown_id INT, hometown_name INT, location_id INT, location_name TEXT, checkins INT)')	
c.execute('CREATE TABLE FRIEND_EDUCATION (friend_id INT, school_id INT, school_name TEXT, school_type TEXT)')

#read data line by line and inert into tables
with open('friend_profile_caogl.csv', 'rU') as sheet1:
	data=csv.reader(sheet1)
	i=0
	for item in data:
		i=i+1
		print i
		if item[1]!='NULL':
			item[1]='"'+item[1]+'"'
		if item[4]!='NULL':
			item[4]='"'+item[4]+'"'
		if item[6]!='NULL':
			item[6]='"'+item[6]+'"'
		sql='INSERT INTO FRIEND_PROFILE VALUES('+','.join(item)+');'
		print sql
		c.execute(sql)
sheet1.close()

with open('friend_education_caogl.csv', 'rU') as sheet2:
	data=csv.reader(sheet2)
	i=0
	for item in data:
		i=i+1
		print i
		if item[2]!='NULL':
			item[2]='"'+item[2]+'"'
		if item[3]!='NULL':
			item[3]='"'+item[3]+'"'
		sql='INSERT INTO FRIEND_EDUCATION VALUES('+','.join(item)+');'
		print sql
		c.execute(sql)
sheet2.close()

#commit the change
conn.commit()	
