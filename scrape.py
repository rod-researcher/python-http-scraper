import sys
import requests
import pprint
from BeautifulSoup import BeautifulSoup
from netaddr import *
import threading

import time
start_time = time.time()
cntr = 0
time_out_sec = 2.4

helpmsg = "Usage : scrape-scan.py IP-network\n i.e. scrape-scan.py 192.168.0.0/24\n alowed CIDR netmasks are from /8 to /32"


if len(sys.argv) != 2:
    print helpmsg
    sys.exit()


try:
    ip = IPNetwork(sys.argv[1])
except:
    print sys.argv[1] + ' is not a valid network'
    print helpmsg
    sys.exit()


iplength = len(ip)
hitcnt = 0

if iplength <= 0 or  iplength > 16777216:
    print helpmsg
    sys.exit()

print '---------------------------------------------------------------------------------------'
print 'Starting web scraper for network ' + '%s' % ip + ' with ' + '%s' % iplength + ' hosts'
print '---------------------------------------------------------------------------------------\n\n'

#scrape_site_tr  is unused, I leava as an example on how to narrow down the search to only HTML tables and table data
def scrape_site_tr (address):
    url = 'http://' + '%s' % address
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find('tbody', attrs={'class': 'stripe'})
    list_of_rows = []
    for row in table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll('td'):
            text = cell.text.replace('&nbsp;', '')
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    return list_of_rows

#scrape_site_all scrapes the whole index.html HTML code from the host
def scrape_site_all (address):
    #simple_track_thread += 1
    url = 'http://' + '%s' % address + '/'
    result = ''
    response = ''
    html = ''
    try:
        response = requests.get(url, timeout=time_out_sec)
        html = response.content
    except Exception:
        #print 'exception raised for ' + url
        pass
    finally:
        soup = BeautifulSoup(html)
        result = soup.prettify()
    #print 'result length is : ' +  '%s' % len(result)
    if result != '':
        print '========================= SITE : ' + url + ' ========================\n' + result + '\n\n'
        return 1
    else:
        return 0

# multithreading, very sloppy code but does the job fast
class scrape_thread(threading.Thread):
    cnt = cntr
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.address = address
        self.hit = 0

    def run(self):
        self.cnt += scrape_site_all(self.address)
        #scrape_site_all(self.address)

threads = []

#very bad threading, gives the results as who is first to finish and no organization of results
#this can be improved with queues but this is fast and gets the job done
#iplength checks if the subnet is with in /32 = 1 address to /8 = 16777216 addresses 
if iplength >= 1 and  iplength <= 16777216:
    for host in ip:
        hoststr = '%s' % host
        thread = scrape_thread(host)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

print("--- Scraper finished in %s seconds ---" % (time.time() - start_time))
#some broken counter stuffs
#print("Got " + '%s' % cntr + " hits")
