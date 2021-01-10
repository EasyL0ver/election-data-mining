from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

session = start_session("sqlite:///database.sqlite")
data_counties = load_counties(session)
counties_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_counties)))

data_states = load_states(session)
states_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_states)))

vector_labels = data_counties[0].get_vector().labels(short=True)
candidate_names = vector_labels[:7]

counties_names = list(map(lambda x: x.facts.area_name, data_counties))
states_names = list(map(lambda x: x.facts.area_name, data_states))

election_results = counties_mat[:, :7]
attributes = counties_mat[:,7:]
reg = LinearRegression(positive=True).fit(attributes, election_results)

actual_state_results = states_mat[:, :7]
state_attributes = states_mat[:,7:]
predicted_state_results = reg.predict(state_attributes)



for i, candidate_name in enumerate(candidate_names):
    actual_results  = actual_state_results[:, i]
    predicted_results = predicted_state_results[:, i]

    zip_results = zip(actual_results, predicted_results, data_states)
    zip_results = sorted(zip_results, key=lambda x: x[0], reverse=True)


    actual, predicted, labels = zip(*zip_results)

    x = np.arange(len(labels))
    width = 0.35 

    fig, ax = plt.subplots()
    ax.bar(x - width/2, actual, width, label='Actual results')
    ax.bar(x + width/2, predicted , width, label='Predicted results')
    ax.set_title("Actual vs predicted results: " + candidate_name)
    ax.set_ylabel("Percentage of votes")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
    ax.legend()
    plt.xticks(rotation=75)
    plt.tight_layout()

plt.show()
pass