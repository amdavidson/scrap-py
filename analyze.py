#!/usr/bin/env python3

import pandas as pd

sf = pd.read_csv("scrap-dummy.csv", encoding="ISO-8859-1", dtype=str)
lf = pd.read_csv("lt-dummy.csv", encoding = "ISO-8859-1", dtype=str)


def get_resources_pn(pn, pn_memory):
    try:
        l = pn_memory[pn[:6]]
    except KeyError:
        l = lf[lf['PART_ID'].str.match(pn[:6], na=False)]['RESOURCE_ID'].unique()
        l.sort()
        pn_memory[pn[:6]] = l
    return l

def get_resources_wo(wo, wo_memory):
    try:
        l = wo_memory[wo]
    except KeyError:
        l = lf[lf['WORKORDER_BASE_ID'].str.match(wo,na=False)]['RESOURCE_ID'].unique()
        l.sort()
        wo_memory[wo] = l
    return l

def str_arr(arr):
    return ' '.join(str(s) for s in arr)

lf['sub_PART_ID']=lf['PART_ID'].str.slice(0,5)
pn_memory = lf.sort_values(['RESOURCE_ID']).groupby(['sub_PART_ID'])['RESOURCE_ID'].unique().apply(list).to_dict()
sf['ResourceList_byPN'] = sf.apply(lambda r:
        str_arr(get_resources_pn(r.PART, pn_memory)), axis = 1)


wo_memory = lf.sort_values(['RESOURCE_ID']).groupby(['WORKORDER_BASE_ID'])['RESOURCE_ID'].unique().apply(list).to_dict()
sf['ResourceList_byWO'] = sf.apply(lambda r: 
        str_arr(get_resources_wo(r.WO, wo_memory)), axis = 1)
print(sf.to_csv())

