"""Initial migration

Revision ID: 01a6721263db
Revises: 
Create Date: 2023-06-29 11:38:41.814333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01a6721263db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),
        sa.Column('email', sa.String(100), unique=True)
    )

def downgrade() -> None:
    op.drop_table('users')