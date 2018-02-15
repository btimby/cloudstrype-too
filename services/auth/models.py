from sqlalchemy import Metadata, Table, Integer, Column
from sqlalchemy.schema import CreateTable


metadata = MetaData()

User = Table('auth_user', metadata,
    Column(),
    Column())


Group = Table('auth_group', metadata,
    Column())


async def create_tables(engine):
    async with engine.acquire() as c:
        for table in (User, Group):
            # TODO: skip if table exists, migrations?
            sql = CreateTable(table.__table__).compile(engine.dialect)
            await c.execute(sql)
