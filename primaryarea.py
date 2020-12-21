from math import floor
import re
from factsvector import *


class ResultBase:
    def __init__(self):
        self.votes = dict()
        self.votes_count = 0

    def get_candidate_fraction(self, candidate_name):
        if candidate_name not in self.votes:
            return 0

        candidate_votes = self.votes[candidate_name]

        if candidate_votes == 0:
            return 0
        
        return float(candidate_votes / self.votes_count)

class Result(ResultBase):
    def __init__(self, data):
        super().__init__()

        votes_sum = 0
        fraction_sum = 0
        for element in data:
            self.votes[element.candidate] = element.votes
            votes_sum += element.votes
            fraction_sum += element.fraction_votes

        if(votes_sum != 0):
            self.votes_count = votes_sum / fraction_sum
        else:
            self.votes_count = 0
            
class AggregateResult(ResultBase):
    def __init__(self, results):
        super().__init__()

        for child_dict in results:
            self.votes_count += child_dict.votes_count
            for key, value in child_dict.votes.items():

                if(key not in self.votes):
                    self.votes[key] = 0
                
                self.votes[key] += value
        
class Area:
    def __init__(self, area_facts):
        self.facts = area_facts
        self.democrat = None
        self.republican = None

    def get_vector(self):
        fac = FactsVectorFactory()
        return fac.get_complete_vector(self)

    def __repr__(self):
        return self.facts.area_name + " " + self.facts.state_abbreviation

    def is_valid(self):
        return self.democrat.votes_count != 0 or self.republican.votes_count != 0

class CountyArea(Area):
    def __init__(self, area_facts):
        super().__init__(area_facts)
        primary_results = area_facts.primary_results_collection

        republican_results = filter(lambda x:x.party == 'Republican', primary_results)
        democrat_results = filter(lambda x:x.party == 'Democrat', primary_results)

        self.democrat = Result(list(democrat_results))
        self.republican = Result(list(republican_results))

class AggregateArea(Area):
    def __init__(self, child_areas, area_facts):
        super().__init__(area_facts)
        self.child_areas = child_areas

        democrat_dicts = map(lambda x: x.democrat, self.child_areas)
        republican_dicts = map(lambda x: x.republican, self.child_areas)

        self.democrat = AggregateResult(list(democrat_dicts))
        self.republican = AggregateResult(list(republican_dicts))







