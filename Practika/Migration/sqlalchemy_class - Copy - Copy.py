
def upgrade() -> None:
    op.add_column('users', sa.Column('age', sa.Integer))

def downgrade() -> None:
    op.drop_column('users', 'age')


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),
        sa.Column('email', sa.String(100), unique=True)
    )

def downgrade() -> None:
    op.drop_table('users')