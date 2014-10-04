import csv, math


def isMissing(line):
    if len(line)==20 and line[1]!='' and line[4]!='' and line[5]!='' and line[6]!='' and line[9]!='' and line[19]!='':
        return False
    else:
        return True
    
#step 1
# the function to read input files line by line, ignore lines with missing data
def readDataFile1(fileName):

    line_list=[]
    
    fileHeader=open(fileName, 'rU') # universal new line, to parse lines by special delimiter
    line=fileHeader.next() # skipping the first header line
    for line in fileHeader:
        #print 'haha'
        line=line.replace('"','')
        line=line.replace(',','')
        line=line.strip().split('\t') # remove the head and tail spaces and split into list by delimiter '\t'
        year=line[1].split('/')
        year=int(year[2])

        if isMissing(line)==False and (year==2000 or year==2010): # if no missing values and year is either 2000 or 2010
            info=dict() # need key and value pairs
            info['country']=line[0]
            info['date']=year
            info['population']=int(line[9])
            info['mobile_sub']=int(line[4])
            info['health']=int(line[6])
            info['internetUser']=int(line[5])
            info['gdp_per_cap']=int(line[19])
            info['mobile_per_cap']=float(line[4])/float(line[9])
            info['log_gdp_per_cap']=math.log(float(line[19])+0.001)
            info['log_health']=math.log(float(line[6])+0.001)
            line_list.append(info)

    fileHeader.close()
    return line_list

# step 2
def readDataFile2(fileName):
    
    hash_map1=dict()
    fileHeader=open(fileName, 'rU')
    line=fileHeader.next()

    for line in fileHeader:
        line=line.strip().split('\t')
        hash_map1[line[2]]=line[0]
        
    fileHeader.close()
    return hash_map1
    
# step 6: write to .csv file
def write_csv(dict_list, fileName, labels):
    fileHeader=open(fileName, 'wb') # binary write mode, more stable, use 'w'/'r' only for .txt file
    csvwriter=csv.DictWriter(fileHeader, fieldnames=labels, delimiter=',')
    csvwriter.writeheader() # write the label row
    for item in dict_list:
        csvwriter.writerow(item)
    fileHeader.close()
    
def main():
    
    indicatorData=readDataFile1('C:\Users\caogl\Downloads\si601-f14-hw1\world_bank_indicators.txt')
    regionHash=readDataFile2('C:\Users\caogl\Downloads\si601-f14-hw1\world_bank_regions.txt')
    # step 2: map country to region
    finalData=[]
    
    for item in indicatorData:
        if item['country'] in regionHash:
            item['region']=regionHash.get(item['country'])
            finalData.append(item)

    # step 5: 3-level sort
    indicatorData=sorted(finalData, key=lambda x: (x['date'], x['region'], x['gdp_per_cap']))
    # step 6: write to .csv file
    labels=['country','date','population','mobile_sub','health','internetUser','gdp_per_cap','mobile_per_cap','log_gdp_per_cap','log_health','region']


            
    write_csv(finalData, 'C:\Users\caogl\Downloads\worldbank_output_caogl.csv', labels)
    
if __name__ == '__main__':
  main()
