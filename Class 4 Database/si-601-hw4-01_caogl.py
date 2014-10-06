# -*- coding: utf-8 -*-
#!/usr/bin/env python

import facebook, urllib2, json, re, os, csv, codecs
from time import sleep


### Code to access the Facebook API
### Put your access token in the string variable:
access_token='CAACEdEose0cBAMt3ZBN0yl112IFPkn6ZA98UVZAHxkZALtx9Ad6sOudonqTDW5uDb90tAAPj5ON3cQYpawTjaZArzZBl1G9u3gZANX996Eci7Is9XvpZBqgYgUIkOTlPmi7bnW4bH7qwsMSSlSQSD895JLnODYsrh2q9ZA3creNwrAxXJLhWAPdH5hfxAFDyeIXhTZCf5fkAWqFoR8IfFuICEsmOxAC6MJgsEZD'

### use Graph API to get friends
graph = facebook.GraphAPI(access_token)
profile = graph.get_object('me')
friends = graph.get_connections('me', 'friends')


with open('friend_profile_caogl.csv', 'a') as table1:
    id_num=1
    for friend in friends['data']:

        
        ## friend id auto increase
        friend_id=id_num
        id_num=id_num+1;
        
        ### get friend details
        response = urllib2.urlopen('https://graph.facebook.com/%s?access_token=%s&fields=gender,birthday,hometown,location,education,checkins' % (friend['id'], access_token))
        json_str = response.read()
        json_obj=json.loads(json_str)

        print json_obj
        #gender
        if 'gender' in json_obj:
            if json_obj['gender']=='male':
                gender='M'
            else:
                gender='F'
        else:
            gender='NULL'

        #birthyear
        if 'birthday' in json_obj:
            match=re.search(r'[0-9]{4}', json_obj['birthday'])
            if match:
                birthyear=match.group()
            else:
                birthyear='NULL'
        else:
            birthyear='NULL'

        #hometown
        if 'hometown' in json_obj:
            hometown_id=json_obj['hometown']['id']
            hometown_name=codecs.encode(json_obj['hometown']['name'], 'utf-8')
        else:
            hometown_id='NULL'
            hometown_name='NULL'

        #location
        if 'location' in json_obj:
            location_id=json_obj['location']['id']
            location_name=codecs.encode(json_obj['location']['name'], 'utf-8')
        else:
            location_id='NULL'
            location_name='NULL'

        #checkins
        if 'checkins' in json_obj and 'data' in json_obj['checkins']:
            checkins=len(json_obj['checkins']['data'])
        else:
            checkins='NULL'

        to_write=[friend_id, gender, birthyear, hometown_id, hometown_name, location_id, location_name, checkins]
        tmp=csv.writer(table1, lineterminator='\n')
        tmp.writerow(to_write)
        
        #education
        if 'education' in json_obj:
            for item in json_obj['education']:
                if 'school' in item:
                    school_id=item['school']['id']
                    school_name=codecs.encode(item['school']['name'], 'utf-8')
                else:
                    school_id='NULL'
                    school_name='NULL'
                if 'type' in item:
                    school_type=codecs.encode(item['type'], 'utf-8')
                else:
                    school_type=item['type']
                to_write=[friend_id, school_id, school_name, school_type]
                with open('friend_education_caogl.csv', 'a') as table2:
                    tmp=csv.writer(table2, lineterminator='\n')
                    tmp.writerow(to_write)
                table2.close()

        sleep(2)
table1.close()       
                    
        
        
        
        


            
        
        
            
            
