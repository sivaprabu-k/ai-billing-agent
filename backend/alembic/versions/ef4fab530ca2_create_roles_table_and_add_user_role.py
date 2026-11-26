
"""create roles table and add user role

Revision ID: ef4fab530ca2
Revises: cc1f42c345ee
Create Date: 2026-11-26 10:46:10.580945

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ef4fab530ca2"
down_revision: Union[str, Sequence[str], None] = "cc1f42c345ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create roles table
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_roles_name",
        "roles",
        ["name"],
        unique=True,
    )

    # 2. Insert default roles
    roles_table = sa.table(
        "roles",
        sa.column("name", sa.String()),
        sa.column("description", sa.String()),
    )

    op.bulk_insert(
        roles_table,
        [
            {
                "name": "Admin",
                "description": "Administrator with full system access",
            },
            {
                "name": "Billing Staff",
                "description": "Manages customers, bills, and billing operations",
            },
            {
                "name": "Support Staff",
                "description": "Handles customer support and billing inquiries",
            },
        ],
    )

    # 3. Add role_id temporarily as nullable
    op.add_column(
        "users",
        sa.Column("role_id", sa.Integer(), nullable=True),
    )

    # 4. Assign Admin role to existing users
    op.execute(
        sa.text(
            """
            UPDATE users
            SET role_id = (
                SELECT id
                FROM roles
                WHERE name = 'Admin'
            )
            """
        )
    )

    # 5. Make role_id mandatory
    op.alter_column(
        "users",
        "role_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # 6. Add foreign key constraint
    op.create_foreign_key(
        "fk_users_role_id_roles",
        "users",
        "roles",
        ["role_id"],
        ["id"],
    )


def downgrade() -> None:
    # Remove foreign key
    op.drop_constraint(
        "fk_users_role_id_roles",
        "users",
        type_="foreignkey",
    )

    # Remove role_id from users
    op.drop_column("users", "role_id")

    # Remove roles table and index
    op.drop_index("ix_roles_name", table_name="roles")
    op.drop_table("roles")
