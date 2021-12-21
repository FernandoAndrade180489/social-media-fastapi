"""add content column to posts table

Revision ID: cd4b920376c0
Revises: 2d40c54f5529
Create Date: 2021-12-20 17:14:21.684727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd4b920376c0'
down_revision = '2d40c54f5529'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
