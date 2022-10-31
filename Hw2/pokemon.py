import math
from collections import defaultdict
from collections import Counter
import csv
TYPE_PATH = "pokemon1.txt."
FILE_PATH = "pokemonTrain.csv"
NEW_CSV_PATH = "pokemonResult.csv"
PERSONALITY_PATH = "pokemon4.txt."
HP_PATH = "pokemon5.txt."
A_D_H_THRESHOLD = 40.0
def average(lst):
    ans = 0
    try:
        ans = round(sum([float(x) for x in lst]) / len(lst),1)
    except ZeroDivisionError:
        ans = 0
    return ans
def write_to_file(path,text):
    f = open(path, "w")
    f.write(text)
    f.close()
def read_csv(path):
    csv_dict = []
    with open(path, 'r') as file:
        fieldnames = ["id","name","level","personality","type","weakness","atk","def","hp","stage"]
        reader = csv.DictReader(file,delimiter = ',', fieldnames=fieldnames)
        temp = 0
        for row in reader:
            csv_dict.append(dict(row))
    return csv_dict
def create_csv(path,dict):
    csv_file = path
    fieldnames = ["id","name","level","personality","type","weakness","atk","def","hp","stage"]
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in dict:
                if data["id"] == "id":
                    continue
                writer.writerow(data)
    except IOError:
        print("I/O error")
def get_Fire_Type():
    count = 0
    dict = read_csv(FILE_PATH)
    for pokemon in dict:
        if pokemon["level"]  == "level":
            continue
        if (float(pokemon["level"]) >= float(40) ) and (pokemon["type"] == "fire"):
            count = count + 1
    percentage = 0
    try:
        percentage = round((len(dict) -1) / count)
    except ZeroDivisionError:
        percentage = 0
    value = ("Percentage of fire type pokemon at or above level 40 = " + str(percentage))
    return value

def missing_type():
    dict = read_csv(FILE_PATH)
    tmp_dict = defaultdict(list)
    type_weakness_dict = defaultdict(str)
    for entry in dict:
        if entry["type"]  == "type":
            continue
        if entry["type"]  == "NaN":
            continue
        tmp_dict[entry['type']].append(entry['weakness'])
    for entry in tmp_dict:
        type_weakness_dict[entry] = Counter(tmp_dict[entry]).most_common(1)[0][0]
    for pokemon in dict:
        if pokemon["type"]  == "NaN":
            for type in type_weakness_dict:
                if type_weakness_dict[type] == pokemon["weakness"]:
                    if pokemon["type"]  == "NaN":
                        pokemon["type"] = type
                    elif type < pokemon["type"]:
                        pokemon["type"] = type
               
    return dict

def missing_atk_hp_def():
    dict = read_csv(NEW_CSV_PATH)
    tmp_dict_above_thres = defaultdict(list)
    tmp_dict_below_thres = defaultdict(list)
    above_thres = defaultdict(float)
    below_thres = defaultdict(float)
    for entry in dict:
        if entry["atk"]  == "atk":
            continue
        if entry["atk"]  == "NaN" or entry["def"]  == "NaN" or entry["hp"]  == "NaN":
            continue
        if float(entry["level"]) > A_D_H_THRESHOLD:
            tmp_dict_above_thres['atk'].append(entry['atk'])
            tmp_dict_above_thres['def'].append(entry['def'])
            tmp_dict_above_thres['hp'].append(entry['hp'])
        if float(entry["level"]) <= A_D_H_THRESHOLD:
            tmp_dict_below_thres['atk'].append(entry['atk'])
            tmp_dict_below_thres['def'].append(entry['def'])
            tmp_dict_below_thres['hp'].append(entry['hp'])
    for entry in tmp_dict_above_thres:
        above_thres[entry] = average(tmp_dict_above_thres[entry])
    for entry in tmp_dict_below_thres:
        below_thres[entry] = average(tmp_dict_below_thres[entry])
    for pokemon in dict:
        if pokemon["atk"]  == "NaN":
            if float(pokemon["level"]) > A_D_H_THRESHOLD:
                pokemon["atk"] = above_thres["atk"]
            if float(pokemon["level"]) <= A_D_H_THRESHOLD:
                pokemon["atk"] = below_thres["atk"]
        if pokemon["def"]  == "NaN":
            if float(pokemon["level"]) > A_D_H_THRESHOLD:
                pokemon["def"] = above_thres["def"]
            if float(pokemon["level"]) <= A_D_H_THRESHOLD:
                pokemon["def"] = below_thres["def"]
        if pokemon["hp"]  == "NaN":
            if float(pokemon["level"]) > A_D_H_THRESHOLD:
                pokemon["hp"] = above_thres["hp"]
            if float(pokemon["level"]) <= A_D_H_THRESHOLD:
                pokemon["hp"] = below_thres["hp"]
    return dict

def get_Personality():
    dict = read_csv(NEW_CSV_PATH)
    tmp_dict = defaultdict(list)
    for pokemon in dict:
        if pokemon["personality"]  == "personality":
            continue
        tmp_dict[pokemon["type"]].append(pokemon["personality"] )
    value = ("Pokemon type to personality mapping:\n\n")
    for entry in sorted(tmp_dict):
        value = value + str(entry) + ": "
        temp = " ".join(str(x) for x in sorted(list(set(tmp_dict[entry])))).replace(" ",", ")
        value = value + str(temp) + "\n"
        
    return value

def get_Hp():
    count = 0
    dict = read_csv(NEW_CSV_PATH)
    temp = []
    for pokemon in dict:
        if pokemon["stage"]  == "stage":
            continue
        if float(pokemon["stage"]) == 3.0:
            count = count + 1
            temp.append(pokemon["hp"])
    value = ("Average hit point for pokemon of stage 3.0 = " + str(average(temp)))
    return value 

def main():
    write_to_file(TYPE_PATH,get_Fire_Type())
    create_csv(NEW_CSV_PATH,missing_type())
    create_csv(NEW_CSV_PATH,missing_atk_hp_def())
    write_to_file(PERSONALITY_PATH,get_Personality())
    write_to_file(HP_PATH,get_Hp())
main()