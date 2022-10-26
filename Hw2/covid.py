import math
from collections import defaultdict
from collections import Counter
import csv
FILE_PATH = "covidTrain.csv"
NEW_PATH = "covidResult.csv"
FIELD_NAMES = ["ID","age","sex","city","province","country","latitude","longitude","date_onset_symptoms","date_admission_hospital","date_confirmation","symptoms"]
def most_frequent(my_list): 
    counter = 0 
    num = my_list[0] 
    for i in my_list: 
        curr_frequency = my_list.count(i) 
        if(curr_frequency > counter):
            counter = curr_frequency  
            num = i 
        if(curr_frequency == counter):
            if num > i :
                counter = curr_frequency  
                num = i
    return num
def average(lst):
    ans = 0
    try:
        ans = round(sum([float(x) for x in lst]) / len(lst),2)
    except ZeroDivisionError:
        ans = 0
    return ans
def read_csv(path):
    csv_dict = []
    with open(path, 'r') as file:
        reader = csv.DictReader(file,delimiter = ',', fieldnames=FIELD_NAMES)
        temp = 0
        for row in reader:
            csv_dict.append(dict(row))
    return csv_dict
def create_csv(path,dict):
    csv_file = path
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
            writer.writeheader()
            for data in dict:
                if data["ID"] == "ID":
                    continue
                writer.writerow(data)
    except IOError:
        print("I/O error")

def age_helper_method(input):
    try:
        a = input.index('-')
        ends = input.split('-')
        return round((float(ends[0]) + float(ends[1])) /2)
    except ValueError:
        return input

def date_helper_method(input):
    try:
        a = input.index('.')
        ends = input.split('.')
        return str(ends[1]) + "." + str(ends[0]) + "." +str(ends[2])
    except ValueError:
        return input

def edit_age():
    dict = read_csv(FILE_PATH)
    for patient in dict:
        if patient["age"]  == "age":
            continue
        patient["age"]  = age_helper_method(patient["age"])
    return dict

def edit_date_format():
    dict = read_csv(NEW_PATH)
    for patient in dict:
        if patient["date_onset_symptoms"]  == "date_onset_symptoms":
            continue
        patient["date_onset_symptoms"]  = date_helper_method(patient["date_onset_symptoms"])
        patient["date_admission_hospital"]  = date_helper_method(patient["date_admission_hospital"])
        patient["date_confirmation"]  = date_helper_method(patient["date_confirmation"])
    return dict

def edit_lat_and_long():
    dict = read_csv(NEW_PATH)
    tmp_lat_dict = defaultdict(list)
    tmp_long_dict = defaultdict(list)
    avg_lat = defaultdict(float)
    avg_long = defaultdict(float)
    for patient in dict:
        if patient["province"]  == "province":
            continue
        if patient["latitude"]  != "NaN":
            tmp_lat_dict[patient["province"]].append(patient["latitude"])
        if patient["longitude"]  != "NaN":
            tmp_long_dict[patient["province"]].append(patient["longitude"])
        
    
    for entry in tmp_lat_dict:
        avg_lat[entry] = average(tmp_lat_dict[entry])
    for entry in tmp_long_dict:
        avg_long[entry] = average(tmp_long_dict[entry])

    for patient in dict:
        if patient["province"]  == "province":
            continue
        if patient["latitude"] == "NaN":
            patient["latitude"] = str(avg_lat[patient["province"]])
        if patient["longitude"] == "NaN":
            patient["longitude"] = str(avg_lat[patient["province"]])
    return dict

def edit_city():
    dict = read_csv(NEW_PATH)
    province_dict = defaultdict(list)
    temp = []
    for patient in dict:
        if patient["city"]  == "city":
            continue
        if patient["city"]  != "NaN":
            province_dict[patient["province"]].append(patient["city"])
    
    for prov in province_dict:
        province_dict[prov] = most_frequent(province_dict[prov])
        
    for patient in dict:
        if patient["city"]  == "NaN":
            patient["city"] = province_dict[patient["province"]]
    return dict

def edit_symp():
    dict = read_csv(NEW_PATH)
    symp_dict = defaultdict(list)
    temp = []
    for patient in dict:
        if patient["province"]  == "province":
            continue
        if patient["symptoms"]  != "NaN":
            symp_dict[patient["province"]] = [word.strip() for word in patient["symptoms"].split(';')]
    
    for prov in symp_dict:
        symp_dict[prov] = most_frequent(symp_dict[prov])
    
    for patient in dict:
        if patient["symptoms"]  == "NaN":
            patient["symptoms"] = symp_dict[patient["province"]]
    return dict
def main():
    create_csv(NEW_PATH,edit_age())
    create_csv(NEW_PATH,edit_date_format())
    create_csv(NEW_PATH,edit_lat_and_long())
    create_csv(NEW_PATH,edit_city())
    create_csv(NEW_PATH,edit_symp())
main()