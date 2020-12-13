from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea

session = start_session("sqlite:///database.sqlite")
#data_counties = load_counties(session, filter_empty=True)
data_states = load_states(session)


print(data_states)