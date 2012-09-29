'''OutEat is an app to coordinate groups of diners on a current-day basis.
'''

import json
from elixir import metadata, setup_all, session, Entity, Field, String
from sqlalchemy.orm.exc import NoResultFound

metadata.bind = "sqlite:///outeat.sqlite"
metadata.bind.echo = True

class Diner(Entity):
    who = Field(String(256), default="", nullable=False)
    where = Field(String(4096), default="[]", nullable=False)
    when = Field(String(64), default="[]", nullable=False)

setup_all(True)

class OutEat(object):
    '''
    Imagine a hungry developer would like to go out to eat, and would like to advertise
    that fact to the other developers.
    Unfortunately, wandering about asking someone if the want to go eat is distracting.

    So, the hungry developer puts out a call on OutEat.

    (Presuming we have an instantiated OutEat instance)

    It's basically the same as sending an email like:
        "I want to eat out today."
    >>> OutEat().register("Charles")
    [{'who: 'Charles', 'where': ['any'], 'when': 'any'}]

    If they choose, they can give some preferences:
        "I want to eat out today at McKillahenny's Pub or Lopez' Pizza."
    >>> OutEat().register("Charles", ["McKillahenny's Pub", "Lopez' Pizza"])
    [{'who: 'Charles', 'where': ["McKillahenny's Pub", "Lopez' Pizza"], 'when': 'any'}]

    Or just a type of food:
        "I want to eat pub food today."
    >>> OutEat().register("Charles", "pub")
    [{'who: 'Charles', 'where': ['pub'], 'when': 'any'}]

        "I want to eat chinese today."
    >>> OutEat().register("Charles", "chinese")
    [{'who: 'Charles', 'where': ['chinese'], 'when': 'any'}]

        "I want to eat out for lunch."
    >>> OutEat().register("Charles", time='lunch')
    [{'who: 'Charles', 'where': ['pub'], 'when': 'any'}]

    This triggers notifications to people subscribed to certain places or types of food.
    >>> outeat = OutEat()
    >>> outeat.register("Charles", ["chinese", ])
    [{'who: 'Charles', 'where': ['chinese'], 'when': 'any'}]
    >>> outeat.register("Charles", ["Lopez' Pizza", ])
    [{'who: 'Charles', 'where': ['chinese', "Lopez' Pizza"], 'when': 'any'}]
    >>> outeat.notify()
    [{'who: 'Charles', 'where': ['chinese', "Lopez' Pizza"], 'when': 'any'}]
    '''

    def register(self, person, place=None, time=None):
        if not place:
            place = ['any']
        if not time:
            time = ['any']

        try:
            # Get person if in the Diner table.
            diner = Diner.query.filter_by(who=person).one()
        except NoResultFound:
            # if not, insert a new one.
            diner = Diner(who=person)
        # Update their places and times.
        where = json.loads(diner.where)
        if where:
            where.extend(place)
        else:
            where = place
        diner.where = json.dumps(where)

        when = json.loads(diner.where)
        if when:
            when.extend(time)
        else:
            when = time
        diner.when = json.dumps(where)

        session.commit()

    def notify(self):
        '''Send out notifications to people interested in eating out.'''
        pass
