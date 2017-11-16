#
# coding: utf-8

import requests
import time
import logging
import sys
import json
import sys
import mimetypes



logging.basicConfig(level=logging.DEBUG,stream=sys.stderr)
logger = logging.getLogger(__name__)

class PictureAllianceBadRequest(ValueError) :
    pass

class PictureAllianceClient(object) :

    url = "https://api-test.dpa.com"

    def __init__(self,client_id=None,
                      client_secret=None,
                 application_id=None):
        self.session=requests.session()
        if not (client_id or application_id) :
            raise(ValueError("Must be initialized with either client_id / client_secret or application_id"))
        if client_id is not None :
            self.client=dict(id=client_id,secret=client_secret)
            self.app=None
            self.token=None
        else :
            self.app=application_id
            self.client=None
            self.session.headers["X-ApplicationID"]=self.app


    def hastoken(self) :
        if self.app is not None :
            return True
        if self.token is None:
            return False
        if self.token["not_valid_after"]<time.time()-60 :
            return False
        return True


    def gettoken(self) :
        assert "id" in self.client and  "secret" in self.client
        response=requests.post("{}/oauth/token".format(PictureAllianceClient.url),
                                auth=(self.client["id"],
                                      self.client["secret"]),
                                headers=({"Accept": "application/json"}),
                                data={ "grant_type" : "client_credentials" }
                                )
        if response.status_code < 300 :
            logger.debug("Got Bearer Token")
            self.token=response.json()
            self.token["not_valid_after"]=int(time.time())+self.token["expires_in"]
            self.session.headers["Authorization"]="Bearer {access_token}".format(**self.token)
        else :
            self.token=None




    def get(self,*args,**kwargs) :
        """ make authenticated API call """
        if not self.hastoken() :
            self.gettoken()
        if args[0][0]=="/" :
            # prepend hostname
            thisurl="{}{}".format(PictureAllianceClient.url,args[0])
        else :
            thisurl=args[0]
        return self.session.get(thisurl,*args[1:],**kwargs)

    def post(self,*args,**kwargs) :
        """ make authenticated API call """
        if not self.hastoken() :
            self.gettoken()
        if args[0][0]=="/" :
            # prepend hostname
            thisurl="{}{}".format(PictureAllianceClient.url,args[0])
        else :
            thisurl=args[0]
        thisurl="{}{}".format(PictureAllianceClient.url,args[0])
        return self.session.post(thisurl,**kwargs)


    def search(self,query,**kwargs) :
        """ Returns image search results.
            Parameters include startDate, endDate (case sensitive!),
            date (alternative to startDate/endDate)
            and lang
            Please see API documentation.
        """
        if 'limit' not in kwargs :
            kwargs['limit']=10
        params=dict(query=query)
        params.update(kwargs)
        for pn in ("startDate","endDate","date") :
            v=params.get(pn,None)
            if v is not None and hasattr(v,"strftime") :
                # 1. POST 2. Als JSON
                params[pn]=v.strftime("%Y-%m-%d")
                logging.debug(f"Changed {pn} to {params[pn]}")
        rp={}
        for (k,v) in params.items() :
            if v is not None :
                rp[k]=v
        result=self.post("/open-pa/v1/search/images",json=rp)
        # embed_ipython()
        return PictureAllianceSearchResult(result.json(),api=self,url=result.url)

class PictureAllianceSearchResult(object) :

    __slots__= ('message', 'count', 'images','url','api', '_metadata')


    def __init__(self,d,api=None,url=None) :
        if "results" in d :
            for k in ('count','message') :
                setattr(self,k,d["results"].get(k,None))
            self.url=url
            self.api=api
            self._metadata=None
            if "images" in d["results"] :
                self.images=[ PictureAllianceImage(a["id"],api=api) for a in d["results"]["images"]]
            else :
                self.images=[]
        else:
            raise PictureAllianceBadRequest(repr(d))


    @property
    def metadata(self) :
        if self._metadata is None :
            ids=[ { "id" : a.id } for a in self.images ]
            result=self.api.post("/open-pa/v1/images", json=ids)
            data=result.json()
            self.images=[ PictureAllianceImage(a["id"],api=self.api,metadata=a) for a in data["images"]]
            self._metadata=data["images"]
        return self._metadata



    def __repr__(self) :
        return "PictureAlliance Search Result <[{} ... {}] {} images>".format(self.images[0].id,self.images[-1].id,len(self.images))

class PictureAllianceImage(object) :

    __slots__=  ('api','id','_metadata')


    def __init__(self,id,api,metadata=None) :
        self.id=id
        self.api=api
        self._metadata=metadata


    def __repr__(self) :
        if self._metadata is None :
            metadata="(metadata not loaded)"
        else :
            metadata="metadata {} bytes".format(len(json.dumps(self._metadata)))
        return "<PictureAlliance Image ID {} {}>".format(self.id,metadata)


    @property
    def metadata(self) :
        if self._metadata is None :
            result=self.api.get("/open-pa/v1/images/{}".format(self.id))
            self._metadata=result.json()
        return self._metadata


    def file(self,**kwargs) :
        if "url" in kwargs :
            # url from metadata
            response=self.api.get(kwargs["url"])
        else :
            response=self.api.get("/open-pa/v1/downloads/images/{}".format(self.id),params=kwargs)
        if response.status_code < 300 :
            # import IPython
            # IPython.embed()
            if "content-disposition" not in response.headers :
                response.headers["content-disposition"]='inline; filename="{id}{ext}"'.format(
                       id=self.id,
                       ext=mimetypes.guess_all_extensions(response.headers["content-type"].split(";")[0])[-1])
            return response
        else :
            return None









