from retrieve_city_info import *


def neighbors_of_city(city: str, country: str, d: float, s: float) -> set:
    """
    This function takes as input a city, a country, a distance d and a distance s. It finds all neighboring cities of
    city, where "being neighbors" is defined as:

    (a) being in the same province OR
    (b) being on the same river OR
    (c) being on the same lake OR
    (d) being at distance < d OR
    (e) being on the same sea but at distance < s

    for the last two points, the distance is computed using longitude and latitude coordinates and the Taxicab norm:
    |city1.longitude − city2.longitude| + |city1.latitude − city2.latitude|

    :param: city: city should be a string which is among the cities listed in table City in the database.
    :param: country: country should be a string which is among the cities listed in table City in the database.
    country is used to distinguish between cities which have the same name so we refer exactly to one line of the table.
    :param: d: d should be a float number >= 0.
    :param: s: s should be a float number >= 0.
    :return: neighbors is a set of tuples of the form (city, country), where city and country are strings. It is the set
    of neighbors of the input city.
    """

    city_info = retrieve_city_info(city, country)
    neighbors = set()

    # CHECK FOR PROVINCE NEIGHBORS
    province = city_info["province"]
    province = f"'{province}'"
    q = "SELECT Name, Country FROM City WHERE Province = " + province
    eq = quote(q)
    url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

    query_results = urlopen(url)
    for line in query_results:
        string_line = line.decode('utf-8').rstrip()
        if len(string_line) > 0:
            columns = string_line.split("\t")
            neighbors.add(tuple(columns))
    query_results.close()

    # CHECK FOR RIVER NEIGHBORS
    if city_info["river"] is not None:
        river = city_info["river"]
        river = f"'{river}'"
        q = "SELECT City, Country FROM located WHERE River = " + river
        eq = quote(q)
        url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

        query_results = urlopen(url)
        for line in query_results:
            string_line = line.decode('utf-8').rstrip()
            if len(string_line) > 0:
                columns = string_line.split("\t")
                neighbors.add(tuple(columns))
        query_results.close()

    # CHECK FOR LAKE NEIGHBORS
    if city_info["lake"] is not None:
        lake = city_info["lake"]
        lake = f"'{lake}'"
        q = "SELECT City, Country FROM located WHERE Lake = " + lake
        eq = quote(q)
        url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

        query_results = urlopen(url)
        for line in query_results:
            string_line = line.decode('utf-8').rstrip()
            if len(string_line) > 0:
                columns = string_line.split("\t")
                neighbors.add(tuple(columns))
        query_results.close()

    # CHECK DISTANCE NEIGHBORS
    if city_info["long_lat"] is not None:
        long_lat = city_info["long_lat"]
        long = f"'{long_lat[0]}'"
        lat = f"'{long_lat[1]}'"
        d = f"'{d}'"
        q = "SELECT Name, Country FROM City WHERE ABS(Longitude-" + long + ") + ABS(Latitude-" + lat + ")<" + d
        eq = quote(q)
        url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

        query_results = urlopen(url)
        for line in query_results:
            string_line = line.decode('utf-8').rstrip()
            if len(string_line) > 0:
                columns = string_line.split("\t")
                neighbors.add(tuple(columns))
        query_results.close()

        # CHECK FOR SEA WITH DISTANCE
        if city_info["sea"] is not None:
            sea = city_info["sea"]
            sea = f"'{sea}'"
            s = f"'{s}'"
            q = """SELECT City.Name, City.Country
                FROM City, located
                WHERE located.City = City.Name
                AND Sea = """ + sea + "AND ABS(Longitude-" + long + ") + ABS(Latitude-" + lat + ")<" + s
            eq = quote(q)
            url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql=" + eq

            query_results = urlopen(url)
            for line in query_results:
                string_line = line.decode('utf-8').rstrip()
                if len(string_line) > 0:
                    columns = string_line.split("\t")
                    neighbors.add(tuple(columns))
            query_results.close()

    # the city itself is included in the set of neighbors, we remove it.
    neighbors.remove((city, country))
    return neighbors
