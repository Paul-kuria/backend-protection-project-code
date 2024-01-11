"""Create status table

Revision ID: fa19b5cb260e
Revises: 
Create Date: 2023-12-14 10:50:31.728298

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fa19b5cb260e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "status_messages",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("device_id", sa.String(), nullable=False),
        sa.Column("battery_level", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("network_status", sa.String(), nullable=False),
        sa.Column("storage_usage", sa.String(), nullable=False),
        sa.Column("last_response", sa.String(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("status_messages")
