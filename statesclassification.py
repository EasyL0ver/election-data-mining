from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
plt.close()

session = start_session("sqlite:///database.sqlite")
data_states = load_states(session, filter_empty=True)

states_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_states)))
vector_labels = data_states[0].get_vector().labels(short=True)

candidate_names = vector_labels[:7]
election_results = states_mat[:, :7]
attributes = states_mat[:,7:]
attributes = normalize(attributes, axis=0)

classes = {0:'rural', 3:'urban', 37:'rural', 36:'urban', 13:'rural', 24:'urban'}

training_X = list(map(attributes.__getitem__, classes.keys())) 
training_T = list(classes.values())

neigh = KNeighborsClassifier(n_neighbors=2)
neigh.fit(training_X, training_T)

predicted_classes = neigh.predict(attributes)

for state, predicted_class in zip(data_states, predicted_classes):
    print(state.facts.area_name + " " + predicted_class)

results = dict()
for class_name in ['urban', 'rural']:
    indices = np.where(predicted_classes == class_name)
    class_election_results = list(map(election_results.__getitem__, indices)) 
    mean_election_results = np.mean(class_election_results, axis=1)
    results[class_name] = mean_election_results.flatten()
    pass

bar_width = 0.3
fig, ax1 = plt.subplots()
x = np.arange(len(candidate_names))
ax1.bar(x - bar_width / 2, results['rural'], bar_width, label='rural')
ax1.bar(x + bar_width / 2, results['urban'], bar_width, label='urban')

ax1.set_xticks(x)
ax1.set_xticklabels(candidate_names)
ax1.legend()
ax1.set_title('Average percentage of votes in rural and urban areas')
vals = ax1.get_yticks()
ax1.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
plt.show()