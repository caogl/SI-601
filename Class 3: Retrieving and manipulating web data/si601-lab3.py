#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lab 3 SI 601: Fetching and parsing structured documents
#
# The utf8 'magic comment' is to tell Python that this source code will
# contain unicode literals outside of the ISO-Latin-1 character set.

# Some lines of code are taken from Google's Python Class
# http://code.google.com/edu/languages/google-python-class/  and
# an earlier lab by Dr. Yuhang Wang.

# The purpose of this lab is to have you practice using some powerful
# modules for fetching and parsing content:
#    urllib2 : for fetching the content of a URL (e.g. HTML page)
#    BeautifulSoup : for parsing HTML and XML pages
#    json : for JSON reading and writing
#
# As in earlier labs, you should fill in the code for the functions below.
# main() is already set up to call the functions with a few different inputs,
# printing 'OK' when each function is correct.

from bs4 import BeautifulSoup
import json, urllib2

# this is the html document used in this lab
html_doc = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
      "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
  <title>Three Little Pigs</title>
  <meta name="generator" content="Amaya, see http://www.w3.org/Amaya/">
</head>

<body>
<p>Once upon a time, there were <a
href="http://en.wikipedia.org/wiki/Three_Little_Pigs">three little pigs</a>:</p>
<ol>
  <li><h2>Pig A</h2>
  </li>
  <li><h2>Pig B</h2>
  </li>
  <li><h2>Pig C</h2>
  </li>
</ol>

<p>And unfortunately, there was a <a
href="http://en.wikipedia.org/wiki/Big_bad_wolf">big bad wolf</a> too.</p>

<p>There are many stories about them.</p>

<h2>Story 1</h2>

<p>This is story 1.</p>

<h2>Story 2</h2>

<p>This is story 2.</p>

<h2>Story 3</h2>

<p>This is story 3.</p>

<h1>Type of Houses Constructed</h1>

<table border="1" style="width: 100%">
  <caption></caption>
  <col>
  <col>
  <tbody>
    <tr>
      <td>Pig</td>
      <td>House Type</td>
    </tr>
    <tr>
      <td>Pig A</td>
      <td>Straw</td>
    </tr>
    <tr>
      <td>Pig B</td>
      <td>Stick</td>
    </tr>
    <tr>
      <td>Pig C</td>
      <td>Brick</td>
    </tr>
  </tbody>
</table>
</body>
</html>
"""

# this is the json string used in this lab
json_str = '{"Belle": 3, "Aurora": 2, "Jasmine": 1, "Irene": 1, "Adella": 1}'

# A. get_title (2 points)
# The get_title function should should process the HTML page stored in the global
# variable html_doc, and return the title of the page in a unicode string.
# get_title() should return u'Three Little Pigs'
def get_title():
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  soup=BeautifulSoup(html_doc)
  return soup.title.string


# B. process_json (2 points)
# The process_json function should load the dictionary stored as a JSON string
# in global variable json_str, and return the sum of the values in this dictionary.
# process_json() should return 8 because 3+2+1+1+1 = 8
def process_json():
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  result=json.loads(json_str)
  return sum(result.values())


# C. get_pigs (3 points)
# The get_pigs function should process the HTML page stored in the global variable
# html_doc, and return the three pigs listed below 'there were three little pigs'
# in a JSON string.
# Note that it should return a string, not a list. 
# get_pigs() should return '["Pig A", "Pig B", "Pig C"]'
def get_pigs():
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  soup=BeautifulSoup(html_doc)
  result=[]
  for item in soup.findAll('li'):
	result.append(item.h2.string)
  return json.dumps(result)


# D. get_story_headings (3 points)
# The get_story_headings function should process the HTML page stored in the global variable
# html_doc, and return the three story headings in a JSON string.
# Note that it should return a string, not a list. 
# get_story_headings() should return '["Story 1", "Story 2", "Story 3"]'
def get_story_headings():
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  soup=BeautifulSoup(html_doc)
  result=[]
  for item in soup.findAll('h2'):
    if item.parent.name=='body':
      result.append(item.string)
  return json.dumps(result)


# E. get_houses (3 points)
# The get_houses function should process the HTML page stored in the global variable
# html_doc, and return information in the house table in a JSON string.
# Note that it should return a string, not a list.
# get_houses() should return '[["Pig A", "Straw"], ["Pig B", "Stick"], ["Pig C", "Brick"]]'
# HINT: contruct a list of tuples first, and then convert it to a JSON string.
def get_houses():
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  soup=BeautifulSoup(html_doc)
  result=[]
  for item in soup.findAll('tr'):
    pig=item.findAll('td')[0].string
    house=item.findAll('td')[1].string
    result.append((pig, house))
  del result[0]
  return json.dumps(result)


# F. get_links (3 points)
# The get_links function should process the HTML page stored in the global variable
# html_doc, and return all url links in the page in a JSON string.
# Note that it should return a string, not a list.
# get_links() should return '["http://en.wikipedia.org/wiki/Three_Little_Pigs", "http://en.wikipedia.org/wiki/Big_bad_wolf"]'
def get_links():
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  soup=BeautifulSoup(html_doc)
  result=[]
  for item in soup.findAll('a'):
    result.append(item.get('href'))
  return json.dumps(result)


# G. treasure_hunting (4 points)
# The treasure_hunting function should first visit http://www.example.com, and
# then find the only url link on that page, and then visit that url link.
# On this page, there is a table under 'Test IDN top-level domains'. In the first
# column (Domain), there are a list of foreign characters.
# You need to fetch the content of the cell in column 1 and row 3, and return it
# in a unicode string.
#
# treasure_hunting() should return the Unicode string u'\u6d4b\u8bd5' corresponding
# to the characters 浿诿  (the code points U+6D4B U+8BD5)
def treasure_hunting():
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  response=urllib2.urlopen('http://www.umich.edu/~kevynct/si601/Example_Domain.htm')
  html_doc=response.read()
  soup=BeautifulSoup(html_doc)
  link=soup.a.get('href') # href = More Information
  response=urllib2.urlopen(link) 
  html_doc=response.read()
  soup=BeautifulSoup(html_doc)

  table=soup.findAll('table')[0] # the first table matches
  item=table.findAll('tr')[3]# row 3, there is a lable row
  item=item.findAll('td')[0]   
  return item.string


#######################################################################
# DO NOT MODIFY ANY CODE BELOW
#######################################################################

# Provided simple test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))

def test2(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print '%s got: %s expected: %s' % (prefix, got, expected)

# Provided main() calls the above functions with interesting inputs,
# using test() to check if each result is correct or not.
def main():

  print 'get_title'

  test(get_title(), u'Three Little Pigs')
  
  print 'process_json'

  test(process_json(), 8)

  print 'get_pigs'

  test(get_pigs(),  '["Pig A", "Pig B", "Pig C"]' )
  
  print 'get_story_headings'

  test(get_story_headings(),  '["Story 1", "Story 2", "Story 3"]' )

  print 'get_houses'

  test(get_houses(), '[["Pig A", "Straw"], ["Pig B", "Stick"], ["Pig C", "Brick"]]')

  print 'get_links'

  test(get_links(), '["http://en.wikipedia.org/wiki/Three_Little_Pigs", "http://en.wikipedia.org/wiki/Big_bad_wolf"]')

  print 'treasure_hunting'

  test2(treasure_hunting(), u'\u6d4b\u8bd5')
  

  
# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

