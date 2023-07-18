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

I created multiple threads and started them. 
Then, I recursively called the Request_thread class in a loop. 
However, in order to speed up the process, I waited for all the threads to finish 
and then used the join method at the end.

Describe how to speed up part 2

I was trying to implement two while loops but unfortunately I kept running into erros.
It works intermittently at the moment



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
   

    requested_fam = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    requested_fam.start()
    requested_fam.join()

    new_fam = Family(requested_fam.get_response())
    tree.add_family(new_fam)
    husband, wife = None, None
    

    list_of_people = list()
    

    husband_id = new_fam.get_husband()

    husband_thread = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
    list_of_people.append(husband_thread)
    

    wife_id = new_fam.get_wife()
    wife_thread = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
    list_of_people.append(wife_thread)

    
    for each_child_id in new_fam.get_children():
        if not tree.does_person_exist(each_child_id): 
            requested_child = Request_thread(f'{TOP_API_URL}/person/{each_child_id}')
            list_of_people.append(requested_child)

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
    listed = queue.Queue()
    listed.put(start_id)

    
    while listed.qsize() > 0:

        def family_thread(id, fam_id, tree):
            if not tree.does_family_exist(fam_id):
                family_request =  Request_thread(f'{TOP_API_URL}/family/{fam_id}')

                family_request.start()
                family_request.join() 
                family = Family(family_request.get_response())   
                tree.add_family(family)
                pers_details = list()
                if family.get_husband():
                    pers_details.append(Request_thread(f'{TOP_API_URL}/person/{family.get_husband()}'))
                if family.get_wife():
                    pers_details.append(Request_thread(f'{TOP_API_URL}/person/{family.get_wife()}'))
                for child in family.get_children():
                    if not tree.does_person_exist(child):
                        pers_details.append(Request_thread(f'{TOP_API_URL}/person/{child}'))

                for j in pers_details:
                    j.start()
                for j in pers_details:
                    j.join() 

                for pers in pers_details:
                    if not tree.does_person_exist(pers.get_response()['id']):
                        person = Person(pers.get_response())
                        tree.add_person(person)
                        if person.get_parentid() != None:
                            id.put(person.get_parentid())
                            # print(person.get_parentid())
        famList = []

        while listed.qsize() > 0:
            name_id = listed.get()
            fam_Thread = threading.Thread(target=family_thread, args=(listed, name_id, tree))
            fam_Thread.start()
            famList.append(fam_Thread)
 
        for fam in famList:
            fam.join()
# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass