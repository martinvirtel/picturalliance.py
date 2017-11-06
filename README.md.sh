#! /bin/bash

cat <<__END__

# picturealliance.py

This is a demo python client for the API of Picture Alliance. It was tested with their API as of Version V.1.1 dated September 10, 2017. It includes a demo command line tool that can be used for downloading metadata and images. 



## The command line client 
\`\`\`bash
paquery.py 

$(./paquery.py 2>&1 | sed -n '/Usage:/,$p')

\`\`\`


\`SEARCH\`  - the search term.

\`[--limit LIMIT]\`  - limit the download to LIMIT images (please use 100 or less).

\`[--startDate STARTDATE] [--endDate ENDDATE] [--date DATE]\`  - limit the search to DATE or STARTDATE to ENDDATE.

\`[--lang LANG]\`  - search language - de. 

\`[--destination DESTINATION]\`  - specify download directory.

\`[--download DOWNLOAD]\` - specify download format. Can be one of thumb,layout,hires or a comma-separated list.

\`[--filename FILENAME]\`  - specify template for the filename. Default is \`{image.id}_{format}{ext}\`.

\`[--metadata METADATA]\` - specify METADATA filename, or False for "no metadata download". Default is STDOUT.

\`[--loglevel LOGLEVE]\` - specify Python loglevel, one of DEBUG, INFO, ERROR.


### Example 1: Download a thumbnail image of Hamburg's new landmark into the "samples" folder

\`\`\`bash
./paquery.py "Elbphilharmonie" --limit=1 --destination=samples/ --download=thumb --metadata=False


$(./paquery.py "Elbphilharmonie" --limit=1 --destination=samples/ --download=thumb --metadata=False 2>&1)
\`\`\`



### Example 2: Download a layout-sized and a hires-sized image of 2010 or earlier mentioning Hamburg's new landmark into the \'samples\' folder, and the metadata into \`samples/metadata.json\`. 

\`\`\`bash
./paquery.py "Elbphilharmonie" --limit=1 --destination=samples/ \\
             --download=hires,layout --endDate=2010-12-01 --metadata=samples/metadata.json


$(./paquery.py "Elbphilharmonie" --limit=1 --destination=samples/ --download=layout --endDate=2010-12-01 --metadata=samples/metadata.json 2>&1)
\`\`\`



### Example 3: Print Metadata of the image from example 2 to standard output

\`\`\`bash
./paquery.py "Elbphilharmonie" --limit=1 --endDate=2010-12-01 
\`\`\`


\`\`\`json
$(./paquery.py "Elbphilharmonie" --limit=1 --endDate=2010-12-01 | jq .  2>&1)
\`\`\`


### Caveats

While implementing this sample client, there were some things I stumbled upon. This list may help others who
are on the same assignment.


  - The API returns HTTP Error Code 403 if your credentials are wrong, but also if your credentials are right,
  but your IP address is not whitelisted by the API

  - The \`/search\` endpoint parameters startDate, date, endDate do not work with GET. POST works.

  - Some values of \`endDate\` raise a HTTP Error Code 400, for example \`--endDate=2010-12-10\`



__END__



