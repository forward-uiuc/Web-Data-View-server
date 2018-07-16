# Web Data View Server 
## Installation

### Getting Started

Pull down the entire project to your local folder.

Then 
```
pip install -r requirement.txt
```
to install all required libraries

To run server, run 
```python3 chat.py```.

### Common Problem for MacOS
If some of the libraries are not found when running ```chatup.py```, try adding ```sys.path.append('/usr/local/lib/python2.7/site-packages/')``` before importing them.

### Server specifications
At the bottom of ```chatup.py```, the first two lines are for eventlet localhost and the next two lines are for Kite server.  



## Query Languange Semantics 
### Element-By-Element Operators

A set of different categories of language primitives supported in our framework are shown below.

| Type    | Functions   |
| --------|---------|
| Generic | isdate, isprice, islink, isnumeric   |
| String | len, startswith, endswith, contains, regex |
| Image  | size, location   |
| Position | align (left,right,top,bottom,vertical,horizontal), bounding box |
| Web  | classname, tagname  |
| Visual | location (top, bottom,left,right,middle) |
The fundamental reasons to support different types of primitives are 

1. completeness ofoperators (similar to SQL)
2.  expressives (i.e how much a user could potentially describe using the primitives). 


Each class of primitives is briefly explained below with a simple illustration.Generic functions enable extraction of string in a specific format like date or price. For example, price, available date of a books, URL of book description from an online bookstore could be obtained using generic primitives. String functions provide a variety of ways to extract text information from a webpage. Typically, title text in e‑commerce websites are longest strings. Users could use this insight in “len” primitive to extract titles. Users could specify substring‑based extraction with startswith and endswith functions for additional filtering. Regular expressions are powerful constructs that enable users to reuse queries across multiple webpages with a generic pattern. Image extraction is enabled through bounded box location and image size (height and weight) functions. The fundamental advantage of our method is enabling the user to extract information based on visual layout of the webpage. The position and visual primitives enable the user to extract web elements based on “what user sees” principle. “Align” position primitive extracts a set of web elements that satisfy user’s align criteria. For instance, the news article headings in BBC homepage are top‑aligned i.e their X position varies and Y position remains the same. Users could use this insight to extract news headlines. Visual primitivesenable users to extract information based on their relative location in the webpage. We divide the layout of the webpage into three parts vertically and horizontally. “Top” represents top 30% of the page, bottom represents bottom 30% of the page. Similar definitions are used for left,right and middle. For instance, the BBC news headlines could be extracted by specifying the location criteria as “top”.

Sample Query: select the elements that 

1. have type as "text"
2. have text with length equal or greater than 40 letters and equal or less than 200 letters
3. have HTML tags "H2".

```
{
    "extract" : {

        "fields": [

            {
                "Field_id": "Laptop Title",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":200,"gt":40},             
                "tagName"   : "H2"
                }
            }
    ]
   }

}
```
### GroupBy Operator

In order to support queries that work across different websites, we also provide the GroupBy Operator besides the Element-By-Element Operators.

Sample Query: divide all the elements into groups by className and select the groups that 

1. have equal or greater than 0% and equal or less than 10% area of webpage
2. have more than 15 elements in the group 
3. contain "$" equal or more than 100% of the elements in the group
4. After the three steps above, we may still have a spate of groups. By applying "maximum" field in the query, it will select the group from the result above that have text of maximum font size.


```
{
    "extract" : {

        "fields": [

            {
                "Field_id": "prices",
                "match" : {
                "type" : "text",
                "grouping" : {
                    "by": {"className": true, "prefix": 0},
                    "area": {"gt":0.0, "lt":0.1},
                    "count": {"gt": 15},
                    "contains": {"keys":["$"],"gt":1.0},
                    "maximum": {"fontSize": true}
                }
                }
            }
    ]
   }
}

```


## Relevant Links
[https://flask-socketio.readthedocs.io/en/latest/](https://flask-socketio.readthedocs.io/en/latest/)


[https://developer.chrome.com/extensions/messaging](https://developer.chrome.com/extensions/messaging)



## Contributors
Started by Herbert Wang;


Improved by UIUC CS511 Team3 during Spring 2018: Xinyuan Chen, Wenhan Zhao, Yao Xu, Ramya Narayanaswamy;


Improved by Yanbo Chen during Summer 2018;
