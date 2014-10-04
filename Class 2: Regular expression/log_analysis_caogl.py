import re

def process_log_file(filename):

    valid_logs=[]
    invalid_logs=[]

    f=open(filename, 'rU')
    for item in f:
        line=item.strip().split()
        
        timestamp=line[3]
        verb=line[5]
        url=line[6]
        http2=line[7] # may not exist, need to check
        status=line[8]

        # check the correctness of url, if valid, extract the top level domain
        top_level_domain=re.search(r'^http[s]?://[A-Za-z]+[^/:]+\.([A-Za-z]+)[/:]?', url)
        if top_level_domain!=None:
            top_level_domain=top_level_domain.group(1).lower()
            if top_level_domain=='php':
                print url
               
        # if http2 part is missing, adjust the value of status
        if re.match(r'^[0-9]{3}$', http2) != None:
            status = http2
        # extract the date for write valid_log.txt    
        date = re.search(r'[[0-9]{2}/[a-zA-Z]{3}/[0-9]{4}', timestamp)        
        date= date.group(0)

        # verb should be GET or POST
        # status should be 200
        # append the dict() data sturture into list<dict()>
        if re.search(r'(GET|POST)', verb)==None or status != '200' or top_level_domain==None:
            invalid_logs.append({'date':date, 'top_level_domain':top_level_domain, 'raw_line': item})        
        else:
            valid_logs.append({'date':date, 'top_level_domain':top_level_domain, 'raw_line': item})
        
    f.close()
    return (valid_logs, invalid_logs)

# start execution
if __name__ == '__main__':

    # data structure: dict(dict()) outer key is the date, second key is the top_level_domain, element is the count 
    report=dict()
    (valid_logs, invalid_logs)=process_log_file(r'C:\Users\caogl\Downloads\access_log.txt')
    for item in valid_logs:
        top_level_domain=item['top_level_domain']
        date=item['date']
        if report.get(date)==None:
            report[date]=dict()
            report[date][top_level_domain]=1
        else:
            if report[date].get(top_level_domain)==None:
                report[date][top_level_domain]=1
            else:
                report[date][top_level_domain]+=1

    # write the
    f1=open(r'C:\Users\caogl\Downloads\valid_log_summary_caogl.txt','w+')
    sortedKeys1=sorted(report.keys())
    for date in sortedKeys1:
        count=report[date]
        sortedKeys2=sorted(count.keys())
        output=date
        for top_level_domain in sortedKeys2:
            output=output+'\t'+top_level_domain+':'+str(count[top_level_domain])
        f1.write(output+'\n')
    f1.close()

    f2= open(r'C:\Users\caogl\Downloads\invalid_access_log_caogl.txt','w+')
    for item in invalid_logs:
        line = item['raw_line']
        f2.write(line)
        
    f2.close()

