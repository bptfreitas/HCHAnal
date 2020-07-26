#!/usr/bin/python3

from bs4 import BeautifulSoup
import urllib3
import re

http = urllib3.PoolManager()

url = "https://c19study.com/"

response = http.request('GET', url)

soup = BeautifulSoup(response.data, "lxml")

# pretty output to study
pretty_html = open("Output.html", "w")
pretty_html.write(soup.prettify())
pretty_html.close()

prog_id = re.compile( "^r[0-9]+$" )
index = 1
for table_row in soup.find_all( "td"):
    #print("\nLine "+str(index))

    #print( table_row.attrs )
    try:
        # matches = prog_id.match( table_row['id'] )
        # print( table_row['id'], matches )

        if table_row['class'] == [ 'ratd' , 'ref' ]:
            print("\n\nStudy " + str(index))

            print(table_row)
            print(table_row.contents)

            index += 1
    except:
        pass
    #print(study)
