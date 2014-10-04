from bs4 import BeautifulSoup
import json, urllib2
import re
from time import sleep

import pydot
import itertools

def step():
  
  ##########################step1##########################
  response=urllib2.urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100')
  html_doc=response.read()
  soup=BeautifulSoup(html_doc)
  file1=open(r'step1.html', 'w')
  file1.write(soup.prettify().encode('utf8'))
  file1.close()

  ##########################step2##########################
  table=soup.findAll('table')[0]
  result=[];
  for item in table.findAll('tr')[1:]:  # skip the tile of the table

    # to get the IMBD ID and title
    link=item.a.get('href')
    title=item.a.get('title')
    imbdid=re.search(r'/title/(.+)/', link)
        
    # to get the rank number
    if item.td.get('class')[0]==u'number':
      rank=re.search(r'\d+', item.td.string) 
    
    result.append((imbdid.group(1), rank.group(), title))
  
  file2=open(r'step2.txt', 'w')
  for item in result:
    line='\t'.join(item)+'\n'
    file2.write(unicode(line).encode('utf8'))
  file2.close() 
    
  ##########################step3##########################
  file3=open(r'step3.txt', 'w')
  for item in result:
    imbdid=item[0]   
    url='http://www.omdbapi.com/?i='+imbdid
    response=urllib2.urlopen(url)
    jsonStr=response.read()
    file3.write(jsonStr+'\n')
    sleep(1)
  file3.close()

  ##########################step4##########################
  
  file4=open(r'step4.txt', 'w')
  file3=open(r'step3.txt', 'rU')
  for item in file3:
    item=item.strip()
    metaData=json.loads(item)
    title=metaData.get('Title')
    title=json.dumps(title)
    title=title.replace('"', '')
    actors=metaData.get('Actors')
    actors=json.dumps(actors)
    actors=actors.replace('"','');
    actors=actors.replace(', ',',')
    actors=actors.split(',')
    actors=json.dumps(actors)
    file4.write(title+'\t'+actors+'\n')

  file4.close()
  file3.close()

  ##########################step5##########################

  graph=pydot.Dot(graph_type='graph')

  infile=open(r'step4.txt', 'rU')

  for item in infile:
    item=item.strip()
    item=item.split('\t')
    actors=item[1]
    actors=json.loads(actors)
    
    actor_pairs = itertools.combinations(actors, 2)
    for p in actor_pairs:
      edge = pydot.Edge(p[0], p[1])
      graph.add_edge(edge)
    
  infile.close()
  graph1=r'actors_graph_output.dot'
  graph.write(graph1)
  
# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main():

  step()
  

  
# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

