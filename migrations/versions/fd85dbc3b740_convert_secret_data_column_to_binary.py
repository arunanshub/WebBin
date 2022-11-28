"""convert secret_data column to binary

Revision ID: fd85dbc3b740
Revises: 79662f67dff2
Create Date: 2022-11-23 14:41:45.421028

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fd85dbc3b740"
down_revision = "79662f67dff2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.drop_column("secret_data")
        batch_op.add_column(
            sa.Column("secret_data", sa.LargeBinary(), nullable=False)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.drop_column("secret_data")
        batch_op.add_column(
            sa.Column("secret_data", sa.TEXT(), nullable=False)
        )

    # ### end Alembic commands ###
