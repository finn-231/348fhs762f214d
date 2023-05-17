import os 
import glob #retrieve all the json file paths in the directory
import json

#directory path where json files are stored 
JSON_DIR = 'C:\\Users\\krish\\OneDrive\\Desktop\\Builder'

received_json_files = []

def collect_json_files():
    global received_json_files
    file_paths = glob.glob(os.path.join(JSON_DIR, '*.json'))

    for file_path in file_paths:
        with open(file_path, 'r') as file: 
            try:
                json_data = json.load(file) #the json file is loaded 
                received_json_files.append(json_data)
            
            #an error message is generated if there is an errror decoding
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON file {file_path}: {str(e)}')


collect_json_files()

#print the received json files 
#for json_data in received_json_files: 
#    print(json_data)

#dictionary to store the enter and exit counts for each unique building and room combination
room_data = {}

#itertae to extract the information
for json_data in received_json_files:
    building_number = json_data.get('building_number')
    room_number = json_data.get('room_number')
    enter_count = json_data.get('enter', 0)
    exit_count = json_data.get('exit', 0)

    #if the room already exists in the 'room data' then the enter anc exit counts are updated
    room_key = (building_number, room_number)
    if room_key in room_data:
        room_data[room_key]['enter_count'] += enter_count
        room_data[room_key]['exit_count'] += exit_count
    else:
        room_data[room_key] = {
            'enter_count': enter_count,
            'exit_count': exit_count
        }

#calulate the number of people in the room
for room_key, room_stats in room_data.items():
    building_number, room_number = room_key
    people_inside = room_stats['enter_count'] - room_stats['exit_count']
    print(f"Building {building_number}, Room {room_number}: People inside the room: {people_inside}")