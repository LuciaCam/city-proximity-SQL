from urllib.request import urlopen
from urllib.parse import quote


def retrieve_city_info(city: str, country: str) -> dict:
    """
    This function takes as input a city and country and queries the Mondial database to know:

    (a) which province is the city in (province has no NULL values, it is always defined for each city);
    (b) if the city has longitude and latitude coordinates (can be NULL, in which case long_lat will be None);
    (c) if the city is on a river (can be NULL, in which case river will be None);
    (d) if the city is on a lake (can be NULL, in which case lake will be None);
    (e) if the city is on a sea (can be NULL, in which case sea will be None).

    The function gives the result of its search as a dictionary in the following shape:
    {"province": province,
     "long_lat": long_lat,
     "river": river,
     "lake": lake,
     "sea": sea}

    :param: city: city should be a string which is among the cities listed in table City in the database.
    :param: country: country should be a string which is among the cities listed in table City in the database.
    country is used to distinguish between cities which have the same name so we refer exactly to one line of the table.
    :return: result is a dictionary as shown above, where keys are strings and the values are attributes of the city.
    province will always be a string, the other four can have value None. If the values aren't None, long_lat is a tuple
    containing two floats and river, lake and sea are strings.
    """

    # This allows to put double quotes around single quotes to a string: if city is Geneva, city becomes "'Geneva'".
    city = f"'{city}'"
    country = f"'{country}'"

    # retrieve province, longitude and latitude
    q = "SELECT Province, Longitude, Latitude FROM City WHERE Name = " + city + " AND Country = " + country
    eq = quote(q)
    url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

    query_results = urlopen(url)
    for line in query_results:
        string_line = line.decode('utf-8').rstrip()
        if len(string_line) > 0:
            city_pro_long_lat = string_line.split("\t")
    query_results.close()

    # province is always defined, no NULL values:
    province = city_pro_long_lat[0]

    # longitude and latitude can be NULL. We check for their presence and attribute them
    if len(city_pro_long_lat) == 3:
        longitude = float(city_pro_long_lat[1])
        latitude = float(city_pro_long_lat[2])
        long_lat = (longitude, latitude)
    else:
        long_lat = None

    # check if city has a river. Value can be NULL.
    river = None
    q = "SELECT River FROM located WHERE City = " + city + " AND Country = " + country
    eq = quote(q)
    url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

    query_results = urlopen(url)
    for line in query_results:
        string_line = line.decode('utf-8').rstrip()
        if len(string_line) > 0:
            river = string_line
    query_results.close()

    # check if city has a lake. Value can be NULL.
    lake = None

    q = "SELECT Lake FROM located WHERE City = " + city + " AND Country = " + country
    eq = quote(q)
    url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

    query_results = urlopen(url)
    for line in query_results:
        string_line = line.decode('utf-8').rstrip()
        if len(string_line) > 0:
            lake = string_line
    query_results.close()

    # check if city has a sea. Value can be NULL.
    sea = None

    q = "SELECT Sea FROM located WHERE City = " + city + " AND Country = " + country
    eq = quote(q)
    url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

    query_results = urlopen(url)
    for line in query_results:
        string_line = line.decode('utf-8').rstrip()
        if len(string_line) > 0:
            sea = string_line
    query_results.close()

    result = {"province": province,
              "long_lat": long_lat,
              "river": river,
              "lake": lake,
              "sea": sea}
    return result
