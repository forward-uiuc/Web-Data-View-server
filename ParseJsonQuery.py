import json,sys,csv

''' Query Parser: The stored queery is in self.parsedquery.

    The helperquery function has details on how to access the stored qery object'''
import re
class ParseJsonQuery:

    def __init__(self,jsonstring):
        #Input json query from front-end as string
        self.inpjson = jsonstring
        #Dictionary object containing parsed query
        self.parsedquery = None
        #self.jsonformat = json.loads(self.inpjson)
        self.ParseInpString()

    def ParseInpString(self):
        json_data = json.loads(self.inpjson)
        #Flatten nested Json with "." as separator
        self.parsedquery =  self.FlattenJson(json_data,".")

    #To flatten a nested json
    def FlattenJson(self,b,delim):
        val = {}
        for i in b.keys():
            if isinstance( b[i], dict ):
                get = self.FlattenJson( b[i], delim )
                for j in get.keys():
                    val[ i + delim + j ] = get[j]
            else:
                val[i] = b[i]

        print("val: ")
        print(val)
        return val


    def helperquery(self):

         fieldlist = self.parsedquery['extract.fields']
         url = self.parsedquery['from.url']

         #This is the number of things to extract. For example, if we have to extract title and price of laptops, this number wil be 2
         num_fields = len(fieldlist)

         for each_field in fieldlist:
              #Unique identifer for every
              identifier = each_field['Field_id']
              #Match params is a dictionary. Key is primitives and value is user-specified value, For example minLength is key with value as 80 from Query1
              matchparams = each_field['match']
              for key, val in matchparams.items():
                print(key)
                print(val)




if __name__ == "__main__":

    query = """ {
        "extract" : {

            "fields": [

                {
                    "Field_id": "Aspire Title",
                    "match" : {
                    "type" : "text",
                    "TextLength" : {"lt":200,"gt":40},
                    "strRegex" : "\\\$[0-9\\\.,\\\]+"
                    }
                }


        ]
       },

      "from" :  {
        "url" : "https://www.amazon.com/s/ref=nb_sb_noss/138-7753184-2542555?url=search-alias%3Delectronics&field-keywords=computer&rh=n%3A172282%2Ck%3Acomputer"

        }

    }

"""
    pq = ParseJsonQuery(query)
    #print pq.ParseInpString()
    pq.ParseInpString()
    a = '\$[0-9\.,]+'
    '''print a
    print re.search(a,'$200.09')
    print re.search( pq.parsedquery['extract.fields'][0]['match']['strRegex'].replace('\[','[').replace('\]',']'),'$1250 - $1499.99 (63)',re.M | re.I)'''
    #pq.helperquery()
