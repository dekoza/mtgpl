#coding: utf-8
import re

#~ exp = r'^(?P<numer>\d{3}\.\d+[a-z.]*) (?P<content>.+)'
#~ 
#~ result = []
#~ 
#~ with open('comprules.rst','r') as plik:
    #~ for line in plik.xreadlines():
        #~ r = re.match(exp, line)
        #~ if r:
            #~ number, content = r.groups()
            #~ number = number.strip('.')
            #~ result.append(number+'\n')
            #~ result.append('-'*len(number)+'\n')
            #~ result.append(content+'\n')
        #~ else:
            #~ result.append(line)
#~ with open('cmpformat.rst','w') as zapis:
    #~ zapis.writelines(result)
#~ 
########################################################################
#~ 
#~ exp = r'(?P<pre>.*[Ss]ee rule )(?P<number>\d{3})(?P<post>.*)'
#~ exp = r'(?P<pre>.*[Ss]ee rule )(?P<numer>\d{3}\.\d+[a-z.]*)(?P<post>.*)'
#~ result = []
#~ 
#~ with open('comprules.rst','r') as plik:
    #~ for line in plik.xreadlines():
        #~ r = re.match(exp, line)
        #~ if r:
            #~ pre, number, post = r.groups()
            #~ number = number.strip('.')
            #~ result.append(pre)
            #~ result.append(':ref:`'+number+' <mtgcr-'+number.lower().replace('.','-')+'>`')
            #~ result.append(post+'\n')
        #~ else:
            #~ result.append(line)
#~ with open('cmpformat.rst','w') as zapis:
    #~ zapis.writelines(result)
########################################################################

#~ exp = r'^(?P<numer>\d{3}\.\d+[a-z.]*)$'
#~ exp = r'^(?P<raz>\d{3}\. )(?P<dwa>.+)'
#~ 
#~ result = []
#~ 
#~ with open('comprules.rst','r') as plik:
    #~ for line in plik.xreadlines():
        #~ r = re.match(exp, line)
        #~ if r:
            #~ try:
                #~ number, rest = r.groups()
                #~ number = number.strip().strip('.')
                #~ result.append('.. _mtgcr-'+number+':\n\n')
            #~ except:
                #~ print number, type(number)  
        #~ result.append(line)
#~ with open('cmpformat.rst','w') as zapis:
    #~ zapis.writelines(result)
#~ 

