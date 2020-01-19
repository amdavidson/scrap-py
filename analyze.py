#!/usr/bin/env python3

import pandas as pd


def get_resources(string, column, mem):
    try:
        l = mem[string]
    except KeyError:
        l = lf[lf[column].str.match(string, na=False)]['RESOURCE_ID'].unique()
        l.sort()
        mem[string] = l
    return l

def build_resource_dict(df, column):

    id_dict = df.sort_values(['RESOURCE_ID']).groupby(
        [column])['RESOURCE_ID'].unique().apply(list).to_dict()
    return id_dict

def str_arr(arr):
    return ' '.join(str(s) for s in arr)


if __name__ == "__main__":

    sf = pd.read_csv("scrap-dummy.csv", encoding="ISO-8859-1", dtype=str)
    lf = pd.read_csv("lt-dummy.csv", encoding="ISO-8859-1", dtype=str)

    lf['sub_PART_ID'] = lf['PART_ID'].str.slice(0, 5)
    pn_memory = build_resource_dict(lf, 'sub_PART_ID')
    sf['ResourceList_byPN'] = sf.apply(lambda r: str_arr(
        get_resources(r.PART[:6], 'PART_ID', pn_memory)), axis=1)

    wo_memory = build_resource_dict(lf, 'WORKORDER_BASE_ID')
    sf['ResourceList_byWO'] = sf.apply(lambda r: str_arr(
        get_resources(r.WO, 'WORKORDER_BASE_ID', wo_memory)), axis=1)

    print(sf.to_csv())

