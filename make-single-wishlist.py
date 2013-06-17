# -*- coding: utf-8 -*-

#===============================================================================
# This reads in all the lists in the input folder and the collection list
# it will make a single wish list that is purged and would bring the collection
# up to 4 of each of the wished for cards
#
# Usage of this script:
#  python make-single-wishlist.py  <folder with lists> <collection file> <output list>
# 
#===============================================================================

import sys
import os.path
import re
import codecs
import sets

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

expected_arguments = 3

# Check for correct script arguments and usage
if (len(sys.argv) != (expected_arguments + 1)):
    print "Incorrect usage!"
    print "Correct usage: python make-single-wishlist.py  <folder with lists> <collection file> <output list>"
    sys.exit(1);
    
# Name of the folder with profiles
list_folder = sys.argv[1]
collection_filename = sys.argv[2]
output_filename = sys.argv[3]

if (not os.path.exists(list_folder) or not os.path.isdir(list_folder)):
    print "Error: List folder must exist and be a directory."
    sys.exit(1);
    
if (not os.path.exists(collection_filename)):
    print "Error: Collection list doesn't exist"
    sys.exit(1);
    
card_num = 0

#import wish-lists
cards_wish_list = []

list_filenames = os.listdir(list_folder)

for list_file in list_filenames:
    
    file = codecs.open(list_folder + "/"+ list_file, 'r', 'utf-8')
    
    for line in file:
        match = re.search('^(?P<num>[0-9]+?) (?P<card_name>.+?)$', line)
        if (match):
            cards_wish_list.append(match.group("card_name").strip())
        
# clean wish list
set = sets.Set(cards_wish_list)
cards_wish_list = list(set)

# import collection
collection_file = codecs.open(collection_filename, 'r', 'utf-8')

cards_in_collection = []

for line in collection_file:

    match = re.search('^(?P<num>[0-9]+?) (?P<card_name>.+?)$', line)
    if (match):
        cards_in_collection.append((match.group("num"),match.group("card_name").strip()))
        
# purge wishlist and output
output_file = codecs.open(output_filename, 'w', 'utf-8')

for card in cards_wish_list:
    num_wanted = 4
    card_name = card
    
    found_owned = False
    
    for owned_card in cards_in_collection:
        if (owned_card[1] == card_name):
            found_owned = True
            if (int(owned_card[0]) < 4):
                this_num_wanted = num_wanted - int(owned_card[0])
                output_file.write(str(this_num_wanted) + " " + card_name + "\n")
            
    if (not found_owned):
        output_file.write(str(num_wanted) + " " + card_name + "\n")