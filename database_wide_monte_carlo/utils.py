# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:20:44 2024

@author: xtang
"""

import brightway2 as bw
from scipy import sparse



def explicit_inventory(lca) :
    """
    Just like in regular LCA class, diagonalize the supply array, yielding an explicit inventory
    of dimensions m x m, rather than m x 1. Enables tracing which activity yields high contributions 

    inventory results are then accessed by calling ".explicit_inventory" on the object.

    # Inspired from bw2calc.LCA.lci_calculation
    """
    count = len(lca.activity_dict)
    lca.explicit_inventory = lca.biosphere_matrix * \
                              sparse.spdiags([lca.supply_array],[0],count,count)

    return lca

    


def trace_dependent_db(database_name) : 
    """
    Iterate through a database to identify all possible database dependencies
    
    ## Note : if dependencies are not up to date, run a sacrificial LCA first (force update)
    
    """
    
    # pick a random dataset in the target database, run the LCA, to force update direct dependencies
    #bw.LCA({(database_name,bw.Database(database_name).random()):1})
    
    # Make a shallow copy from the 1st layer of dependent databases 
    master_list = list(bw.Database(database_name).metadata['depends'])
    
    # Initiate storage variables
    updated_depends = []
    
    # Initial differences :  
    diff_depends = len(master_list)-len(updated_depends)
    
    # Check all list elements for their own dependent databases :    
    while diff_depends > 0 : 
        
        # Shallow copy of the up to date master list : 
        updated_depends = list(master_list) 
        
        for db in master_list : 
            # Find closest dependents
            dependent_db = bw.Database(db).metadata['depends']
            
            # Add to the copy of the master list
            updated_depends.extend(dependent_db)

            # Clear duplicates
        updated_depends = list(set(updated_depends)) # Clear databases flagged already
        
        # Check if this iteration yields any change : 
        diff_depends = len([x for x in updated_depends if x not in master_list])
    
        master_list = updated_depends
        
    return master_list
