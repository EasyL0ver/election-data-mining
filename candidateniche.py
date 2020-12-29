from dbload import load_counties, load_states, start_session
from primaryarea import CountyArea
import numpy as np
import matplotlib.pyplot as plt


def calc_niche(mat, candidate_names, attribute_names, factor = 1):
    pos = dict()
    neg = dict()
    for name in candidate_names:
        pos[name] = []
        neg[name] = []

    stddev = np.std(mat)
    tresh = factor * stddev

    for i in range(mat.shape[1]):
        for j in range(mat.shape[0]):
            val = mat[j,i]
            attribute = attribute_names[i]
            candidate = candidate_names[j]
            if val >= tresh:
                pos[candidate].append(attribute)
            elif val <= (-tresh):
                neg[candidate].append(attribute)


    return pos, neg


session = start_session("sqlite:///database.sqlite")
data_counties = load_counties(session, filter_empty=True)

counties_mat = np.array(list(map(lambda x:x.get_vector().numerical(), data_counties)))
vector_labels = data_counties[0].get_vector().labels(short=True)

m = np.corrcoef(counties_mat, rowvar=False)

candidates_mat = m[:7, 7:]
dem_mat = candidates_mat[:2, :]
rep_mat = candidates_mat[2:, :]

democrat_candidate_names = vector_labels[:2]
republican_candidate_names = vector_labels[2:7]
attribute_names = vector_labels[7:]

rep_pos, rep_neg = calc_niche(rep_mat, republican_candidate_names, attribute_names, factor=1)
dem_pos, dem_neg = calc_niche(dem_mat, democrat_candidate_names, attribute_names, factor=1)

pos = {**rep_pos, **dem_pos}
neg = {**rep_neg, **dem_neg}

pi = pos.items()
ni = neg.items()

table_mat = [list(map(lambda x: x[0], pi)), list(map(lambda x: " ".join(x[1]), pi)), list(map(lambda x: " ".join(x[1]), ni))]

print(pos)
print(neg)

plt.table(table_mat)
plt.show()


pass
