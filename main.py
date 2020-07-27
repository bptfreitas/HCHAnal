#!/usr/bin/python3

from bs4 import BeautifulSoup
import urllib3
import re
import sys
import pickle

debug = True

http = urllib3.PoolManager()

url = "https://c19study.com/"

response = http.request('GET', url)

soup = BeautifulSoup(response.data, "lxml")

# saves HTML file for later study if necessary
pretty_html = open("Output.html", "w")
pretty_html.write(soup.prettify())
pretty_html.close()

prog_id = re.compile( "^r[0-9]+$" )
index = 1

sys.stdout.write( "\nProcessing results ..." )

results = []
titles = []
refs = []
for table_row in soup.find_all( "td"):
    #print (  set( table_row['class'] ) )

    # study result
    try:        
        if set( [ 'xatd' , 'xresult' ] ) & set( table_row['class'] ) == set( [ 'xatd' , 'xresult' ] ):
            sys.stdout.write( "\nxresult found" )
            results.append( table_row.contents )
    except:
        pass

    # study reference
    try:
        if table_row['class'] == [ 'xctd' , 'xref' ]:
            sys.stdout.write( "\nxref found" )
            refs.append( table_row.contents )
    except:
        pass

    # study title
    try:
        if table_row['class'] == [ 'xctd' , 'xtitle' ]:
            sys.stdout.write( "\nxtitle found" )
            titles.append( table_row.contents )
    except:
        pass

print('\n')

n_titles = str( len( titles ) )
n_refs = str( len( refs ) )
n_results = str( len( results ) )

sys.stdout.write("\nTotal titles: " + n_titles )
sys.stdout.write("\nTotal refs: " + n_refs )
sys.stdout.write("\nTotal results: " + n_results )

if len(titles) != len(refs):
    sys.stderr.write("\nERROR: number of titles != number os references (" + str( n_titles ) + "/"+ str( n_refs ) +"\n"  )
    sys.exit(-1)

if len(titles) != len(results):
    sys.stderr.write("\nERROR: number of titles != number of results (" + str( n_titles ) + "/"+ str( n_results) +"\n"  )
    sys.exit(-1)    


if debug:
    sys.stdout.write( "\nDEBUG: Saving 'titles' list on file 'titles.dat'" )
    titles_file = open("titles.dat", "w")
    first = True
    for t in titles:
        if not first:
            titles_file.write( "\n" + str(t) )
        else:
            titles_file.write( str(t) )
            first = False
    titles_file.close()

    sys.stdout.write( "\nDEBUG: Saving 'references' list on file 'refs.dat'" )
    refs_file = open("references.dat", "w")
    first = True
    for r in refs:
        if not first:
            refs_file.write( "\n" + str( r ) )
        else:
            refs_file.write( str( r ) )
            first = False
    refs_file.close()

    sys.stdout.write( "\nDEBUG: Saving 'results' list on file 'results.dat'" )
    results_file = open("results.dat", "w")
    first = True
    for r in results:
        if not first:
            results_file.write( "\n" + str( r ) )
        else:
            results_file.write( str( r ) )
            first = False
    results_file.close()    

sys.stdout.write( "\nStarting processing of data ..." )

# sys.exit(0)

DOI_extract = re.compile( "doi.*" )
DOI_code = re.compile( "10\.[./0-9A-Za-z]+" )
Preprint = re.compile( "Preprint" )

study = []
base_url = "https://doi.org/"

summary = {}

summary[ 'total_studies' ] = n_titles
summary[ 'total_studies_with_DOI' ] = 0

for index in range( len(titles) ):

    title = titles[index]
    reference = refs[index]
    result = results[index]

    sys.stdout.write( '\n\nExtracting DOI ... ' )
    if debug:
        sys.stdout.write( "\nDEBUG: " + str(reference[1]) )

    try:
        DOI_raw = DOI_extract.search( reference[1] )
    except:
        sys.stderr.write( '\nERROR: error extracting raw DOI\n')
        sys.exit(-1)

    if debug:
        sys.stdout.write( "\nDEBUG: " + str(DOI_raw) )        

    if DOI_raw != None:
        if not debug:
            sys.stdout.write("found")

        try:
            DOI = DOI_code.search( DOI_raw.group(0) )
        except:
            sys.stderr.write( '\nERROR: error extracting DOI code from ' + str( DOI_raw.group(0) ) + "\n" )
            sys.exit(-1)

        try:
            DOI_url = base_url + DOI.group(0)
        except:
            sys.stderr.write( '\nERROR: error forming DOI url from ' + str( DOI ) + "\n" )
            sys.exit(-1)            

        sys.stdout.write( "\nChecking DOI data on '" + DOI_url + "' " )

        try:
            response = http.request('GET', DOI_url )
        except urllib3.exceptions.MaxRetryError:
            sys.stderr.write("\nERROR: too many retries") 
            continue
     
        if response.status == 200:
            summary[ 'total_studies_with_DOI' ] += 1

            sys.stdout.write( "OK" )

        else:
            sys.stderr.write("\nERROR: study DOI not found")

    else:
        if not debug:
            sys.stdout.write("not found")


print(summary)

    #sys.stdout.write( "\n" )
    #sys.stdout.write( "\nTitle:" + title )
    #sys.stdout.write( "\nReference: " + reference )
    #sys.stdout.write( "\nResults: " + result )

print('\n')