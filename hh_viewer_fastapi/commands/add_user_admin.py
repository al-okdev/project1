import asyncio
import db
import bcrypt
from users.models import User
from tortoise.contrib.pydantic import pydantic_model_creator
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

async def create_user(user_data: UserIn_Pydantic):
    user = await User.create(**user_data.model_dump(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user)


async def add_user_admin(username: str, password: str) -> None:
    await db.init()

    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash_password = bcrypt.hashpw(bytes, salt) 

    user_data = UserIn_Pydantic(username=username, hash_password=hash_password, is_superuser=True, is_active=True)
    user = await create_user(user_data)
    print(user)

def main(username: str, password: str) -> None:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(add_user_admin(username, password))


if __name__ == "__main__":
    import sys
    print(sys.argv)
    main(sys.argv[1], sys.argv[2])