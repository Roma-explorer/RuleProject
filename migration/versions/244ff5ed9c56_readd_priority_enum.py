"""readd priority enum

Revision ID: 244ff5ed9c56
Revises: eaacbf406b03
Create Date: 2022-06-18 22:49:24.926867

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sad_psql


# revision identifiers, used by Alembic.
from sqlalchemy.testing import db

from db.models import Priority

revision = '244ff5ed9c56'
down_revision = 'eaacbf406b03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('geography_columns',
    # sa.Column('f_table_catalog', sa.String(), nullable=True),
    # sa.Column('f_table_schema', sa.String(), nullable=True),
    # sa.Column('f_table_name', sa.String(), nullable=True),
    # sa.Column('f_geography_column', sa.String(), nullable=True),
    # sa.Column('coord_dimension', sa.Integer(), nullable=True),
    # sa.Column('srid', sa.Integer(), nullable=True),
    # sa.Column('type', sa.Text(), nullable=True)
    # )
    # op.create_table('geometry_columns',
    # sa.Column('f_table_catalog', sa.String(length=256), nullable=True),
    # sa.Column('f_table_schema', sa.String(), nullable=True),
    # sa.Column('f_table_name', sa.String(), nullable=True),
    # sa.Column('f_geometry_column', sa.String(), nullable=True),
    # sa.Column('coord_dimension', sa.Integer(), nullable=True),
    # sa.Column('srid', sa.Integer(), nullable=True),
    # sa.Column('type', sa.String(length=30), nullable=True)
    # )
    vals, name = (e.value for e in Priority), "priority"
    sa_enum = sa.Enum(*vals, name=name)
    psql_enum = sad_psql.ENUM(*vals, name=name, create_type=False)
    variant_enum = sa_enum.with_variant(psql_enum, "postgresql")
    variant_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('feature', sa.Column('priority', variant_enum, nullable=True))
    op.add_column('mistake', sa.Column('priority', variant_enum, nullable=True))
    op.add_column('task', sa.Column('priority', variant_enum, nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'priority')
    op.drop_column('mistake', 'priority')
    op.drop_column('feature', 'priority')
    sa_enum = sa.Enum(name='priority')
    sa_enum.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###