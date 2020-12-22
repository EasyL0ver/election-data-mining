import re

facts_labels = {'PST045214':'Population, 2014 estimate',
'PST040210':'Population, 2010 (April 1) estimates base',
'PST120214':'Population percent change, - April 1, 2010 to July 1, 2014',
'POP010210':'Population, 2010',
'AGE135214':'Persons under 5 years, percent, 2014',
'AGE295214':'Persons under 18 years, percent, 2014',
'AGE775214':'Persons 65 years and over, percent, 2014',
'SEX255214':'Female persons, percent, 2014',
'RHI125214':'White alone, percent, 2014',
'RHI225214':'Black or African American alone, percent, 2014',
'RHI325214':'American Indian and Alaska Native alone, percent, 2014',
'RHI425214':'Asian alone, percent, 2014',
'RHI525214':'Native Hawaiian and Other Pacific Islander alone, percent, 2014',
'RHI625214':'Two or More Races, percent, 2014',
'RHI725214':'Hispanic or Latino, percent, 2014',
'RHI825214':'White alone not Hispanic or Latino, percent, 2014',
'POP715213':'Living in same house 1 year & over, percent, 2009-2013',
'POP645213':'Foreign born persons, percent, 2009-2013',
'POP815213':'Language other than English spoken at home, pct age 5+, 2009-2013',
'EDU635213':'High school graduate or higher, percent of persons age 25+, 2009-2013',
'EDU685213':'Bachelors degree or higher, percent of persons age 25+, 2009-2013',
'VET605213':'Veterans, 2009-2013',
'LFE305213':'Mean travel time to work (minutes), workers age 16+, 2009-2013',
'HSG010214':'Housing units, 2014',
'HSG445213':'Homeownership rate, 2009-2013',
'HSG096213':'Housing units in multi-unit structures, percent, 2009-2013',
'HSG495213':'Median value of owner-occupied housing units, 2009-2013',
'HSD410213':'Households, 2009-2013',
'HSD310213':'Persons per household, 2009-2013',
'INC910213':'Per capita money income in past 12 months (2013 dollars), 2009-2013',
'INC110213':'Median household income, 2009-2013',
'PVY020213':'Persons below poverty level, percent, 2009-2013',
'BZA010213':'Private nonfarm establishments, 2013',
'BZA110213':'Private nonfarm employment,  2013',
'BZA115213':'Private nonfarm employment, percent change, 2012-2013',
'NES010213':'Nonemployer establishments, 2013',
'SBO001207':'Total number of firms, 2007',
'SBO315207':'Black-owned firms, percent, 2007',
'SBO115207':'American Indian- and Alaska Native-owned firms, percent, 2007',
'SBO215207':'Asian-owned firms, percent, 2007',
'SBO515207':'Native Hawaiian- and Other Pacific Islander-owned firms, percent, 2007',
'SBO415207':'Hispanic-owned firms, percent, 2007',
'SBO015207':'Women-owned firms, percent, 2007',
'MAN450207':'Manufacturers shipments, 2007 ($1,000)',
'WTN220207':'Merchant wholesaler sales, 2007 ($1,000)',
'RTN130207':'Retail sales, 2007 ($1,000)',
'RTN131207':'Retail sales per capita, 2007',
'AFN120207':'Accommodation and food services sales, 2007 ($1,000)',
'BPS030214':'Building permits, 2014',
'LND110210':'Land area in square miles, 2010',
'POP060210':'Population per square mile, 2010'}

class Fact:
    def __init__(self, fact_name, fact_value):
        self.fact_name = fact_name
        self.fact_value = fact_value

class FactsVector:
    def __init__(self, facts):
        self.facts = facts

    def numerical(self):
        return list(map(lambda x:x.fact_value, self.facts))

    def labels(self, short = False):
        if short:
            return list(map(lambda x: x.fact_name.split(',')[0], self.facts))
        return list(map(lambda x: x.fact_name, self.facts))

class FactsVectorFactory:
    democrat_candidates = ['Hillary Clinton', 'Bernie Sanders']
    republican_candidates = ['Ben Carson', 'Donald Trump', 'Marco Rubio', 'Ted Cruz', 'John Kasich']

    def init_transforms(self):
        tdict = dict()

        none = lambda val, prop_name, area : Fact(prop_name, val)
        normalize_per_capita = lambda val, prop_name, area : Fact(prop_name + " per capita", val / area.facts.PST045214)
        normalize_per_10000 = lambda val, prop_name, area : Fact(prop_name + " per 10000", val / area.facts.PST045214 * 10000)

        tdict['PST045214'] = none
        tdict['PST120214'] = none
        tdict['^AGE'] = none
        tdict['^SEX'] = none
        tdict['^RHI'] = none
        tdict['POP715213'] = none
        tdict['POP645213'] = none
        tdict['POP815213'] = none
        tdict['^EDU'] = none
        tdict['VET605213'] = normalize_per_10000
        tdict['LFE305213'] = none
        tdict['HSG010214'] = normalize_per_capita
        tdict['HSG096213'] = none
        tdict['HSG495213'] = none
        tdict['HSD410213'] = normalize_per_capita
        tdict['HSD310213'] = none
        tdict['^INC'] = none
        tdict['^PVY'] = none
        tdict['BZA010213'] = normalize_per_10000
        tdict['BZA110213'] = normalize_per_10000
        tdict['BZA115213'] = none
        tdict['NES010213'] = none
        tdict['^SBO0'] = normalize_per_10000
        tdict['^SBO[1-9]'] = none
        tdict['RTN131207'] = none
        tdict['BPS030214'] = normalize_per_10000
        tdict['POP060210'] = none

        return tdict

    def __init__(self):
        self.transform_dict = self.init_transforms()

    def get_facts_vector(self, area):
        pattern = re.compile('^[A-Z]{3}')
        vector = []
        for key, value in sorted(vars(area.facts).items(), key=lambda x: x[0]):
            if not re.match(pattern, key):
                continue

            for transform_regex, transform_function in self.transform_dict.items():
                if re.match(transform_regex, key):
                    fact_name = facts_labels[key]
                    fact = transform_function(float(value),fact_name, area)
                    vector.append(fact)
                    break

        return vector

    def get_votes_vector(self, area):
        vector = []
        for democratCandidate in FactsVectorFactory.democrat_candidates:
            fact = Fact(democratCandidate, area.democrat.get_candidate_fraction(democratCandidate))
            vector.append(fact)
        for republicanCandidate in FactsVectorFactory.republican_candidates:
            fact = Fact(republicanCandidate, area.republican.get_candidate_fraction(republicanCandidate))
            vector.append(fact)

        return vector

    def get_complete_vector(self, area):
        return FactsVector(self.get_votes_vector(area) + self.get_facts_vector(area))
        


