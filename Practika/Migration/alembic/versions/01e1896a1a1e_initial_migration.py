"""Initial migration

Revision ID: 01e1896a1a1e
Revises: 01a6721263db
Create Date: 2023-06-29 11:39:43.996922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e1896a1a1e'
down_revision = '01a6721263db'
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.add_column('users', sa.Column('age', sa.Integer))

def downgrade() -> None:
    op.drop_column('users', 'age')
