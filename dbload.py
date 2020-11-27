from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, relationship, deferred
from sqlalchemy import create_engine, Column, Integer, ForeignKey
from itertools import groupby
from primaryarea import CountyArea, AggregateArea

import us

Base = automap_base()

class PrimaryResult(Base):
    __tablename__ = 'primary_results'
    facts_id = Column('fips', Integer, ForeignKey('county_facts.fips'))
    facts = relationship('county_facts', lazy='select')

def load_session(db_address):
    engine = create_engine(db_address)
    Base.prepare(engine, reflect=True)

    global CountyFact
    CountyFact = Base.classes.county_facts

    return Session(engine)

def prepare_county_data(session):
    results = session.query(PrimaryResult).order_by(PrimaryResult.facts_id).all()

    counties = []
    for key, area_members in groupby(results, lambda x: x.facts_id):
        members = list(area_members)
        area_facts = members[0].facts
        if(area_facts is None):
            print('Area facts not found for county with id: ' + str(key))
            continue
        c = CountyArea(members, area_facts)
        counties.append(c)
    return counties

def prepare_state_data(session):
    counties = prepare_county_data(session)
    counties.sort(key=lambda x:x.facts.state_abbreviation)

    states = []
    for code, counties in groupby(counties, lambda x:x.facts.state_abbreviation):
        state = us.states.lookup(code)
        state_facts = session.query(CountyFact).filter(CountyFact.area_name == state.name).first()

        a = AggregateArea(list(counties), state_facts)
        states.append(a)
    return states

def prepare_country_data(session):
    states = prepare_state_data(session)
    country_facts = session.query(CountyFact).filter(CountyFact.fips == 0).first()
    return AggregateArea(states, country_facts)
