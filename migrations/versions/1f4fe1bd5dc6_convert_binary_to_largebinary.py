"""convert BINARY to LargeBinary

Revision ID: 1f4fe1bd5dc6
Revises: 2bd41d942105
Create Date: 2022-11-25 21:43:44.907746

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1f4fe1bd5dc6"
down_revision = "2bd41d942105"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.alter_column(
            "secret_data",
            existing_type=sa.NUMERIC(),
            type_=sa.LargeBinary(),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "nonce",
            existing_type=sa.NUMERIC(precision=16),
            type_=sa.LargeBinary(length=16),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "salt",
            existing_type=sa.NUMERIC(precision=32),
            type_=sa.LargeBinary(length=32),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "token",
            existing_type=sa.NUMERIC(precision=32),
            type_=sa.LargeBinary(length=32),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None) as batch_op:
        batch_op.alter_column(
            "token",
            existing_type=sa.LargeBinary(length=32),
            type_=sa.NUMERIC(precision=32),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "salt",
            existing_type=sa.LargeBinary(length=32),
            type_=sa.NUMERIC(precision=32),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "nonce",
            existing_type=sa.LargeBinary(length=16),
            type_=sa.NUMERIC(precision=16),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "secret_data",
            existing_type=sa.LargeBinary(),
            type_=sa.NUMERIC(),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
