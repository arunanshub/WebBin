"""convert BINARY to LargeBinary

Revision ID: 1f4fe1bd5dc6
Revises: 2bd41d942105
Create Date: 2022-11-25 21:43:44.907746

"""

from __future__ import annotations

from alembic import op

# revision identifiers, used by Alembic.
revision = "1f4fe1bd5dc6"
down_revision = "2bd41d942105"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None):
        pass

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("secrets", schema=None):
        pass

    # ### end Alembic commands ###
