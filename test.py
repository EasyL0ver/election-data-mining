from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np

session = start_session("sqlite:///database.sqlite")
#data_counties = load_counties(session, filter_empty=True)
data_states = load_states(session)
states_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_states)))

print(data_states)