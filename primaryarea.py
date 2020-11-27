from math import floor

class Result:
    def __init__(self, data):
        self.votes = dict()

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

class AggregateResult:
    def __init__(self, results):
        self.votes = dict()
        self.votes_count = 0

        for child_dict in results:
            self.votes_count += child_dict.votes_count
            for key, value in child_dict.votes.items():

                if(key not in self.votes):
                    self.votes[key] = 0
                
                self.votes[key] += value
        

class Area:
    def __init__(self, area_facts):
        self.facts = area_facts

    def __repr__(self):
        return self.facts.area_name + " " + self.facts.state_abbreviation

class CountyArea(Area):
    def __init__(self, primary_results, area_facts):
        super().__init__(area_facts)
        self.results = list(primary_results)

        republican_results = filter(lambda x:x.party == 'Republican', primary_results)
        democrat_results = filter(lambda x:x.party == 'Democrat', primary_results)

        self.democrat = Result(list(democrat_results))
        self.republican = Result(list(republican_results))

    def get_democrat(self):
        return self.democrat

    def get_republican(self):
        return self.republican


class AggregateArea(Area):
    def __init__(self, child_areas, area_facts):
        super().__init__(area_facts)
        self.child_areas = child_areas

    def get_democrat(self):
        democrat_dicts = map(lambda x: x.get_democrat(), self.child_areas)
        return AggregateResult(list(democrat_dicts))

    def get_republican(self):
        republican_dicts = map(lambda x: x.get_republican(), self.child_areas)
        return AggregateResult(list(republican_dicts))





