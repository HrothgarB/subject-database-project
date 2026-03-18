"""initial schema

Revision ID: 20260318_0001
Revises:
Create Date: 2026-03-18
"""

from alembic import op
import sqlalchemy as sa


revision = "20260318_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("middle_name", sa.String(length=120), nullable=True),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("alias", sa.String(length=120), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("case_number", sa.String(length=64), nullable=True),
        sa.Column("intel_number", sa.String(length=64), nullable=True),
        sa.Column("restricted_ssn_ciphertext", sa.String(length=512), nullable=True),
        sa.Column("created_by_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_subjects_first_name", "subjects", ["first_name"])
    op.create_index("ix_subjects_last_name", "subjects", ["last_name"])
    op.create_index("ix_subjects_dob", "subjects", ["dob"])
    op.create_index("ix_subjects_alias", "subjects", ["alias"])
    op.create_index("ix_subjects_case_number", "subjects", ["case_number"])
    op.create_index("ix_subjects_intel_number", "subjects", ["intel_number"])

    op.create_table(
        "subject_photos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject_id", sa.Integer(), sa.ForeignKey("subjects.id"), nullable=False),
        sa.Column("object_key", sa.String(length=512), nullable=False, unique=True),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_subject_photos_subject_id", "subject_photos", ["subject_id"])

    op.create_table(
        "encounters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject_id", sa.Integer(), sa.ForeignKey("subjects.id"), nullable=False),
        sa.Column("officer_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("encountered_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_encounters_subject_id", "encounters", ["subject_id"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=False),
        sa.Column("resource_id", sa.String(length=64), nullable=True),
        sa.Column("method", sa.String(length=10), nullable=False),
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])


def downgrade() -> None:
    op.drop_index("ix_audit_logs_action", table_name="audit_logs")
    op.drop_index("ix_audit_logs_actor_user_id", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("ix_encounters_subject_id", table_name="encounters")
    op.drop_table("encounters")
    op.drop_index("ix_subject_photos_subject_id", table_name="subject_photos")
    op.drop_table("subject_photos")
    op.drop_index("ix_subjects_intel_number", table_name="subjects")
    op.drop_index("ix_subjects_case_number", table_name="subjects")
    op.drop_index("ix_subjects_alias", table_name="subjects")
    op.drop_index("ix_subjects_dob", table_name="subjects")
    op.drop_index("ix_subjects_last_name", table_name="subjects")
    op.drop_index("ix_subjects_first_name", table_name="subjects")
    op.drop_table("subjects")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_table("users")
