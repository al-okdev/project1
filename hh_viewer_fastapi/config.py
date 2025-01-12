TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["vacancies.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}