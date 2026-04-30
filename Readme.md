The ``database_wide_monte_carlo`` package, built on the [Brightway2 life cycle assessment framework](http://brightwaylca.org/>),  provides the means to generate precalculated sample arrays for a whole life cycle inventory (LCI) database.

>[!WARNING]
>This is a fork of the original repository. Minor edits have been implemented in this fork to enable the library to operate on a personal computer. 


# Motivation

Precalculating Monte Carlo samples for LCA matrices and associated results (e.g. aggregated LCIs, LCIA scores) can make subsequent LCA calculations much quicker. However, independently calculating Monte Carlo samples for different products in a single database ignores correlation across LCI and LCIA results. 

The ``database_wide_monte_carlo`` uses dependent sampling to generate precalculated sample arrays for a whole database. 

These can then be reused for efficient uncertainty analyses in LCA.

# Structure of results


- each **row** of the precalculated sample arrays represents a specific object (e.g. an input to a given activity, a cradle-to-gate result for a given elementary flow, an LCIA score). Files are generated to inform what each row refers to.  
- each **column** refers to a given Monte Carlo iteration. All arrays have the same number of columns, and each column in any of the arrays was generated with the same Monte Carlo iteration, i.e. with the same initial data in the technosphere and biosphere matrix. 
 

# Types of results

- Arrays with the values sampled for the technosphere matrix **A** and the elementary flow matrix **B** (called the biosphere matrix in Brightway2)
- Supply arrays **s** for unit demands of each activity (i.e. how much each unit process needs to produce to meet a unit of demand for any activity in the database)  
- Inventory arrays **g** for unit demands of each activity, functionaly equivalent to aggregated LCI datasets  
- LCIA score arrays **h** for unit demands of each activity  

# Usage

See the pelicun_2_brightway2 library for usage. 


# Warning - Time and memory!

Some of the steps above (especially `sample_generation.py` and `concatenate_within_jobs.py`) can take lots of time and take up a lot of space.

The current implementation is intended to work with pelicun_2_brightway2 and can take several hours to prepare thousands of samples on a personnal computer (even for small foregrounds).  

Depending on the database size (e.g. applying the algorithm directly to a full-sized ecoinvent database), factor several weeks to a full month for all calculations with a typical personnal computer, and have TBs of disk available.  

To minimize time issues: 
- The more complicated tasks are `embarrassingly parallel <https://en.wikipedia.org/wiki/Embarrassingly_parallel>`_. Distribute your work on as many CPU as you can on your computer, and on multiple computers if you have some available. Note that using multiple computes will require you to move the results of `concatenate_within_jobs.py` to the computer that will eventually aggregate all the results to single arrays. 
- Make sure you use all the CPU you have at your disposal - a server cluster would be the best option.

To minimize disk space issues: 
- Delete samples and temporary files as you go along (`delete_raw_files=True` in `concatenate_within_jobs.py` and `delete_temps=True` in `concatenate_across_jobs.py`)
- Only generate the information you need. Specifically, supply arrays **s** take up lots of space, and are generally not very useful.






# Original Contributors

Chris Mutel (PSI) 

Pascal Lesage (CIRAIG)

Nolwenn Kazoum