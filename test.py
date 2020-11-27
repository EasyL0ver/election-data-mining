from dbload import prepare_state_data, load_session, prepare_country_data
from primaryarea import CountyArea

session = load_session("sqlite:///database.sqlite")
data = prepare_country_data(session)
a = data.get_democrat()
b = data.get_republican()
print(data)