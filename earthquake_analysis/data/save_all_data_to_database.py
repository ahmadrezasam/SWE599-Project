import os
import datetime
from api.models import Earthquake 

def populate_db_from_txt(file_path):
    missing_values_lines = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file.readlines()[1:], start=1):  # Skip the header line
            data = line.strip().split('\t')
            
            # print("Processing line: {}".format(data))
            
            if len(data) == 15:
                _, event_id, date_str, time_str, lat, lon, depth, magnitude, md, ml, mw, ms, mb, event_type, location = data

                try:
                    # Convert date and time strings to Python datetime objects
                    date = datetime.datetime.strptime(date_str, '%Y.%m.%d')
                    origin_time = datetime.datetime.strptime(time_str, '%H:%M:%S.%f').time()

                    # Convert latitude, longitude, depth, magnitude, and other numerical values to float
                    latitude = float(lat) if lat.strip() else None
                    longitude = float(lon) if lon.strip() else None
                    depth = float(depth) if depth.strip() else None
                    magnitude = float(magnitude) if magnitude.strip() else None
                    md_value = float(md) if md.strip() else None
                    ml_value = float(ml) if ml.strip() else None
                    mw_value = float(mw) if mw.strip() else None
                    ms_value = float(ms) if ms.strip() else None
                    mb_value = float(mb) if mb.strip() else None
                    
                    # Check if event_id already exists
                    if Earthquake.objects.filter(event_id=event_id).exists():
                        print(f"Event ID {event_id} already exists. Skipping insertion.")
                        continue

                    # Create and save Earthquake instance
                    earthquake = Earthquake(
                        event_id=event_id,
                        date=date,
                        origin_time=origin_time,
                        latitude=latitude,
                        longitude=longitude,
                        depth=depth,
                        magnitude=magnitude,
                        md=md_value,
                        ml=ml_value,
                        mw=mw_value,
                        ms=ms_value,
                        mb=mb_value,
                        event_type=event_type,
                        location=location
                    )
                    earthquake.save()
                except ValueError as e:
                    print(f"Error processing line {line_num}: {data}. Error: {e}")
            else:
                print(f"Line {line_num} is missing values. Saving to separate file.")
                missing_values_lines.append(line)

    if missing_values_lines:
        missing_values_file_path = os.path.splitext(file_path)[0] + '_missing_values.txt'
        with open(missing_values_file_path, 'w') as missing_values_file:
            missing_values_file.writelines(missing_values_lines)
            print(f"Lines with missing values saved to file: {missing_values_file_path}")

def save_all_txt_to_database(directory_path):
    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            populate_db_from_txt(file_path)
            print(f"Database populated from file: {filename}")

# Directory containing downloaded text files
directory_path = r'.\data\files2'

# Delete existing data in the database
# Earthquake.objects.all().delete()

# Save all text files in the directory to the database
save_all_txt_to_database(directory_path)
