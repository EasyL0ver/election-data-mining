from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
from factsvector import *

session = start_session("sqlite:///database.sqlite")
#data_counties = load_counties(session, filter_empty=True)
data_states = load_states(session)
state = data_states[0]


fac = FactsVectorFactory()

vector = fac.get_facts_vector(state)

print(data_states)