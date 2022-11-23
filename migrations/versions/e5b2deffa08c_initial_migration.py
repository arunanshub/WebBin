"""initial migration

Revision ID: e5b2deffa08c
Revises:
Create Date: 2022-11-23 13:15:09.439824

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e5b2deffa08c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "secrets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("paste_id", sa.String(length=32), nullable=True),
        sa.Column("secret_data", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_secrets_paste_id"), ["paste_id"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_secrets_paste_id"))

    op.drop_table("secrets")
    # ### end Alembic commands ###
