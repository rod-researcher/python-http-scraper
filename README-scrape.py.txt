Here is a handy readme on how to fully use the scrape.py script

There are a fiew non standard python pacages you will need
install them with pip
pip install requests
pip install pprint
pip install BeautifulSoup
pip install netaddr



Example how you can get the sorted list of scraped IP addresses:
python scrape.py x.y.z.n/i > scrape-result.txt 
grep -E "\=\=\=\=\=\=\=\= SITE" scrape-result.txt | awk '{print $4}' | sed 's/http\:\/\// /' | sed 's/\///' | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4


Example on finding some string and also see from what host it was found, with line number:
python scrape.py x.y.z.n/i > scrape-result.txt
grep -n -E "some string|\=\=\=\=\=\=\=\= SITE" scrape-result.txt



