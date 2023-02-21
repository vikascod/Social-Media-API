"""add content column to posts table

Revision ID: d11c3979617f
Revises: 2dc352f19594
Create Date: 2023-02-20 09:56:01.996223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd11c3979617f'
down_revision = '2dc352f19594'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
