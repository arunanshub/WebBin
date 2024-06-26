"""add nonce, tag, token, salt columns

Revision ID: 79662f67dff2
Revises: e5b2deffa08c
Create Date: 2022-11-23 14:28:12.207562

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "79662f67dff2"
down_revision = "e5b2deffa08c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("nonce", sa.LargeBinary(length=16), nullable=False)
        )
        batch_op.add_column(
            sa.Column("salt", sa.LargeBinary(length=32), nullable=False)
        )
        batch_op.add_column(
            sa.Column("token", sa.LargeBinary(length=32), nullable=False)
        )
        batch_op.alter_column(
            "secret_data", existing_type=sa.Text(), nullable=False
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.alter_column(
            "secret_data", existing_type=sa.Text(), nullable=True
        )
        batch_op.drop_column("token")
        batch_op.drop_column("salt")
        batch_op.drop_column("nonce")

    # ### end Alembic commands ###
