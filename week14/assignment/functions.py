"""
Course: CSE 251, week 14
File: functions.py
Author: Joseph Kaku

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    if not family_id:
        return
    
    if tree.does_family_exist(family_id) or family_id == None:
        return
   
    #Retrieve family by id and start and join thread
    # print(f'Getting Family: {family_id}')
    requested_fam = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    requested_fam.start()
    requested_fam.join()
    
    #Create New Family Object and add it to the tree
    new_fam = Family(requested_fam.get_response())
    tree.add_family(new_fam)
    husband, wife = None, None
    
    #Create array to store list of people
    list_of_people = list()
    
    # Let's get the husband and wife's details starting with the husband
    husband_id = new_fam.get_husband()
    # print(f'Getting Husband : {husband_id}')
    husband_thread = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
    list_of_people.append(husband_thread)
    
    #Now let's get the Wife's details
    wife_id = new_fam.get_wife()
    # print(f'Getting Wife    : {wife_id}')
    wife_thread = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
    list_of_people.append(wife_thread)
    
    #Now Let's retrive the children too
    # print(f'Getting children: {str(new_fam.get_children())[1:-1]}')
    
    for each_child_id in new_fam.get_children():
        if not tree.does_person_exist(each_child_id): 
            requested_child = Request_thread(f'{TOP_API_URL}/person/{each_child_id}')
            list_of_people.append(requested_child)
            # requested_child.start()
    for i in list_of_people:
        i.start()   
    for i in list_of_people:
        i.join()
    
    next_gen = list()
    for i in list_of_people:
        person = Person(i.get_response())
        if not tree.does_person_exist(person.get_id()):
            tree.add_person(person)
            next_gen.append(threading.Thread(target=depth_fs_pedigree, args=(person.get_parentid(), tree)))

    for i in next_gen:
        i.start()
    for i in next_gen:
        i.join()

 

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    queue = list()
    queue.append(start_id)
    
    while len(queue) > 0:
        fam_thread = list()
        for fam_id in queue:
            if fam_id == None or tree.does_family_exist(fam_id):
                continue
            fam_thread.append((fam_id, Request_thread(f'{TOP_API_URL}/family/{fam_id}')))
        for _, j in fam_thread:
            j.start()
        for _, j in fam_thread:
            j.join() 
        for fam_id, k in fam_thread:
            pers_details = list()
            family = Family(k.get_response())   
            tree.add_family(family)
            if family.get_husband():
                pers_details.append((family.get_husband(), Request_thread(f'{TOP_API_URL}/person/{family.get_husband()}')))
            if family.get_wife():
                pers_details.append((family.get_wife(), Request_thread(f'{TOP_API_URL}/person/{family.get_wife()}')))
            for child_id in family.get_children():
                pers_details.append((child_id, Request_thread(f'{TOP_API_URL}/person/{child_id}')))
                
        queue = list()
        for _, j in pers_details:
            j.start()
        for _, j in pers_details:
            j.join() 
        
        for _, pers in pers_details:
            person = Person(pers.get_response())
            if tree.does_person_exist(person.get_id()):
                continue
            tree.add_person(person)
            queue.append(person.get_parentid())

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass