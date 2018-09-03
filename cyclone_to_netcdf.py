#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 13:45:48 2018

Maria J. Molina
Ph.D. Candidate
Central Michigan University

"""

#########################################################################################
#########################################################################################
#########################################################################################


from __future__ import division, print_function

import pandas as pd
import calendar
from datetime import datetime
from datetime import timedelta
import xarray as xr


#########################################################################################
#########################################################################################
#########################################################################################


class cyclone_to_netCDF(object):
    
    
    """
    
    Class for converting cyclone track data into netCDF format files.
    
    
    """

    def __init__(self, 
                 year_init, year_end,
                 month_init, month_end,
                 cyclone_dir, destination_dir):
        
        
        """
        
        Parameters
        ----------
        
        year_init, year_end : YYYY (string)
                              first and last year of dates considered
                              
        month_init, month_end : MM (string)
                                first and last month of dates considered
                                
        cyclone_dir : directory where cyclone tracks are located
        
        destination_dir : where to save the netCDF cyclone tracks
        
        
        Additional Parameters
        ---------------------
        time : time of cyclone in six-hour intervals
        lon : longitude of minimum pressure
        lat : latitude of minimum pressure
        pmin : minimum pressure
        pcont : pressure of outer contour
        idtrack : unique track number
        
        """


        self.year_init = year_init
        self.year_end = year_end
        
        self.month_init = month_init
        self.month_end = month_end

        self.cyclone_dir = cyclone_dir
    
        self.destination_dir = destination_dir
    

        


    def load_cyclone(self):
        
        
        cyclone_dates = pd.date_range(self.year_init+'-'+self.month_init+'-01',
                                      self.year_end+'-'+self.month_end+'-'+str(calendar.monthrange(int(self.year_end),int(self.month_end))[1]),
                                      freq='MS')
    

        cyc_time = []
        cyc_lon = []
        cyc_lat = []
        cyc_pmin = []
        cyc_pcont = []
        cyc_idtrack = []


        for yr_mo in cyclone_dates:
            
            print('Working on month:', yr_mo.strftime('%m'), 'and year:', yr_mo.strftime('%Y'))
            
            
            with open(self.cyclone_dir+'tr_'+yr_mo.strftime('%Y')+yr_mo.strftime('%m'), 'r') as cyclone_data:
                
                contents = cyclone_data.readlines()
                
                
                for line in contents:
                    
                    if len(line) == 91:
                    
                        try:
                    
                            data = [float(x) for x in line.split()]
                            
                            cyc_time.append(data[0])
                            cyc_lon.append(data[1])
                            cyc_lat.append(data[2])
                            cyc_pmin.append(data[3])
                            cyc_pcont.append(data[4])
                            cyc_idtrack.append(data[7])                         
                            
                            
                        except ValueError:
                            
                            #some len(91) lines do not contain actual data
                                #skipping these non-data lines here...
                            
                            continue
                    
        
        correct_time = []
        
        for cychrs in cyc_time:
        
            correct_time.append(datetime(1979, 01, 01, 00, 00, 00) + timedelta(hours=cychrs))
            
            
        
        cyclone_dataset = xr.Dataset({'time':(['length'],correct_time),
                                      'lons':(['length'],cyc_lon),
                                      'lats':(['length'],cyc_lat),
                                      'pmin':(['length'],cyc_pmin),
                                      'pcon':(['length'],cyc_pcont),
                                      'IDtr':(['length'],cyc_idtrack)},
                                      coords={'length':range(len(correct_time))},
                                      attrs={'File Contents':'Converted Cyclone Tracks',
                                             'File Author':'Maria J. Molina'}) 
            

        cyclone_dataset.to_netcdf(self.destination_dir+'cyclone_ready.nc')
        
        print('File saved.')
                    
        return
                    

#########################################################################################
#########################################################################################
#########################################################################################    
