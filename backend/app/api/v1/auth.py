
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.auth.auth import verify_keycloak_token
from app.core.auth.kc_admin import kc_admin_get

from app.deps import get_db

from app.models.projects import Project, UserProjectAccess

router = APIRouter(tags=["auth"])
client = "mihira-cli"
realm = "MIHIRA-REALM"

def get_all_roles(token: dict, client_id: str = client):
    realm_roles = token.get("realm_access", {}).get("roles", [])
    client_roles = (
        token.get("resource_access", {})
             .get(client_id, {})
             .get("roles", [])
    )
    return set(realm_roles) | set(client_roles)

@router.get("/me")
def me(user=Depends(verify_keycloak_token)):
    return {
        "kc_user_id": user["sub"],
        "username": user.get("preferred_username"),
        "realm_roles": user.get("realm_access", {}).get("roles", []),
        "client_roles": user.get("resource_access", {}).get("admin-cli", {}).get("roles", []),
        "groups": user.get("groups", []),
    }

@router.get("/me/projects")
def my_projects(user=Depends(verify_keycloak_token), db: Session = Depends(get_db)):
    kc_id = user["sub"]

    rows = (
        db.query(Project, UserProjectAccess.role)
          .join(UserProjectAccess, UserProjectAccess.project_id == Project.id)
          .filter(UserProjectAccess.user_kc_id == kc_id)
          .all()
    )

    return [
        {
            "id": str(project.id),
            "name": project.name,
            "code": project.code,
            "role": role,
        }
        for project, role in rows
    ]



@router.get("/kc/users")
def list_keycloak_users(
    first: int = Query(0, ge=0),
    max: int = Query(50, ge=1, le=200),
    user=Depends(verify_keycloak_token),
):
    roles = get_all_roles(user, client_id=client)
    if "app_admin" not in roles:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        return kc_admin_get(f"/admin/realms/{realm}/users?first={first}&max={max}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Keycloak admin API failed: {e}")
