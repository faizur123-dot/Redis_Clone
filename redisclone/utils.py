from datetime import datetime, timedelta
import logging
from sortedcontainers import SortedList, SortedSet, SortedDict
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
import json
import pickle

key_value_pair = {}
zdata_store = {}
timeout_key = {}
value_score_map = {}
logger = logging.getLogger(__name__)

def add_key_value(key, value): # To SET the key value pair
    key_value_pair[key]=[]
    key_value_pair[key].append(value)
    return

def get_value_for_key(key): # To GET the value for given key
    load_data_on_start()
    try:
        return key_value_pair[key][0]
    except Exception as e:
        logger.exception('Error: '+str(e))
        return "Key not present"

def set_expiry_time(key, timeout): # Set the timeout
    timeout_key[key] = datetime.now() + timedelta(seconds=timeout)
    return

def delete_key_value(): # Delete key value which have expired
    global key_value_pair, zdata_store, timeout_key, value_score_map
    for key, value in timeout_key.items():
        if datetime.now() > value:
            try:
                if key in key_value_pair.keys():
                    del key_value_pair[key]
                if key in zdata_store.keys():
                    del zdata_store[key]
                if key in value_score_map.keys():
                    del value_score_map[key]
                del timeout_key[key]
            except Exception as e:
                logger.exception("Error:"+str(e))
    return

def store_zdata(key, data): # To store the Z data in a dictionary
    n = len(data)
    if key not in zdata_store:
        zdata_store[key] = SortedDict()
    if key not in value_score_map:
        value_score_map[key] = {}
    cnt = 0
    for i in range(0,n,2):
        if data[i+1] in value_score_map[key].keys():
            temp = value_score_map[key][data[i+1]]
            if len(zdata_store[key][temp]) > 1:
                idx = zdata_store[key][temp].index(data[i+1])
                del zdata_store[key][temp][idx]
            elif len(zdata_store[key][temp]) == 1:
                del zdata_store[key][temp]
        value_score_map[key][data[i+1]] = data[i]
        if data[i] not in zdata_store[key]:
            zdata_store[key][data[i]] = SortedList()
        if data[i+1] not in zdata_store[key][data[i]]: 
            zdata_store[key][data[i]].add(data[i+1])
        cnt = cnt + 1
    print(value_score_map)
    print(zdata_store)
    return cnt

def get_rank_for_value(key, value): # Get the rank for given value
    cnt = 0
    for i, j in zdata_store[key].items():
        if value in j:
            return cnt + j.index(value)
        cnt = cnt + len(j)
    return 'nil'

def get_values_for_range(key, start, stop, is_withscores=None): # To get the values for the given Range
    values = []
    scores = []
    if is_withscores:
        for score, item in zdata_store[key].items():
            if len(item) ==1:
                values.append(list(item))
                values.append(list(score))
            elif len(item)>1:
                for j in item:
                    temp = []
                    temp.append(j)
                    values.append(temp)
                    values.append(list(score))
        print(values)
    else:
        for item in zdata_store[key].values():
            if len(item) ==1:
                values.append(list(item))
            elif len(item)>1:
                for j in item:
                    temp = []
                    temp.append(j)
                    values.append(temp)
    if start < 0:
        start = len(values) - (-1 * start)
    if stop < 0:
        stop = len(values) - (-1 * stop)
    lower = min(start, stop)
    upper = max(start, stop)
    if is_withscores:
        ans = values[2*lower:2*(upper+1)]
    else:
        ans = values[lower:upper+1]
    return ans


def save_data_in_disk(): # Saves data to disk in regular intervals
    global key_value_pair, zdata_store, timeout_key, value_score_map
    try:
        with open('key_value_pair.pkl', 'wb') as fp:
            pickle.dump(key_value_pair, fp)
        with open('zdata_store.pkl', 'wb') as fp:
            pickle.dump(zdata_store, fp)
        with open('timeout_key.pkl', 'wb') as fp:
            pickle.dump(timeout_key, fp)
        with open('value_score_map.pkl', 'wb') as fp:
            pickle.dump(value_score_map, fp)
    except Exception as e:
        print("ERROR SAVING DATA TO DISK: "+str(e))

def load_data_on_start(): # Loads the data from disk upon starting the application
    global key_value_pair, zdata_store, timeout_key, value_score_map
    try:
        with open('key_value_pair.pkl', 'rb') as fp:
            key_value_pair = pickle.load(fp)
        with open('zdata_store.pkl', 'rb') as fp:
            zdata_store = pickle.load(fp)
        with open('timeout_key.pkl', 'rb') as fp:
            timeout_key = pickle.load(fp)
        with open('value_score_map.pkl', 'rb') as fp:
            value_score_map =  pickle.load(fp)
    except Exception as e:
        print("ERROR LOADING DATA: "+str(e))


def clear(): #To clear all the stored data
    global key_value_pair, zdata_store, timeout_key, value_score_map
    key_value_pair.clear()
    zdata_store.clear()
    timeout_key.clear()
    value_score_map.clear()


def add_jobs(): #To schedule periodic tasks
    scheduler.start()
    load_data_on_start()
    job = scheduler.add_job(save_data_in_disk, 'interval' , seconds=10, replace_existing=False)
    job = scheduler.add_job(delete_key_value, 'interval' , seconds=6, replace_existing=True)
    