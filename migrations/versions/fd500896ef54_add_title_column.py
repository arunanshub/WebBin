"""add title column

Revision ID: fd500896ef54
Revises: ed4ebf81df7a
Create Date: 2022-11-26 12:04:04.982337

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fd500896ef54"
down_revision = "ed4ebf81df7a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("title", sa.LargeBinary(length=100), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.drop_column("title")

    # ### end Alembic commands ###