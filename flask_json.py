# import requests
import json
# from flask import request, Flask,render_template,json
# from html.parser import HTMLParser
import webmatch
import math
from ParseJsonQuery import ParseJsonQuery
from collections import defaultdict


def query_filter(res=None, query = None):
    newres = {}
    cnt = 0

    '''outfile = open('domelement.txt','w')
    for allnode in res:
        outfile.write(json.dumps(allnode) + '\n')'''
        
    for allnode in res:
        if cnt == 0:
            # print('allnode: ')
            # print(allnode)
            cnt += 1
        idnum = str(allnode['id'])
        newres[idnum] = allnode
    res = newres
    try:
        pq = ParseJsonQuery(query)
    except Exception as err:
        print(err)
        return json.dumps({'error' : 'Query is missing or ill formatted'})

    fieldlist = pq.parsedquery['extract.fields']
    #print("length of fieldlist: " + str(len(fieldlist)))
    #print("fieldlist: ")
    #print(fieldlist)
    resdict = {}
    reslist = []
    #This helps in getting more than one field : like price and laptop titles
    for each_field in fieldlist:
        identifier = each_field['Field_id']
        requirements = each_field['match']
        if 'tagName' not in each_field['match']:
            each_field['match']['tagName'] = ''
        tagname = each_field['match']['tagName']






        if "fontColor" not in requirements:
            requirements['fontColor'] = ''
        if "fontSize" not in requirements:
            requirements['fontSize'] = ''
        if "className" not in requirements:
            requirements['className'] = ''
        if "TextLength" not in requirements:
            requirements['minTextLength'] = ''
            requirements['maxTextLength'] = ''
        else:
            requirements['minTextLength'] = ''
            requirements['maxTextLength'] = ''
            if 'lt' in requirements['TextLength']:
                requirements['maxTextLength'] = requirements['TextLength']['lt']
            if 'gt' in requirements['TextLength']:
                requirements['minTextLength'] = requirements['TextLength']['gt']
        if "imgXLoc" not in requirements:
            requirements['imgminXLoc'] = ''
            requirements['imgmaxXLoc'] = ''
        else:
            requirements['imgminXLoc'] = ''
            requirements['imgmaxXLoc'] = ''
            if 'lt' in requirements["imgXLoc"]:
                requirements['imgmaxXLoc'] = requirements["imgXLoc"]['lt']
            if 'gt' in requirements["imgXLoc"]:
                requirements['imgminXLoc'] = requirements["imgXLoc"]['gt']
        if "imgYLoc" not in requirements:
            requirements['imgminYLoc'] = ''
            requirements['imgmaxYLoc'] = ''
        else:
            requirements['imgminYLoc'] = ''
            requirements['imgmaxYLoc'] = ''
            if 'lt' in requirements["imgYLoc"]:
                requirements['imgmaxYLoc'] = requirements["imgYLoc"]['lt']
            if 'gt' in requirements["imgXLoc"]:
                requirements['imgminYLoc'] = requirements["imgYLoc"]['gt']
        if "imgWidth" not in requirements:
            requirements['imgminWidth'] = ''
            requirements['imgmaxWidth'] = ''
        else:
            requirements['imgminWidth'] = ''
            requirements['imgmaxWidth'] = ''
            if 'lt' in requirements["imgWidth"]:
                requirements["imgmaxWidth"] = requirements["imgWidth"]['lt']
            if 'gt' in requirements["imgWidth"]:
                requirements["imgminWidth"] = requirements["imgWidth"]['gt']
        if "imgHeight" not in requirements:
            requirements['imgminHeight'] = ''
            requirements['imgmaxHeight'] = ''
        else:
            requirements['imgminHeight'] = ''
            requirements['imgmaxHeight'] = ''
            if 'lt' in requirements["imgHeight"]:
                requirements["imgmaxHeight"] = requirements["imgHeight"]['lt']
            if 'gt' in requirements["imgHeight"]:
                requirements["imgminHeight"] = requirements["imgHeight"]['gt']


        if "boxwidth" not in requirements:
            requirements['boxminwidth'] = ''
            requirements['boxmaxwidth'] = ''
        else:
            requirements['boxminwidth'] = ''
            requirements['boxmaxwidth'] = ''
            if 'lt' in requirements["boxwidth"]:
                requirements["boxminwidth"] = requirements["boxwidth"]['gt']
            if 'gt' in requirements["boxwidth"]:
                requirements["boxmaxwidth"] = requirements["boxwidth"]['lt']




        if "boxheight" not in requirements:
            requirements['boxminheight'] = ''
            requirements['boxmaxheight'] = ''
        else:
            requirements['boxminheight'] = ''
            requirements['boxmaxheight'] = ''
            if 'lt' in requirements["boxheight"]:
                requirements["boxminheight"] = requirements["boxheight"]['gt']
            if 'gt' in requirements["boxheight"]:
                requirements["boxmaxheight"] = requirements["boxheight"]['lt']





        if "boxstartx" not in requirements:
            requirements['boxstartxmin'] = ''
            requirements['boxstartxmax'] = ''
        else:
            requirements['boxstartxmin'] = ''
            requirements['boxstartxmax'] = ''
            if 'lt' in requirements["boxstartx"]:
                requirements["boxstartxmin"] = requirements["boxstartx"]['gt']
            if 'gt' in requirements["boxstartx"]:
                requirements["boxstartxmax"] = requirements["boxstartx"]['lt']



        if "boxstarty" not in requirements:
            requirements['boxstartymin'] = ''
            requirements['boxstartymax'] = ''
        else:
            requirements['boxstartymin'] = ''
            requirements['boxstartymax'] = ''
            if 'lt' in requirements["boxstarty"]:
                requirements["boxstartymin"] = requirements["boxstarty"]['gt']
            if 'gt' in requirements["boxstarty"]:
                requirements["boxstartymax"] = requirements["boxstarty"]['lt']





        if "beginsWith" not in requirements:
            requirements['beginsWith'] = ''
        if "endsWith" not in requirements:
            requirements['endsWith'] = ''
        if "strContains" not in requirements:
            requirements['strContains'] = ''
        if "strRegex" not in requirements:
            requirements['strRegex'] = ''

        if "align" not in requirements:
            requirements['align'] = ''
        if 'isnumeric' not in requirements:
            requirements['isnumeric'] = ''

        if 'isDate' not in requirements:
            requirements['isDate'] = ''

        if 'isPrice' not in requirements:
            requirements['isPrice'] = ''

        if 'isLink' not in requirements:
            requirements['isLink'] = ''

        if 'location' not in requirements:
            requirements['location'] = ''




        if "grouping" not in requirements:
            requirements['groupingEnable'] = False
            requirements['groupingByClassName'] = False
            requirements['groupingByPrefix'] = 0
            requirements['groupingAreaMin'] = ''
            requirements['groupingAreaMax'] = ''
            requirements['groupingCountMin'] = ''
            requirements['groupingCountMax'] = ''
            requirements['groupingContainsKeys'] = ''
            requirements['groupingContainsMin'] = ''
            requirements['groupingContainsMax'] = ''
            requirements['groupingMaximumFontSize'] = False
        else: 
            requirements['groupingEnable'] = True
            requirements['groupingByClassName'] = False
            requirements['groupingByPrefix'] = 0
            requirements['groupingAreaMin'] = 0.0
            requirements['groupingAreaMax'] = 1.0
            requirements['groupingCountMin'] = 0
            requirements['groupingCountMax'] = math.inf
            requirements['groupingContainsKeys'] = ''
            requirements['groupingContainsMin'] = 0.0
            requirements['groupingContainsMax'] = 1.0
            requirements['groupingMaximumFontSize'] = False

            if 'by' in requirements['grouping']:
                if 'className' in requirements['grouping']['by']:
                    requirements['groupingByClassName'] = requirements['grouping']['by']['className']
                if 'prefix' in requirements['grouping']['by']:
                    requirements['groupingByPrefix'] = requirements['grouping']['by']['prefix']
                # default grouping option
                if not requirements['groupingByClassName'] and requirements['groupingByPrefix'] == 0:
                    requirements['groupingByClassName'] = True

            if 'area' in requirements['grouping']:
                if 'gt' in requirements['grouping']['area']:
                    requirements['groupingAreaMin'] = requirements['grouping']['area']['gt']
                if 'lt' in requirements['grouping']['area']:
                    requirements['groupingAreaMax'] = requirements['grouping']['area']['lt']  

            if 'count' in requirements['grouping']:
                if 'gt' in requirements['grouping']['count']:
                    requirements['groupingCountMin'] = requirements['grouping']['count']['gt']
                if 'lt' in requirements['grouping']['count']:
                    requirements['groupingCountMax'] = requirements['grouping']['count']['lt']

            if 'contains' in requirements['grouping']:
                if 'keys' in requirements['grouping']['contains']:
                    requirements['groupingContainsKeys'] = requirements['grouping']['contains']['keys']
                if 'gt' in requirements['grouping']['contains']:
                    requirements['groupingContainsMin'] = requirements['grouping']['contains']['gt']
                if 'lt' in requirements['grouping']['contains']:
                    requirements['groupingContainsMax'] = requirements['grouping']['contains']['lt']

            if 'maximum' in requirements['grouping']:
                if 'fontSize' in requirements['grouping']['maximum']:
                    requirements['groupingMaximumFontSize'] = requirements['grouping']['maximum']['fontSize']




        #print(requirements)
        # print("type of nodes: ")
        # print(type(res))
        matched_nodes = webmatch.match(res,tag_name = tagname, font_color = requirements['fontColor'],\
                                      font_size=requirements['fontSize'], min_length = requirements['minTextLength'],\
                                      max_length = requirements['maxTextLength'], class_name = requirements['className'], \
                                      ext_type = requirements['type'], text_begins = requirements['beginsWith'], text_ends = requirements['endsWith'],\
                                      text_contains = requirements['strContains'], regex_string = requirements['strRegex'],location = requirements['location'], \
                                      image_minht = requirements['imgminHeight'], image_minwd = requirements['imgminWidth'],\
                                      image_maxht = requirements['imgmaxHeight'], image_maxwd = requirements['imgmaxWidth'], \
                                      image_minx = requirements['imgminXLoc'], image_miny = requirements['imgminYLoc'],\
                                      image_maxx = requirements['imgmaxXLoc'], image_maxy = requirements['imgmaxYLoc'], \
                                      isdate = requirements['isDate'], isprice = requirements['isPrice'], islink = requirements['isLink'],\
                                      align = requirements['align'], isnumeric = requirements['isnumeric'], boxwidth_min = requirements["boxminwidth"],
                                     boxwidth_max = requirements["boxmaxwidth"], boxheight_min = requirements["boxminheight"],
                                    boxheight_max = requirements["boxmaxheight"], boxstartx_min = requirements["boxstartxmin"], boxstarty_min = requirements["boxstartymin"],
                                    boxstartx_max = requirements["boxstartxmax"], boxstarty_max = requirements["boxstartymax"],
                                    ####
                                    grouping_enable = requirements['groupingEnable'], grouping_by_className = requirements['groupingByClassName'], grouping_by_prefix = requirements['groupingByPrefix'],
                                    grouping_maxarea = requirements['groupingAreaMax'], grouping_minarea = requirements['groupingAreaMin'],
                                    grouping_maxcount = requirements['groupingCountMax'], grouping_mincount = requirements['groupingCountMin'],
                                    grouping_containskeys = requirements['groupingContainsKeys'], grouping_maxcontains = requirements['groupingContainsMax'], grouping_mincontains = requirements['groupingContainsMin'],
                                    grouping_maximum_fontSize = requirements['groupingMaximumFontSize'])



        resdict[identifier] = matched_nodes

        # print("matched nodes: ")
        # print(matched_nodes)

    # #print(resdict)
    # records = []
    # for each_field in fieldlist:
    #     identifier = each_field['Field_id']
    #     subres = resdict[identifier]
    #     if len(reslist) == 0:
    #         itemlist = []
    #         for item in subres:
    #             itemlist.append(item)
    #             record = {}
    #             record[identifier] = item
    #             records.append(record)
    #         reslist.append(itemlist)
    #         #print(reslist)
    #     else:
    #         newlist = []
    #         # for item in reslist[0]:
    #         for k in range(len(reslist[0])):
    #             item = str(reslist[0][k])
    #             for newitem in subres:
    #                 temp_item = str(item)
    #                 temp_new = str(newitem)
    #                 itemparent = []
    #                 newparent = []
    #                 for i in range(5):
    #                     #print(res[temp_item])
    #                     if  'parent' in res[temp_item] and int(res[temp_item]['parent']) >= 0:
    #                         itemparent.append(res[temp_item]['parent'])
    #                         temp_item = str(res[temp_item]['parent'])
    #                     if 'parent' in res[temp_new] and int(res[temp_new]['parent']) >= 0:
    #                         newparent.append(res[temp_new]['parent'])
    #                         temp_new = str(res[temp_new]['parent'])
    #                 lca = 9999
    #                 for i in range(len(itemparent)):
    #                     for j in range(len(newparent)):
    #                         if itemparent[i] == newparent[j]:
    #                             lca = min(i, j)
    #                             break
    #                     if lca < 9999:
    #                         break
    #                 if lca < 4:
    #                     newlist.append(newitem)
    #                     records[k][identifier] = newitem
    #         if len(newlist) > 0:
    #             #print(newlist)
    #             reslist.append(newlist)
    # """
# definition of formats:
# records = [ {'title': xxx, 'price': yyy, 'record': zzz}, {'title': aaa, 'price': bbb, 'record':'ccc'} ]
# final_ans = {'title': [xxx, aaa], 'price':[yyy, bbb], 'record':[zzz, ccc]}
# reslist = [[xxx, aaa], [yyy, bbb]]
# """
    # print('resdict: ')
    # print(resdict)
    records = []
    final_ans = {}
    for each_field in fieldlist:
        identifier = each_field['Field_id']
        subres = resdict[identifier]
        # both reslist and records is empty
        if len(reslist) == 0:
            itemlist = []
            for item in subres:
                itemlist.append(item)
                record = {}
                record[identifier] = item
                records.append(record)
            reslist.append(itemlist)
            final_ans[identifier] = itemlist
            #print(reslist)
        # 2nd field of a record, container not found yet
        elif 'record' not in final_ans:
            newlist = []
            containerlist = []
            # for item in reslist[0]:
            # for k in range(len(reslist[0])):
            #     item = str(reslist[0][k])
            #     lcas = []
            #     containers = []
            #     for m in range(len(subres)):
            #         newitem = subres[m]
            #     # for newitem in subres:
            #         temp_item = str(item)
            #         temp_new = str(newitem)
            #         itemparent = []
            #         newparent = []
            #         for i in range(10):
            #             #print(res[temp_item])
            #             if 'parent' in res[temp_item] and int(res[temp_item]['parent']) >= 0 and int(res[temp_item]['parent']) != int(temp_item):
            #                 itemparent.append(res[temp_item]['parent'])
            #                 temp_item = str(res[temp_item]['parent'])
            #             if 'parent' in res[temp_new] and int(res[temp_new]['parent']) >= 0 and int(res[temp_new]['parent']) != int(temp_new):
            #                 newparent.append(res[temp_new]['parent'])
            #                 temp_new = str(res[temp_new]['parent'])
            #         lca = 9999
            #         container = 9999
            #         # if k == 1:
            #         #     print('parent list 1: ')
            #         #     print(itemparent)
            #         #     print('parent list 2: ')
            #         #     print(newparent)
            #         for i in range(len(itemparent)):
            #             for j in range(len(newparent)):
            #                 if itemparent[i] == newparent[j]:
            #                     lca = min(i, j, lca)
            #                     container = itemparent[i]
            #                     break
            #             if lca < 9999:
            #                 break
            #         lcas.append(lca)
            #         containers.append(container)
            #     lca_index = lcas.index(min(lcas))
            #     if min(lcas) < 9999:
            #         newlist.append(subres[lca_index])
            #         records[k][identifier] = subres[lca_index]
            #         records[k]['record'] = containers[lca_index]
            #         containerlist.append(containers[lca_index])
            for k in range(len(reslist[0])):
                item = reslist[0][k]
                diff = []
                # newlist = []
                # containerlist = []
                for m in range(len(subres)):
                    newitem = subres[m]
                    if item > newitem:
                        diff.append(abs(item - newitem) + 1000000)
                    else:
                        diff.append(abs(item - newitem))
                diff_min_idx = diff.index(min(diff))
                newitem = subres[diff_min_idx]
                newlist.append(newitem)
                temp_item = str(item)
                temp_new = str(newitem)
                itemparent = []
                newparent = []
                for i in range(12):
                    #print(res[temp_item])
                    if 'parent' in res[temp_item] and int(res[temp_item]['parent']) >= 0 and int(res[temp_item]['parent']) != int(temp_item):
                        itemparent.append(res[temp_item]['parent'])
                        temp_item = str(res[temp_item]['parent'])
                    if 'parent' in res[temp_new] and int(res[temp_new]['parent']) >= 0 and int(res[temp_new]['parent']) != int(temp_new):
                        newparent.append(res[temp_new]['parent'])
                        temp_new = str(res[temp_new]['parent'])
                # if k == 5:
                    # print('parents: ')
                    # print(itemparent)
                    # print(newparent)
                flag = False
                for i in range(len(itemparent)):
                    for j in range(len(newparent)):
                        if itemparent[i] == newparent[j]:
                            containerlist.append(itemparent[i])
                            flag = True
                            break
                    if flag == True:
                        break
                if flag == False:
                    del newlist[len(newlist)-1]
                else:
                    # if k== 5:
                        # '''print 'ssadasdasdasds'
                        # print itemparent
                        # print newparent'''
                    records[k][identifier] = newitem
                    records[k]['record'] = containerlist[len(containerlist)-1]
                # if k == 5:
                    # print(flag)
                    # print(newlist)
                    # print(containerlist)

            if len(newlist) > 0:
                # print(newlist)
                reslist.append(newlist)
                final_ans['record'] = containerlist
                final_ans[identifier] = newlist
            # else:
                # print("new list: ")
                # print(newlist)
        else:
            newlist = []
            for record in records:
                for k in range(len(subres)):
                    item = subres[k]
                    temp_item = item
                    for i in range(7):
                        if 'parent' in res[str(temp_item)] and int(res[str(temp_item)]['parent']) >= 0:
                            if 'record' in record and int(res[str(temp_item)]['parent']) == record['record']:
                                record[identifier] = item
                                newlist.append(item)
                                # print(k)
                                break
                            else:
                                temp_item = str(res[str(temp_item)]['parent'])
                    if identifier in record:
                        break
            if len(newlist) > 0:
                final_ans[identifier] =  newlist
                reslist.append(newlist)

    # final_ans = defaultdict(list)

    for rec in records:
    	for key,val in rec.items():
    		final_ans[key].append(val)

    # print("mynodes: ")
    # print(final_ans)

    if query:
        # print("reslist: ")
        # print(reslist)
        # print("records: ")
        # print(records)
        # print("Data to front end")
        # print(final_ans)
        if 'record' in final_ans:
            final_ans['records'] = final_ans['record']
            del final_ans['record']
        # return json.dumps({'return_query' : resdict[identifier]})
        return json.dumps(final_ans)

    return json.dumps({'error' : 'Query is missing or URL fetch failed'})



# @app.route('/GetandParse', methods=['POST'])
# def GetandParse():
#     print (request)
#     serialized_nodes = test();
#     query = request.form['query']
#     fid = request.form['fieldid']
#     matchitem = request.form['match']
#     query = "{\"extract\":{\"fields\":[{" + "\"Field_id\":" +    fid     +    ",\"match\":" + ""    +        matchitem        +      ""  + "}]} }"

#     print(query)
#     pq = ParseJsonQuery(query)

#     fieldlist = pq.parsedquery['extract.fields']
#     resdict = {}
#     #This helps in getting more than one field : like price and laptop titles
#     for each_field in fieldlist:
#         identifier = each_field['Field_id']
#         requirements = each_field['match']
#         tagname = each_field['match']['tagName']

#         if "fontColor" not in requirements:
#             requirements['fontColor'] = ''
#         if "fontSize" not in requirements:
#             requirements['fontSize'] = ''
#         if "className" not in requirements:
#             requirements['className'] = ''
#         # if "minTextLength" not in requirements:
#         #     requirements['minTextLength'] = ''
#         # if "maxTextLength" not in requirements:
#         #     requirements['maxTextLength'] = ''






#         if "TextLength" not in requirements:
#             requirements['minTextLength'] = ''
#             requirements['maxTextLength'] = ''
#         else:
#             print('sss')
#             requirements['minTextLength'] = ''
#             requirements['maxTextLength'] = ''
#             if 'lt' in requirements['TextLength']:
#                 requirements['maxTextLength'] = requirements['TextLength']['lt']
#             if 'gt' in requirements['TextLength']:
#                 requirements['minTextLength'] = requirements['TextLength']['gt']
#         if "imgXLoc" not in requirements:
#             requirements['imgminXLoc'] = ''
#             requirements['imgmaxXLoc'] = ''
#         else:
#             requirements['imgminXLoc'] = ''
#             requirements['imgmaxXLoc'] = ''
#             if 'lt' in requirements["imgXLoc"]:
#                 requirements['imgmaxXLoc'] = requirements["imgXLoc"]['lt']
#             if 'gt' in requirements["imgXLoc"]:
#                 requirements['imgminXLoc'] = requirements["imgXLoc"]['gt']
#         if "imgYLoc" not in requirements:
#             requirements['imgminYLoc'] = ''
#             requirements['imgmaxYLoc'] = ''
#         else:
#             requirements['imgminYLoc'] = ''
#             requirements['imgmaxYLoc'] = ''
#             if 'lt' in requirements["imgYLoc"]:
#                 requirements['imgmaxYLoc'] = requirements["imgYLoc"]['lt']
#             if 'gt' in requirements["imgXLoc"]:
#                 requirements['imgminYLoc'] = requirements["imgYLoc"]['gt']
#         if "imgWidth" not in requirements:
#             requirements['imgminWidth'] = ''
#             requirements['imgmaxWidth'] = ''
#         else:
#             requirements['imgminWidth'] = ''
#             requirements['imgmaxWidth'] = ''
#             if 'lt' in requirements["imgWidth"]:
#                 requirements["imgmaxWidth"] = requirements["imgWidth"]['lt']
#             if 'gt' in requirements["imgWidth"]:
#                 requirements["imgminWidth"] = requirements["imgWidth"]['gt']
#         if "imgHeight" not in requirements:
#             requirements['imgminHeight'] = ''
#             requirements['imgmaxHeight'] = ''
#         else:
#             requirements['imgminHeight'] = ''
#             requirements['imgmaxHeight'] = ''
#             if 'lt' in requirements["imgHeight"]:
#                 requirements["imgmaxHeight"] = requirements["imgHeight"]['lt']
#             if 'gt' in requirements["imgHeight"]:
#                 requirements["imgminHeight"] = requirements["imgHeight"]['gt']

#         print(requirements)
#         matched_nodes = webmatch.match(serialized_nodes,tagname,font_color=requirements['fontColor'],\
#                                       font_size=requirements['fontSize'],min_length = requirements['minTextLength'],\
#                                       max_length = requirements['maxTextLength'],class_name=requirements['className'], \
#                                       ext_type = requirements['type'], \
#                                       image_minht = requirements['imgminHeight'],image_minwd = requirements['imgminWidth'],\
#                                       image_maxht = requirements['imgmaxHeight'], image_maxwd = requirements['imgmaxWidth'], \
#                                       image_minx = requirements['imgminXLoc'],image_miny = requirements['imgminYLoc'],\
#                                       image_maxx = requirements['imgmaxXLoc'], image_maxy = requirements['imgmaxYLoc'])



#         resdict[identifier] = matched_nodes




#     if url and query:
#         return json.dumps({'return_url' : request.form['url'], 'return_query' : resdict[identifier]})
#     return json.dumps({'error' : 'Query is missing or URL fetch failed'})
if __name__ == '__main__':
    query = """ {
    "extract" : {

        "fields": [

            {
                "Field_id": "AA",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":100,"gt":80},
                "tagName"   : "H2"
                }
            },

            {
                "Field_id": "BB",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":20, "gt":2},
                "tagName" : "SPAN"
                }
            },

            {
                "Field_id": "CC",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":250,"gt":50},
                "tagName"   : "H2"
                }
            },

            {
                "Field_id": "DD",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":250,"gt":50},
                "tagName"   : "H3"
                }
            }




    ]
   },

  "from" :  {
    "url" : "https://www.amazon.com/s/ref=nb_sb_noss/138-7753184-2542555?url=search-alias%3Delectronics&field-keywords=computer&rh=n%3A172282%2Ck%3Acomputer"

    }

}
"""

    a = [{'id':1,'height':200,'text':'sss','tag':'ss'},{'id':3, 'height':200,'text':'sss','tag':'ss'},{'id':4, 'height':200,'text':'sss','tag':'ss'},{'id':4, 'height':200,'text':'sss','tag':'ss'}]

    print(query_filter(a , query))
