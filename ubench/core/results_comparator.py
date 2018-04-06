#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#  This file is part of the UncleBench benchmarking tool.                    #
#        Copyright (C) 2017  EDF SA                                          #
#                                                                            #
#  UncleBench is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  UncleBench is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with UncleBench.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                            #
##############################################################################
import os
import pandas as pd
import ubench.data_store.data_store_yaml as dsy

class ResultsComparator:
    
  def __init__(self,context_field_list):
    """ Constructor """
    self.context_fields=context_field_list
    self.context_fields_extended=context_field_list
    self.dstore=dsy.DataStoreYAML()

  def print_comparison(self,result_directories):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None,'expand_frame_repr', False):
      print(self.compare(result_directories))

  def compare(self,result_directories):
    """
    compare results of each result_directory, first directory is considered to contain reference results
    """
    pandas=self.build_pandas(result_directories)
    panda_ref=pandas[0]

    for key_f in self.context_fields_extended:
      if key_f not in panda_ref:
        print('    '+str(key_f)+\
              ' is not a valid context field, valid context fields for given directories are:')
        for cfield in panda_ref:
          print('     - '+str(cfield))
        return "No result"

    result_columns_pre_merge=[ x for x in list(panda_ref.columns.values) if x not in self.context_fields_extended]

    
    # Do all but last merges keeping the original result field name unchanged
    idx=0
    pd_compare=panda_ref
    for pdr in pandas[1:-1]:
      pd_compare=pd.merge(pd_compare,pdr,on=self.context_fields_extended,suffixes=['', '_post_'+str(idx)])
      idx+=1
      
    # At last merge add a _pre suffix to reference result
    if len(pandas)>1:
      pd_compare=pd.merge(pd_compare,pandas[-1],on=self.context_fields_extended,suffixes=['_pre', '_post_'+str(idx)])
    else:
      pd_compare=panda_ref
    
    pd_compare_columns_list=list(pd_compare.columns.values)

    result_columns=[ x for x in pd_compare_columns_list if x not in self.context_fields_extended]
        
    ctxt_columns_list= self.context_fields_extended

    if "nodes" in ctxt_columns_list:
      ctxt_columns_list.insert(0, ctxt_columns_list.pop(ctxt_columns_list.index("nodes")))
    
    pd_compare=pd_compare[ctxt_columns_list+result_columns]

    pd.options.mode.chained_assignment = None # avoid useless warning
    # Convert numeric columns to float
    for ccolumn in self.context_fields_extended:
      try:
        pd_compare[ccolumn]=pd_compare[ccolumn].apply(lambda x: float(x))
      except:
        continue
    
    # Add a difference in % for numeric result columns
    for rcolumn in result_columns_pre_merge:
      pre_column=rcolumn+'_pre'
      for i in range(0,len(pandas[1:])):
        post_column=rcolumn+'_post_'+str(i)
        try:
          pd_compare[rcolumn+' diff_'+str(i)+'(%)']=((pd_compare[post_column].apply(lambda x: float(x))-pd_compare[pre_column].apply(lambda x: float(x)))*100)/pd_compare[pre_column].apply(lambda x: float(x))
        except:
          continue
    pd.options.mode.chained_assignment = 'warn' #reactivate warning
    return(pd_compare.sort(ctxt_columns_list).to_string(index=False))



  def _dir_to_data(self,result_dir):
    data_files=[]
    data_list=[]
    dstore=dsy.DataStoreYAML()

    for (dirpath, dirnames, filenames) in os.walk(result_dir):
      for fname in filenames:
        data_files.append(os.path.join(dirpath,fname))
        
    for dfile in data_files:
      try:
        dstore.load(dfile)
        data_list.append((dstore.runs_info,dstore.metadata))
      except Exception, e:
        print(dfile+" is not a data file and will be ignored : "+str(e))

    return data_list

  def build_pandas(self,result_directories):
    pandas_list=[]
    for result_dir in result_directories:
      pandas_list.append(self._data_to_pandas(self._dir_to_data(result_dir)))

    return pandas_list

  def _data_to_pandas(self,data_list):

    report_info={}
          
    if not data_list:
      # return empty DataFrame
      return pd.DataFrame()
  
    # Choose context fields as an intersection of context fields found in results
    first=True
    for data_b,metadata_b in data_list:
      for id_exec in sorted(data_b.keys()): # this guarantees the order of nodes
        if first:
          context_columns=set(data_b[id_exec]['context_fields'])
        else:
          first=False
          context_columns=context_columns.intersection(set(data_b[id_exec]['context_fields']))

    # Add custom context_columns
    if self.context_fields:
      context_columns=self.context_fields
    else:
      self.context_fields=list(context_columns)      
      context_columns=list(context_columns)

    result_name_column=None
    
    for data_b,metadata_b in data_list:
      for id_exec in sorted(data_b.keys()): # this guarantees the order of nodes
        if (len(data_b[id_exec]['results_bench'].items())>1):
          result_name_column=metadata_b['Benchmark_name']+'_bench'

    for column in context_columns+['result']:
      report_info[column] = []

    if result_name_column:
      report_info[result_name_column] = []

    for data_b,metadata_b in data_list:
      for id_exec in sorted(data_b.keys()): # this guarantees the order of nodes
        value = data_b[id_exec]
        # Only one value for bundle, multiple for hpcc
        for key, result in value['results_bench'].items():
          for column in context_columns:
            report_info[column].append(value[column])
            
          report_info['result'].append(result)
          if result_name_column:
            report_info[result_name_column].append(key)

    if result_name_column:
      self.context_fields_extended=self.context_fields+[result_name_column]
    else:
      self.context_fields_extended=self.context_fields
    
    
    return(pd.DataFrame(report_info))

        


