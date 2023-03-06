from neighbors_of_city import *


def cities_at_d(at_d_minus_1: set, at_less_than_d: set, d: float, s: float) -> set:
    """
    This function works exactly like nodes_at_d defined during the course, but it was adapted to fit our problem which
    does not work with graphs as we saw them in the lectures (even if the underlying concept of this project heavily
    relies on graphs, we did not build a graph in python directly).

    The function takes a set of (city, country) tuples which are at distance d-1 and a set of (city, country) tuples
    which are at distance < d and finds the set of (city, country) tuples which are at distance d.
    Since it uses the previously defined function neighbors_of_city, it also takes d and s as inputs in order to
    determine which cities are neighboring.

    :param: at_d_minus_1: at_d_minus_1 should be a set of (city, country) tuples where city and country are strings.
    :param: at_less_than_d: at_less_than_d should be a set of (city, country) tuples where city and country are strings.
    :param: d: d should be a float number >= 0.
    :param: s: s should be a float number >= 0.
    :return: dd is a set of (city, country) tuples where city and country are strings. It is the cities at distance d.
    """

    dd = set()
    for y in at_d_minus_1:
        # finding all neighbors of cities which are at distance d-1
        neighbors_of_y = neighbors_of_city(y[0], y[1], d, s)
        for neighbor in neighbors_of_y:
            # adding all the cities we found to dd only if they aren't part of cities at_less_than_d.
            if neighbor not in at_less_than_d:
                dd.add(neighbor)
    return dd


def cities_at_k_of_start(city: str, country: str, d: float, s: float, k: int) -> set:
    """
    This function finds all cities at distance k of the input city, otherwise said at k steps of the input city.

    :param: city: city should be a string which is among the cities listed in table City in the database.
    :param: country: country should be a string which is among the cities listed in table City in the database.
    :param: d: d should be a float number >= 0.
    :param: s: s should be a float number >= 0.
    :param: k: k should be an int number >= 0.
    :return: at_d_minus_1 is a set of (city, country) tuples where city and country are strings.
    It is the cities at k steps of the input city.
    """

    # the function operates by iterating on cities_at_d k times, and the two initial sets should contain only the input
    # (city, country) tuple.
    at_d_minus_1 = {(city, country)}
    at_less_than_d = {(city, country)}
    for i in range(k):
        cities_at_i = cities_at_d(at_d_minus_1, at_less_than_d, d, s)
        at_d_minus_1 = cities_at_i
        at_less_than_d = at_less_than_d.union(cities_at_i)

    return at_d_minus_1
