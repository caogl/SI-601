import sqlite3, csv

#connect to database
conn=sqlite3.connect(r'si-601-hw4_caogl.db')
c=conn.cursor()

sql='''	SELECT p.friend_id, IFNULL(p.checkins, 0), IFNULL(e.max_school_level, 0)
	FROM FRIEND_PROFILE p LEFT JOIN 
		(SELECT friend_id, max(case when school_type='Graduate School' then 3
					    when school_type='College' then 2
					    when school_type='High School' then 1
				       end) as max_school_level
		 FROM FRIEND_EDUCATION
		 GROUP BY friend_id) e ON p.friend_id=e.friend_id '''

c.execute(sql)

result=c.fetchall()
print len(result)

with open('friend_join_caogl.csv', 'w') as friend_join:
	output=csv.writer(friend_join)
	output.writerow(['friend_id', 'checkins', 'max_school_level'])
	output.writerows(result)
friend_join.close()
