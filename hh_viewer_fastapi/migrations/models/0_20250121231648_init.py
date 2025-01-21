from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "hash_password" VARCHAR(255) NOT NULL,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_active" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "vacancies" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "experiece" VARCHAR(50) NOT NULL,
    "price" INT NOT NULL,
    "competentions" TEXT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
