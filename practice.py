from datetime import datetime

data = {
    "CUF": [
        0.99,
        0.9,
        0.95,
        0.85,
        0.75,
        0.99,
        0.9,
        0.95,
        0.85,
        0.75,
        0.98,
        0.82
    ],
    "Energy": [
        512,
        531,
        549,
        565,
        612,
        571,
        599,
        545,
        612,
        521,
        569,
        645
    ],
    "PR": [
        0,
        0,
        0,
        0,
        7,
        9,
        3,
        7,
        23,
        8,
        2,
        6
    ],
    "site_Name": [
        "test_site2"
    ],
    "timestamp": [
        "2020-03-09 11:30:00",
        "2020-03-09 11:35:00",
        "2020-03-09 11:40:00",
        "2020-03-09 11:45:00",
        "2020-03-09 12:00:00",
        "2020-03-09 12:05:00",
        "2020-03-09 12:40:00",
        "2020-03-09 12:45:00",
        "2020-03-09 12:55:59",
        "2020-03-09 13:05:00",
        "2020-03-09 13:40:00",
        "2020-03-09 14:45:00"
    ]
}

hour_arr = []
for dt in data['timestamp']:
    #    print(n)
    datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    #    print(datetime_object)
    hour_arr.append(datetime_object.hour)
    # index = datetime_object.hour.index(12)

def get_timestamp_range(start_hour, end_hour, hour_list):
    """
    Take the first index of start_hour and last index of end_hour
    :param hour_list: list of hours fetched from mongodb query
    :param start_hour: range start hour
    :param end_hour: range end hour
    :return: index of start_hour and index of end_hour

    usage:
      >>> get_timestamp_range(12, 2)
      >>> (4, 8)
    """
    index_of_first_hour = hour_list.index(start_hour)
    index_of_last_hour = len(hour_arr) - hour_arr[::-1].index(end_hour) - 1
    return index_of_first_hour, index_of_last_hour


# print("get_timestamp_range ",get_timestamp_range(11, 14, hour_arr))

def get_sum_from_list_block(start_range, end_range, resultant_array):
    sliced_array = resultant_array[start_range:end_range + 1]
    # print("sliced_array", (sliced_array))
    return sum(sliced_array)
# print(get_sum_from_list_block(0, 10, data["PR"]))


def get_sum_between_time_range(start_hour, end_hour, data_array):
    """
    :param start_hour:
    :param end_hour:
    :param data_array:
    :return:
        {
            "CUF": 12,
            "Energy": 100,
            ...
        }
    """
    start_range, end_range = get_timestamp_range(start_hour, end_hour, hour_arr)
    return {
        "start_hour": data_array["timestamp"][start_range],
        "end_hour"  : data_array["timestamp"][end_range],
        "CUF"       : get_sum_from_list_block(start_range, end_range, data_array["CUF"]),
        "Energy"    : get_sum_from_list_block(start_range, end_range, data_array["Energy"]),
        "PR"        : get_sum_from_list_block(start_range, end_range, data_array["PR"]),
    }

# print(get_sum_between_time_range(11, 12, data))


for t in list(set(hour_arr)):
    start_hour = t
    end_hour = start_hour + 1
#    print(start_hour, end_hour)
#    get_timestamp_range(start_hour, end_hour, hour_arr)
    try:
#        start, end = get_sum_between_time_range(start_hour, end_hour, hour_arr)
        print(get_sum_between_time_range(start_hour, end_hour, data))
    except (IndexError, ValueError):
        start, end = None, None


