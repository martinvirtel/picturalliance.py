
import json
import logging
import mimetypes
import os
import sys
import re

logger=logging.getLogger('')

from picturealliance import PictureAllianceClient

def cmdline(search,limit=2,
            startDate=None,
            endDate=None,
            lang=None,
            date=None,
            download=False,
            destination="./",
            filename="{image.id}_{format}{ext}",
            metadata=True,
            loglevel='INFO') :
    """
    paquery.py
    Fetch image metadata and images from Picture Alliance API
    """
    if hasattr(logging,str(loglevel).upper()) :
        logger.setLevel(getattr(logging,str(loglevel).upper()))
    try :
        import credentials
    except ImportError :
        logger.error("Please provide a credentials.py file. See example_credentials.py for a template.")
        sys.exit()

    if type(download) == str :
        download=(download,)
    # For production use: Use OAuth2
    # pa=PictureAllianceClient(client_id=credentials.CLIENT_ID,client_secret=credentials.CLIENT_SECRET)
    # for Picturepunk: Use just API_KEY
    pa = PictureAllianceClient(application_id=credentials.API_KEY)
    if re.search(r"(\d{6,}+,)+", search)  :
        imageids=re.split(r" *, *",search)
        print("Download:{}".format(imageids))
        result=PictureAllianceSearchResult({ "results" : { "images" : { "id" : a for a in imageids } } }, api=pa)
    else :
        result=pa.search(search,limit=limit,startDate=startDate,endDate=endDate,lang=lang,date=date)
    if metadata:
        if metadata == True :
            out=sys.stdout
        else :
            out=open(metadata,"w")
        out.write(json.dumps({ "query": result.url, "count": result.count, "message": result.message, "result" : result.metadata}))
    if download :
        for image in result.images :
            res=image.metadata["resolutions"]
            for format in download :
                if format in res :
                    ro=image.file(url=res[format]["url"])
                    ext=mimetypes.guess_all_extensions(ro.headers["content-type"].split(";")[0])[-1]
                    fn=os.path.join(destination,filename.format(**locals()))
                    with open(fn,"wb") as fo:
                        fo.write(ro.content)
                        logger.info(f"{fo.name} written")
                else :
                    formats=",".join(res.keys())
                    logger.error(f"Format {download} not offered for {img}. Possible formats: {formats}")
                    break



