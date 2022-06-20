"""readd status, add dedicated hours

Revision ID: 8a9cfbdf34c1
Revises: 6bc51568b230
Create Date: 2022-06-18 21:26:32.841111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

from db.models import Status

revision = '8a9cfbdf34c1'
down_revision = '6bc51568b230'
branch_labels = None
depends_on = None


def upgrade():
    # # ### commands auto generated by Alembic - please adjust! ###
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
    status_type = postgresql.ENUM(Status, name='status')
    status_type.create(op.get_bind(), checkfirst=True)
    op.add_column('feature', sa.Column('dedicated_hours', sa.Integer(), nullable=True))
    op.add_column('feature', sa.Column('status', status_type, nullable=False))
    op.add_column('mistake', sa.Column('status', status_type, nullable=False))
    op.add_column('mistake', sa.Column('dedicated_hours', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('status', status_type, nullable=False))
    op.add_column('task', sa.Column('dedicated_hours', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'dedicated_hours')
    op.drop_column('task', 'status')
    op.drop_column('mistake', 'dedicated_hours')
    op.drop_column('mistake', 'status')
    op.drop_column('feature', 'status')
    op.drop_column('feature', 'dedicated_hours')
    op.drop_table('geometry_columns')
    op.drop_table('geography_columns')
    # ### end Alembic commands ###
