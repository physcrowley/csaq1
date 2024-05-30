# File: weather.py

# create data list to hold the records
data = []

""" Read the file """

# field indexes in the data file
month = 6
temp = 13
precip = 23

# extract selected fields from all valid records in the file
with open("./data/en_climate_daily_ON_6106001_2024_P1D.csv", "r") as file:
    for line in file:
        fields = line.strip().split(",")
        # check for completely empty data fields (end of data)
        if fields[temp] == '""' and fields[temp + 1] == '""':
            break
        # strip quotes before adding chosen fields to the record
        record = (
            fields[month].strip('"'),
            fields[temp].strip('"'),
            fields[precip].strip('"'),
        )
        # add the record to the data list
        data.append(record)


""" Compile data from the records """

# initialize collector and flag variables
current_month = data[1][0]
temp_count = 0
temp_sum = 0
precip_sum = 0

# initialize output list with the header record
monthly_data = [data[0]]  
# iterate over other records
for i in range(1, len(data)):
    # unpack the record
    month, temp, precip = data[i]
    # when the month changes
    if month != current_month:
        # create new record for the previous month
        last_month = (current_month, temp_sum / temp_count, precip_sum)
        monthly_data.append(last_month)
        # update the current month
        current_month = month
        # reset the counters
        temp_count = 0
        temp_sum = 0
        precip_sum = 0
    # accumulate data for the current month, skipping missing values
    if len(temp) > 0:
        temp_sum += float(temp)
        temp_count += 1
    if len(precip) > 0:
        precip_sum += float(precip)

# add the last month
last_month = (current_month, temp_sum / temp_count, precip_sum)
monthly_data.append(last_month)

# display the results in a table format
for record in monthly_data:
    # unpack the record
    month, temp, precip = record
    if month == monthly_data[0][0]:
        # header record
        print(f"{month:10} {temp:>15} {precip:>20}")
    else:
        # data records
        print(f"{month:10} {temp:15.1f} {precip:20.1f}")
