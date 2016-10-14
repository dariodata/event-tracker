# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 12:42:10 2016

@author: dario
"""

event-tracker
============

event-tracker is a Python program to track discrete event time series and plot
them for parallel visualization. It also plots histograms of the events by day
of the week.

Applications
------------

Examples include tracking and comparing the occurrence of any event that 
can be documented as (YYYY, MM, DD, HH).

e.g. visits to the cinema, doctor appointments, public appearances, etc.

Dependencies
~~~~~~~~~~~~

event-tracker requires::

- Python (>= 3.3),
- NumPy,
- Pandas,
- Seaborn,
- matplotlib.