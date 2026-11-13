from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.models import Base

EXPECTED_TABLES = {
    "organizations",
    "warehouses",
    "distribution_points",
    "inventory_items",
    "inventory_transactions",
    "vehicles",
    "deliveries",
    "risk_alerts",
}


def test_all_core_tables_are_registered():
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_every_business_table_belongs_to_an_organization():
    for name, table in Base.metadata.tables.items():
        if name == "organizations":
            continue
        foreign_tables = {fk.column.table.name for fk in table.c.organization_id.foreign_keys}
        assert foreign_tables == {"organizations"}, name
        assert not table.c.organization_id.nullable, name


def test_tables_compile_for_postgresql():
    dialect = postgresql.dialect()
    for table in Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=dialect))
        assert f"CREATE TABLE {table.name}" in ddl


def test_constraint_names_are_unique():
    names = [
        constraint.name
        for table in Base.metadata.tables.values()
        for constraint in (*table.constraints, *table.indexes)
    ]
    assert len(names) == len(set(names))
