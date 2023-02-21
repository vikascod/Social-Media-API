"""add user table

Revision ID: 5087b53458f0
Revises: d11c3979617f
Create Date: 2023-02-20 10:07:27.792086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5087b53458f0'
down_revision = 'd11c3979617f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
