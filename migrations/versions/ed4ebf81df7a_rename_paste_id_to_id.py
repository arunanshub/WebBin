"""rename paste_id to id

Revision ID: ed4ebf81df7a
Revises: 3492f71fb181
Create Date: 2022-11-26 01:02:13.457705

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ed4ebf81df7a"
down_revision = "3492f71fb181"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.INTEGER(),
            type_=sa.String(length=32),
            existing_nullable=False,
        )
        batch_op.drop_index("ix_secrets_paste_id")
        batch_op.create_index(batch_op.f("ix_secrets_id"), ["id"], unique=True)
        batch_op.drop_column("paste_id")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("paste_id", sa.VARCHAR(length=32), nullable=True)
        )
        batch_op.drop_index(batch_op.f("ix_secrets_id"))
        batch_op.create_index(
            "ix_secrets_paste_id", ["paste_id"], unique=False
        )
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=32),
            type_=sa.INTEGER(),
            existing_nullable=False,
        )

    # ### end Alembic commands ###