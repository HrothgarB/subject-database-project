"""token sessions

Revision ID: 20260318_0002
Revises: 20260318_0001
Create Date: 2026-03-18
"""

from alembic import op
import sqlalchemy as sa


revision = "20260318_0002"
down_revision = "20260318_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "token_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False, unique=True),
        sa.Column("current_refresh_jti", sa.String(length=64), nullable=False, unique=True),
        sa.Column("device_id", sa.String(length=128), nullable=True),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_token_sessions_user_id", "token_sessions", ["user_id"])
    op.create_index("ix_token_sessions_session_id", "token_sessions", ["session_id"])
    op.create_index("ix_token_sessions_device_id", "token_sessions", ["device_id"])


def downgrade() -> None:
    op.drop_index("ix_token_sessions_device_id", table_name="token_sessions")
    op.drop_index("ix_token_sessions_session_id", table_name="token_sessions")
    op.drop_index("ix_token_sessions_user_id", table_name="token_sessions")
    op.drop_table("token_sessions")
