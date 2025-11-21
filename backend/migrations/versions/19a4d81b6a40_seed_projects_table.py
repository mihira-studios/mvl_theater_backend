"""seed projects table

Revision ID: 19a4d81b6a40
Revises: b8fa1b12e9ba
Create Date: 2025-11-20 17:57:37.610777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19a4d81b6a40'
down_revision: Union[str, Sequence[str], None] = 'b8fa1b12e9ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    def update_project(name, code, status, archived, description, ptype, updated_at, updated_by):
        where_field = "code" if code else "name"
        where_value = code or name

        op.execute(
            sa.text(f"""
                UPDATE projects
                SET
                    status = :status,
                    archived = :archived,
                    description = :description,
                    type = :ptype,
                    updated_at = :updated_at,
                    updated_by = :updated_by
                WHERE {where_field} = :where_value
            """).bindparams(
                status=status,
                archived=archived,
                description=description,
                ptype=ptype,
                updated_at=updated_at,
                updated_by=updated_by,
                where_value=where_value,
            )
        )

    # All your rows from the CSV:
    # "Project Name","Thumbnail","Code","Status","Archived","Description","Type","Date Updated","Updated by"

    update_project(
        name="BB3",
        code="bb3",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-11-11 10:59:23",
        updated_by="Tilak Krishna Moorthy",
    )

    update_project(
        name="BB_URC",
        code="",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-11-03 14:33:59",
        updated_by="Bhavik S",
    )

    update_project(
        name="BEW",
        code="bew",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-11-03 14:33:59",
        updated_by="Bhavik S",
    )

    update_project(
        name="dev-test-project",
        code="dtp",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-07-18 12:43:48",
        updated_by="Deepak Thapliyal",
    )

    update_project(
        name="GEN63",
        code="gen63",
        status="Active",
        archived=False,
        description="",
        ptype="Feature",
        updated_at="2025-11-03 14:33:59",
        updated_by="Bhavik S",
    )

    update_project(
        name="GHOST",
        code="ghost",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-11-13 10:49:35",
        updated_by="Bhavik S",
    )

    update_project(
        name="My Film VFX Project",
        code="",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-09-29 16:44:54",
        updated_by="Tilak Krishna Moorthy",
    )

    update_project(
        name="Product",
        code="",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-11-17 11:12:01",
        updated_by="Rahul Gattu",
    )

    update_project(
        name="Studio",
        code="Studio",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-11-06 09:40:22",
        updated_by="Rahul Gattu",
    )

    update_project(
        name="testGen63",
        code="tg63",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-09-02 11:59:20",
        updated_by="Bhavik S",
    )

    update_project(
        name="vfxtraining",
        code="tp",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-10-30 11:47:53",
        updated_by="Saswat Sahoo",
    )

    update_project(
        name="WB",
        code="wb",
        status="",
        archived=False,
        description="",
        ptype="",
        updated_at="2025-09-02 11:59:19",
        updated_by="Bhavik S",
    )


def downgrade() -> None:
    """Downgrade schema."""
    def reset_project(name, code):
        where_clause = ""
        params = {"name": name, "code": code}

        if code:
            where_clause = "code = :code"
        else:
            where_clause = "name = :name"

        op.execute(
            sa.text(
                f"""
                UPDATE projects
                SET
                    status      = NULL,
                    archived    = FALSE,
                    description = NULL,
                    type        = NULL,
                    updated_by  = NULL
                WHERE {where_clause}
                """
            ),
            params,
        )

    reset_project("BB3", "bb3")
    reset_project("BB_URC", "")
    reset_project("BEW", "bew")
    reset_project("dev-test-project", "dtp")
    reset_project("GEN63", "gen63")
    reset_project("GHOST", "ghost")
    reset_project("My Film VFX Project", "")
    reset_project("Product", "")
    reset_project("Studio", "Studio")
    reset_project("testGen63", "tg63")
    reset_project("vfxtraining", "tp")
    reset_project("WB", "wb")
