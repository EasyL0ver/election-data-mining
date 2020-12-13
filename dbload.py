from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, relationship, deferred, reconstructor
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from itertools import groupby
from primaryarea import CountyArea, AggregateArea
import us

Base = automap_base()

class AreaFacts(Base):
    __tablename__ = 'county_facts'

def start_session(db_address):
    engine = create_engine(db_address)
    Base.prepare(engine, reflect=True)
    return Session(engine)

def load_counties(session, filter_empty = True):
    counties = session.query(AreaFacts).filter(AreaFacts.state_abbreviation != '').all()
    mapped_counties = list(map(lambda x: CountyArea(x), counties))

    if filter_empty:
        return list(filter(lambda x: x.is_valid(), mapped_counties))

    return mapped_counties

def load_states(session, filter_empty = True):
    counties = load_counties(session)
    states_facts = session.query(AreaFacts).filter(AreaFacts.state_abbreviation == '', AreaFacts.fips != 0).all()

    states_objects = []
    for states_fact in states_facts:
        state_data = us.states.lookup(states_fact.area_name)
        if not state_data:
            print('State lookup not found! ' + states_fact.area_name)
            continue
        child_counties = list(filter(lambda x:x.facts.state_abbreviation == state_data.abbr, counties))
        states_objects.append(AggregateArea(child_counties, states_fact))
    
    if filter_empty:
        return list(filter(lambda x: x.is_valid(), states_objects))

    return states_objects

