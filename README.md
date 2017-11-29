
# picturealliance.py

This is a demo python client for the API of Picture Alliance. It was tested with their API as of [Version V.1.1 dated September 10, 2017][pdf]. It includes a demo command line tool that can be used for downloading metadata and images. 

## Requirements

This client is written in Python 3.6. Requirements are listed in the `requirements.txt` file. 

## The command line client 
```bash
paquery.py 

Usage:       paquery.py SEARCH [LIMIT] [STARTDATE] [ENDDATE] [LANG] [DATE] [DOWNLOAD] [DESTINATION] [FILENAME] [METADATA] [LOGLEVEL]
             paquery.py --search SEARCH [--limit LIMIT] [--startDate STARTDATE] [--endDate ENDDATE] [--lang LANG] [--date DATE] [--download DOWNLOAD] [--destination DESTINATION] [--filename FILENAME] [--metadata METADATA] [--loglevel LOGLEVEL]

```


`SEARCH`  - the search term. You can also use an image id (usually a number like 12412043), or several ids separated by ",".

`[--limit LIMIT]`  - limit the download to LIMIT images (please use 100 or less).

`[--startDate STARTDATE] [--endDate ENDDATE] [--date DATE]`  - limit the search to DATE or STARTDATE to ENDDATE. Not all dates work, please see "Caveats" below. 

`[--lang LANG]`  - search language - de. 

`[--destination DESTINATION]`  - specify download directory.

`[--download DOWNLOAD]` - specify download format. Can be one of thumb,layout,hires or a comma-separated list.

`[--filename FILENAME]`  - specify template for the filename. Default is `{image.id}_{format}{ext}`.

`[--metadata METADATA]` - specify METADATA filename, or False for "no metadata download". Default is STDOUT.

`[--loglevel LOGLEVEL]` - specify Python loglevel, one of DEBUG, INFO, ERROR.


### Example 1: Download a thumbnail image of Hamburg's new landmark into the "samples" folder

```bash
./paquery.py "Elbphilharmonie" --limit=1 --destination=samples/ --download=thumb --metadata=False


INFO:root:samples/66046527_thumb.jpg written
```



### Example 2: Download a layout-sized and a hires-sized image of 2010 or earlier mentioning Hamburg's new landmark into the \'samples\' folder, and the metadata into `samples/metadata.json`. 

```bash
./paquery.py "Elbphilharmonie" --limit=1 --destination=samples/ \
             --download=hires,layout --endDate=2010-12-01 --metadata=samples/metadata.json


INFO:root:samples/57359450_layout.jpg written
```



### Example 3: Print Metadata of the image from example 2 to standard output

```bash
./paquery.py "Elbphilharmonie" --limit=1 --endDate=2010-12-01 
```


```json
{
  "query": "https://api-test.dpa.com/open-pa/v1/search/images",
  "count": 1,
  "message": "MORE_MATCHES_AVAILABLE",
  "result": [
    {
      "id": "57359450",
      "headline": "Ole von Beust wird 60",
      "description": "ARCHIV - Hamburgs damaliger Bürgermeister Ole von Beust (CDU) spricht am 28.05.2010 in Hamburg in der Elbphilharmonie beim Richtfest.  Am 13.04.2015 feiert Ole von Beust seinen 60. Geburtstag. Foto\\ Maurizio Gambarini/dpa (zu dpa «Hamburgs früherer Bürgermeister Ole von Beust wird 60» vom 12.04.2015) +++(c) dpa - Bildfunk+++",
      "subject": [
        {
          "name": ".Leute",
          "rank": 1
        },
        {
          "name": ".Hamburg",
          "rank": 2
        },
        {
          "name": ".CDU",
          "rank": 3
        },
        {
          "name": ".lno",
          "rank": 4
        },
        {
          "name": ".Parteien",
          "rank": 5
        }
      ],
      "creator": "Maurizio Gambarini",
      "date_created": "2010-05-28",
      "credit": "picture alliance / dpa",
      "source": "dpa",
      "rights": "(c) dpa",
      "city": "Hamburg",
      "state": "Hamburg",
      "country": "Deutschland",
      "country_code": "DEU",
      "max_dimensions": {
        "width": 3933,
        "height": 2661
      },
      "resolutions": {
        "hires": {
          "width": 3933,
          "height": 2661,
          "url": "https://api-test.dpa.com/open-pa/v1/downloads/images/57359450?resolution=hires"
        },
        "layout": {
          "url": "https://api-test.dpa.com/open-pa/v1/downloads/images/57359450?resolution=layout"
        },
        "thumb": {
          "url": "https://api-test.dpa.com/open-pa/v1/downloads/images/57359450?resolution=thumb"
        }
      }
    }
  ]
}
```

### Example 4: Download two images by id

```bash

./paquery.py 81454735,81454747 --download=hires --metadata=False
Download:(81454735, 81454747)
INFO:root:./81454735_hires.jpg written
INFO:root:./81454747_hires.jpg written

```



### Caveats

While implementing this sample client, there were some things I stumbled upon. This list may help others. 


  - The API returns HTTP Error Code 403 if your credentials are correct, but your IP address is not whitelisted by the API.

  - The `/search` endpoint parameters `startDate`, `date`, `endDate` do not work with `GET`. `POST` works.

  - Some values of `--date`, `--endDate` and `--startDate` do not work from the command line (but they work when directly using the library `pictuneralliance` module). This is an unexpected behaviour of fire, the python library used to parse the command line parameters. I've filed an [issue](https://github.com/google/python-fire/issues/102) with them for this, maybe they want to change it. This affects every date that can be read as an arithmetics expression. `2018-10-10` will be resolved to `1998`, since `1998` is `2018` minus `10` minus `10`. So for example `--endDate=2010-12-10` fails, but `--endDate=2010-12-09` works.


[pdf]:https://drive.google.com/file/d/0B-BhWVdbxEELNFlIRnkxaFhvblk/view
