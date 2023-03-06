from cities_at_k_of_start import *
import pprint as pp

n = 'Geneva'
c = 'CH'
d = 2
s = 4
k = 5

print("""
information about Geneva necessary to compute neighbor criteria:""")
print(retrieve_city_info(n, c))

print("""
neighbors of Geneva:""")
print(neighbors_of_city(n, c, d, s))

print("""
outcome of the final function:""")
result = cities_at_k_of_start(n, c, d, s, k)
pp.pprint(result)
