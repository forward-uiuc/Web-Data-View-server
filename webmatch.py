import time
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/')
import webcolors
import ast
import re
from collections import defaultdict
from dateutil.parser import parse
import math


def is_date(string):

    try:
       parse(string)
       return True
    except ValueError:
       return False

def match_isprice(node,flag):

    if flag == '':
        return True

    return match_str_regex(node, "[0-9$\., ]+")


'''def match_eval_true(node, formula):

    x = float(node['text'])
    return eval(formula)'''

def match_num_between(node, low=-math.inf, high=math.inf):

    if node and float(node['text']) > low and float(node['text']) < high:
        return True

    return False



def match_text_length(node, min_length, max_length):

    if min_length == '':
        min_length = 0
    if max_length == '':
        max_length = 99999
    if node and len(node['text'].replace(' ','')) >= min_length and len(node['text'].replace(' ','')) <= max_length:
        return True

    return False

def match_str_contains(node, substring):

    if type(substring) == list:
        flag = True
        for every_string in substring:
            flag = flag and ((node['text'].lower()).find(every_string.lower()) != -1)
        return flag
    if substring == '':
        return True

    if node and ((node['text'].lower()).find(substring.lower()) != -1):
        return True

    return False

def match_str_begins(node, substring):

    if substring == '':
        return True

    if node and ((node['text'].lower()).find(substring.lower()) == 0):
        return True

    return False

def match_str_ends(node, substring):

    if substring == '':
        return True

    if node and ((node['text'].lower()).find(substring.lower()) == (len(node['text']) - len(substring))):
        return True

    return False

def match_isdate(node,flag):

    if flag == '':
        return True
   

    if node and is_date(node['text']):
        return True

    return False

def match_islink(node,flag):

    if flag == '':
        return True
   

    if node and node['tag'] == "A":
        return True

    return False



def match_str_regex(node, regex_string):

    if regex_string == '':
        return True
    searchObj = re.search(regex_string.replace('\[','[').replace('\]',']'), node['text'].replace(' ',''), re.M | re.I)

    for charr in node['text']:
        if charr.isalpha():
            return False

    if node and searchObj:
        #print node
        return True

    return False


def match_font_size(node, font_size):
    if font_size == '' or node['font_size'] == font_size:
        return True
    return False

'''def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def match_font_color(node, font_color):
    if font_color == '':
        return True
    color = node['font_color']
    if color:
        r,g,b, alpha = ast.literal_eval(color.strip("rgba"))
        rgb = []
        rgb.append(r)
        rgb.append(g)
        rgb.append(b)
    try:
        color_name = webcolors.rgb_to_name(rgb)
    except ValueError:
        color_name = closest_colour(rgb)
    if color_name == font_color.lower():
        return True
    else:
        return False
    return False'''

def match_class_name(node, class_name):

    #print("node: ", node)
    if class_name == '' or node['class'] == class_name:
        return True
    return False


def match_all_images(node):

    if node['tag'] == 'IMG':
        return True
    return False

def match_all_nonimages(node):

    if node['tag'] != 'IMG':
        return True
    return False

def is_numericornot(node,flag):

    if flag == '':
        return True
    try:
        int(node['text'])
        if flag == "True" and int(node['text']) > 10:
            return True
        else:
            return False
    except:
        if flag == "True":
            return False
        else:
            return True


def match_boundingbox(node,boxwidth_min,boxwidth_max,boxheight_min,boxheight_max):
    #print("bounding")
    #print(int(node['width']))#,boxwidth_min,boxwidth_max,boxheight_min,boxheight_max
    if (boxwidth_max) != '':
        if int(node['width']) > boxwidth_max:
            return False
    if boxwidth_min != '':
        if int(node['width']) < boxwidth_min:
            return False
    if boxheight_max != '':
        if int(node['height']) > boxheight_max:
            return False
    if boxheight_min != '':
        if int(node['height']) < boxheight_min:
            return False
    return True



def match_startpos(node,boxstartx_min ,boxstarty_min, boxstartx_max,boxstarty_max):
    return True



def match_tagname(node, tagnames):

    if tagnames == "":
        return True
    else:
        return node['tag'] == tagnames


def match_image_size(node, image_minht, image_minwd, image_maxht, image_maxwd):

    if image_minht == '':
        image_minht = 0
    if image_minwd =='':
        image_minwd = 0

    getht = node['height']
    getwd = node['width']

    if image_maxht == '' and image_maxwd == '':
        return True
    if image_maxht == '' and (getwd >= image_minwd and getwd <= image_maxwd):
        return True
    elif image_maxwd == '' and (getht >= image_minht and getht <= image_maxht):
        return True
    elif (getwd >= image_minwd and getwd <= image_maxwd) and (getht >= image_minht and getht <= image_maxht):
        return True
    else:
        return False

def match_image_location(node, image_minx, image_miny, image_maxx, image_maxy):

    if image_minx == '':
        image_minx = 0
    if image_miny =='':
        image_miny = 0

    getxloc = node['x']
    getyloc= node['y']

    if image_maxx == '' and image_maxy == '':
        return True
    if image_maxx == '' and (getyloc >= image_miny and getyloc <= image_maxy):
        return True
    elif image_maxy == '' and (getxloc >= image_minx and getxloc <= image_maxx):
        return True
    elif (getyloc >= image_miny and getyloc <= image_maxy) and (getxloc >= image_minx and getxloc <= image_maxx):
        return True
    else:
        return False

def match_left_align(all_nodes):

    #Group nodes that have same xposition, key is x location, value is list of node numbers
    #print all_nodes
    left_align = defaultdict(list)
    for node in all_nodes:
        xloc = node['x']
        left_align[xloc].append(node['id'])

    #Return the key group with most number of entries
    maxkey = max(left_align.keys(), key=(lambda k: len(left_align[k])))
    return left_align[maxkey]

def match_right_align(all_nodes):

    #Group nodes that have same xposition + width, key is xposition + width, value is list of node numbers
    right_align = defaultdict(list)
    for node in all_nodes:
        xloc = node['x']
        width = node['width']
        right_align[xloc + width].append(node['id'])

    #Return the key group with most number of entries
    maxkey = max(right_align.keys(), key=(lambda k: len(right_align[k])))
    return right_align[maxkey]

def match_bottom_align(all_nodes):

    #Group nodes that have same ypos, key is ypos, value is list of node numbers
    bottom_align = defaultdict(list)
    for node in all_nodes:
        yloc = node['y']
        bottom_align[yloc].append(node['id'])

    #Return the key group with most number of entries
    maxkey = max(bottom_align.keys(), key=(lambda k: len(bottom_align[k])))
    return bottom_align[maxkey]

def match_top_align(all_nodes):

    #Group nodes that have same ypos + height, key is ypos + height, value is list of node numbers
    top_align = defaultdict(list)
    for node in all_nodes:
        yloc = node['y']
        height = node['height']
        top_align[yloc + height].append(node['id'])

    #Return the key group with most number of entries
    maxkey = max(top_align.keys(), key=(lambda k: len(top_align[k])))
    return top_align[maxkey]


def match_vertical_align(all_nodes):

    #Intersection of left and right align
    left_align = match_left_align(all_nodes)
    right_align = match_right_align(all_nodes)

    #print(left_align,right_align)
    return list(set(left_align) & set(right_align))


def match_horizontal_align(all_nodes):

    #Intersection of top and bottom align
    top_align = match_top_align(all_nodes)
    bottom_align = match_bottom_align(all_nodes)

    #print(top_align,bottom_align)
    return list(set(top_align) & set(bottom_align))

def match_location(node,page_xmax,page_ymax,location):

    if location == '':
        return True

    if location == 'top':
        max_y = page_ymax
        min_y = page_ymax*2/3

        if node and int(node['y']) >= min_y and int(node['y']) <= max_y:
            return True

    if location == 'bottom':
        max_y = page_ymax/3
        min_y = 0

        if node and int(node['y']) >= min_y and int(node['y']) <= max_y:
            return True

    if location == 'left':
        max_x = page_xmax
        min_x = page_xmax*2/3

        if node and int(node['x']) >= min_x and int(node['x']) <= max_x:
            return True
    
    if location == 'right':
        max_x = page_xmax
        min_x = page_xmax*2/3

        if node and int(node['x']) >= min_x and int(node['x']) <= max_x:
            return True

    if location == 'middle':
        max_x = page_xmax*2/3
        min_x = page_xmax*1/3
        max_y = page_ymax*2/3
        min_y = page_ymax*1/3

        if node and int(node['x']) >= min_x and int(node['x']) <= max_x:
            return True
        if node and int(node['y']) >= min_y and int(node['y']) <= max_y:
            return True

    return False


def match_grouping_className(node, groups, flag):
    classes = set()
    for x in groups:
        splitted = x.split('/')
        className = splitted[0]
        classes.add(className)

    if flag == True and type(node['class']) is str:
        if node['class'] in classes:
            return True
        else:
            return False
    elif flag == True  and type(node['class']) is not str:
        return False
    else:    
        return True

def match_grouping_prefix(node, groups, prefix):
    if prefix > 0:
        prefixes = []
        for x in groups:
            splitted = x.split('/')
            temp = splitted[1].split(' ')
            del temp[0]
            for y in temp:
                prefixes.append(y)
        my_prefix = node['text'].split()
        # placeholder
        if len(my_prefix) < prefix:
            for i in range(prefix - len(my_prefix)):
                my_prefix.append('nil')
        for i in range(prefix):
            if prefixes[i] != my_prefix[i]:
                return False
        return True
       
    return True


    


def match(all_nodes, tag_name = '', min_length = 0, max_length = sys.maxsize, font_size = '', font_color = '', class_name = '', ext_type = 'text',\
          text_begins = '', text_ends = '', text_contains = '', regex_string = '',\
          image_minht = '', image_minwd = '', image_maxht = '', image_maxwd = '',\
          isdate = '', isprice ='', islink ='', location = '',\
          image_minx = '', image_miny = '', image_maxx = '', image_maxy = '', align = '',isnumeric = '',boxwidth_min = '',
         boxwidth_max = '',boxheight_min = '',
        boxheight_max = '', boxstartx_min = '', boxstarty_min = '',
        boxstartx_max = '', boxstarty_max = '', page_xmin = 0.0, page_xmax = math.inf, page_ymin = 0.0, page_ymax = math.inf,
        grouping_enable = '', grouping_by_className = '', grouping_by_prefix = '',
        grouping_maxarea = '', grouping_minarea = '', grouping_maxcount = '', grouping_mincount = '', 
        grouping_containskeys = '', grouping_maxcontains = '', grouping_mincontains = '', 
        grouping_maximum_fontSize = ''):

    initial_matched_nodes = []
    matched_nodes = []
    additional_filters = []

    initial_groups = {}
    filtered_groups = set()
    if grouping_enable:
        max_area = 0

        # divide all the nodes into groups 
        for node in all_nodes.keys():
            # calculate the total area of the page
            if all_nodes[node]['width'] * all_nodes[node]['height'] > max_area:
                max_area = all_nodes[node]['width'] * all_nodes[node]['height']

            # current structure of group name: "className/prefix" : [{node},{node},{node}]
            keyName = ''
            if grouping_by_className:
                if type(all_nodes[node]['class']) is not str:
                    keyName = keyName + ''
                else:
                    keyName = keyName + all_nodes[node]['class']
            if grouping_by_prefix > 0:
                prefix = ''
                splitted = all_nodes[node]['text'].split()
                keyName = keyName + '/'

                # placeholder
                if len(splitted) < grouping_by_prefix:
                    for i in range(grouping_by_prefix - len(splitted)):
                        splitted.append('nil')

                for i in range(grouping_by_prefix):
                    prefix = splitted[i]
                    keyName = keyName + ' ' + prefix

            if keyName != '' and type(keyName) is str:
                if keyName not in initial_groups.keys():
                    initial_groups[keyName] = []
                    initial_groups[keyName].append(all_nodes[node])
                else:
                    initial_groups[keyName].append(all_nodes[node])

        # filter the groups
        for group in initial_groups.keys():
            # check the number of elements in the current group
            # check the area of of the current group 
            # check if it contains required keys 
            group_count = 0
            group_area = 0
            group_keyoccur = 0
            
            # traverse all the elements in the current group
            for node in initial_groups[group]:
                # get # of elements in the current group
                group_count = len(initial_groups[group])
                # get the area of the current element
                current_area = node['width'] * node['height']
                group_area = group_area + current_area
                # check if any keys are contained in the current element
                for key in grouping_containskeys:
                    if key.lower() in node['text'].lower():
                        group_keyoccur = group_keyoccur + 1
                        break

            percent_area = float(group_area)/max_area
            percent_occur = float(group_keyoccur)/group_count
            if group_count >= grouping_mincount and group_count <= grouping_maxcount:
                if percent_area >= grouping_minarea and percent_area <= grouping_maxarea:
                    if percent_occur >= grouping_mincontains and percent_occur <= grouping_maxcontains:
                        filtered_groups.add(group)

        if grouping_maximum_fontSize:
            max_fontSize = 0
            maximum_groups = set()
            for group in filtered_groups:
                current_fontSize = 0
                for node in initial_groups[group]:
                    fs = int(node['fontSize'].replace('px',''))
                    current_fontSize = current_fontSize + fs
                if current_fontSize > max_fontSize:
                    max_fontSize = current_fontSize

            for group in filtered_groups:
                fs = 0
                for node in initial_groups[group]:
                    fs = fs + int(node['fontSize'].replace('px',''))
                if fs >= max_fontSize:
                    maximum_groups.add(group)
            filtered_groups = maximum_groups


    for node in all_nodes.keys():          
        if ext_type == 'text':
            if match_text_length(all_nodes[node], min_length, max_length) and match_font_size(all_nodes[node], font_size) and match_class_name(all_nodes[node],class_name) and \
               match_str_contains(all_nodes[node],text_contains) and match_str_begins(all_nodes[node],text_begins) and match_str_regex(all_nodes[node],regex_string) \
               and match_str_begins(all_nodes[node],text_ends) and is_numericornot(all_nodes[node], isnumeric) and match_tagname(all_nodes[node], tag_name) and \
               match_location(all_nodes[node],page_xmax,page_ymax,location) and \
               match_boundingbox(all_nodes[node],boxwidth_min,boxwidth_max,boxheight_min,boxheight_max) and match_startpos(all_nodes[node],boxstartx_min ,boxstarty_min,
               boxstartx_max,boxstarty_max) and match_isdate(all_nodes[node], isdate) and match_isprice(all_nodes[node], isprice) and match_islink(all_nodes[node], islink) \
               and match_grouping_className(all_nodes[node], filtered_groups, grouping_by_className) and match_grouping_prefix(all_nodes[node], filtered_groups, grouping_by_prefix): 
                initial_matched_nodes.append(all_nodes[node]['id'])
                additional_filters.append(all_nodes[node])
        if ext_type == 'image':
            if match_all_images(all_nodes[node]) and match_image_size(all_nodes[node],image_minht,image_minwd,image_maxht,image_maxwd) and \
               match_image_location(all_nodes[node], image_minx, image_miny, image_maxx, image_maxy) and match_location(all_nodes[node],page_xmax,page_ymax,location):
                initial_matched_nodes.append(all_nodes[node]['id'])
                additional_filters.append(all_nodes[node])




    if align == 'left':
        matched_nodes = match_left_align(additional_filters)        
        return matched_nodes

    elif align == 'right':
        matched_nodes = match_right_align(additional_filters)        
        return matched_nodes

    elif align == 'top':
        matched_nodes = match_top_align(additional_filters)       
        return matched_nodes

    elif align == 'bottom':
        matched_nodes = match_bottom_align(additional_filters)        
        return matched_nodes

    elif align =='vertical':
        matched_nodes = match_vertical_align(additional_filters)        
        return matched_nodes

    elif align == 'horizontal':
        matched_nodes = match_horizontal_align(additional_filters)        
        return matched_nodes

    else:        
        return initial_matched_nodes
