import asyncio
import db
from vacancies.models import Vacancy

async def load_db(file: str) -> None:
    await db.init()

    vacancies = []
    with open(file, 'r') as f:
        for line in f.readlines():
            exp, price, comp = line.split('# ')
            comp = comp.strip()
            price = int(price)
            comp = eval(comp)
            comp = ", ".join(comp)

            vacancies.append(Vacancy(experiece=exp, price = price, competentions = comp))

    await Vacancy.bulk_create(vacancies)
    print('ok')


def main(file: str) -> None:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(load_db(file))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print('use load_db <file>')
        exit(1)
    
    main(sys.argv[1])