from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
import matplotlib.pyplot as plt



session = start_session("sqlite:///database.sqlite")
data_states = load_states(session)
states_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_states)))

vector_labels = data_states[0].get_vector().labels(short=True)
candidate_names = vector_labels[:7]

states_names = list(map(lambda x: x.facts.area_name, data_states))

election_results = states_mat[:, :7]
stdev = np.std(election_results, axis=0)
mean = np.mean(election_results, axis=0)
strev = np.reciprocal(stdev)

election_results = np.subtract(election_results, mean)
res = np.multiply(election_results, strev.T)


for i, candidate_name in enumerate(candidate_names):
    candidate_results  = election_results[:, i]
    zip_results = zip(candidate_results, states_names)
    zip_results = sorted(zip_results, key=lambda x: x[0], reverse=True)

    results, labels = zip(*zip_results)
    fig, ax = plt.subplots()
    ax.bar(labels, results)
    ax.set_title("Localization bias towards: " + candidate_name)
    ax.set_ylabel("Standard deviations from average")
    plt.xticks(rotation=75)
    plt.tight_layout()


plt.show()

pass