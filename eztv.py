#!/usr/bin/python

import os
import urllib2
import re
import pickle
import time

def check(name, s, history):
  print "Looking for " + name
  m = re.search(r'\<a href="(magnet[^"]+' + name + r'([^\.]+)\.[^"]+)"',s)
  if m and len(m.groups()) > 0:
    link = m.group(1)
    if link:
      ver = m.group(2)
      print "ver=" + ver
      if ver:
        if not (name, ver) in history:
          download(name, link)
          history[(name, ver)] = link
        else:
          print "Ignore " + name + " " + ver + ". Already downloaded it"

def download(name, link):
  print "Found " + name + " link: " + link
  os.system('open "' + link + '"') 

if os.path.exists('history'):
  with open('history', 'r') as f:
    history = pickle.load(f)
else:
  history = {}

print "Loaded history " + str(history)

while True:
  feed = urllib2.urlopen("http://eztv.it/sort/100/")
  s = feed.read()

  print "Got feed from eztv"

  check(r'Latest\.News\.', s, history)

  with open('history', 'w+') as f:
    pickle.dump(history, f)
 
  time.sleep(60)   
