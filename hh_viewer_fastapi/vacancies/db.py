from tortoise import Tortoise
import config

async def init():
    await Tortoise.init(config.TORTOISE_ORM
        #db_url='sqlite://db.sqlite3',
        #modules={'models': ['vacancies.models']}
    )
    # Generate the schema
    #await Tortoise.generate_schemas()