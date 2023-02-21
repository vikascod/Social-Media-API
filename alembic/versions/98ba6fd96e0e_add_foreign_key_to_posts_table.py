"""add foreign-key to posts table

Revision ID: 98ba6fd96e0e
Revises: 5087b53458f0
Create Date: 2023-02-20 10:45:31.551325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98ba6fd96e0e'
down_revision = '5087b53458f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
