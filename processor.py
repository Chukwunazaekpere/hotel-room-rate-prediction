from omp4py import *
from time import time
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import json
import csv


file_names = ["Asokoro", "DiplomaticRes", "Parklane", "Ekiti", "Platinum", "TranstellResidence"]
@omp
def process_DB_data():
    start_time = time()
    room_type_name_dict = {}
    processed_file_name = f"./data/processed_data.csv" # save proceesed records .csv
    header_names = ["Room Rate", "Month Record", "Number of Star", "Hotel Location", "Number of Nights", "Room-type Name"] # model features
    write_processed_file(processed_file_name, header_names) # Write CSV header to processed file
    with omp("for"): # OMP directive for multicore processing
        for count in range(len(file_names)):
            number_of_star = 3 if count < 3 else 4
            hotel_location = "Residence area" if count < 4 else "Commercial area"
            file_name = file_names[count]
            reservation_file_name = f"./data/reservations/{file_name}.json"
            with open(reservation_file_name)as reservation_record: # read reservation files with names as designated by reservation_file_name
                json_record = json.load(reservation_record) # load file as json
                # print("\n\t json_record: ", json_record)
                record_count = 0
                for record in json_record: # collect only 1000 rows
                    room_type_id = get_room_type_id(record, file_name)
                    room_type_file_name = f"./data/roomTypes/{file_name}.json"
                    room_type_res = get_room_type_name(room_type_file_name, room_type_id, room_type_name_dict) 
                    room_type_name = room_type_res['room_type_name']
                    room_type_name_dict = room_type_res['new_room_type_name_dict']
                    try: 
                        data = [
                            record['roomRate'], record['monthRecord'], number_of_star,
                            hotel_location, record["days"], room_type_name
                        ]
                        logging.info(msg=f"\n\t [{time()}]: Writing {record_count+1} record from {file_name} to processed file")
                        write_processed_file(processed_file_name, data) #write processed data to a csv file
                        record_count+=1
                        if record_count > 1000: 
                            logging.info(msg=f"\n\t [{time()}]: End of writing record from {file_name} to processed file")
                            break
                    except Exception as err:
                        logging.info(msg=f"\n\t Exception: {err}")
    logging.info(msg=f"\n\t total time taken: {(time()-start_time)} secs")


def get_room_type_name(room_type_file_name, room_type_id, room_type_name_dict):
    try:
        room_type_name = room_type_name_dict[room_type_id]
        return {"room_type_name": room_type_name, "new_room_type_name_dict": room_type_name_dict}
    except:
        with open(room_type_file_name)as room_type_record: # read room-type files with names as designated by room_type_file_name
            room_type_json_record = json.load(room_type_record) # load room-type file as json
            for room_type_record in room_type_json_record:
                room_type_record_id = room_type_record['_id']
                if room_type_record_id['$oid'] == room_type_id:
                    # print("\n\t room_type_record: ", room_type_record)
                    room_type_name = room_type_record['roomTypeName']
                    room_type_name_dict[room_type_id] = room_type_name
                    return {"room_type_name": room_type_name, "new_room_type_name_dict": room_type_name_dict}


def write_processed_file(file_name, data):
    """Write processed data to csv file"""
    with open(file_name, "+a")as new_processed_data:
        new_csv = csv.writer(new_processed_data, delimiter=",")
        new_csv.writerow(data)



def get_room_type_id(record, file_name):
    """A recursive function for finding the room type-id from both the room-rates & room-types folder"""
    try:
        room_type_obj = record['roomTypeId'] 
        if room_type_obj:
            room_type_id = room_type_obj['$oid']
            return room_type_id
        raise("Object error") # raise an error if object room-type object is not found
    except:
        room_rate_file_name = f"./data/roomRates/{file_name}.json"
        with open(room_rate_file_name)as room_file_data: # open room-rate folder
            room_rate_json_record = json.load(room_file_data) # load room-rate record file as json
            room_details = record['roomDetails'] 
            room_id = room_details['$oid']
            for room_record in room_rate_json_record:
                room_db_id = room_record['_id']
                if room_db_id['$oid'] == room_id:
                    room_type_id = get_room_type_id(room_record, file_name) # recursive call
    return room_type_id


if __name__ == "__main__":
    process_DB_data()