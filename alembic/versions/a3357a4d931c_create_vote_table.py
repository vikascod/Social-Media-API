"""create vote table

Revision ID: a3357a4d931c
Revises: 0fbe37aa78ff
Create Date: 2023-02-20 12:48:05.464607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3357a4d931c'
down_revision = '0fbe37aa78ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id'))
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
