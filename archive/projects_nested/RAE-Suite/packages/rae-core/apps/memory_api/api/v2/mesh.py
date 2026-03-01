import uuid
from typing import Any

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from apps.memory_api.services.mesh_service import MeshService

logger = structlog.get_logger(__name__)
router = APIRouter(tags=["Mesh"], prefix="/v2/mesh")


# Dependency to get MeshService singleton
def get_mesh_service(request: Request) -> MeshService:
    if not hasattr(request.app.state, "mesh_service"):
        # Initialize if not present (Lazy init for MVP)
        request.app.state.mesh_service = MeshService()

    from typing import cast

    return cast(MeshService, request.app.state.mesh_service)


# --- Models ---
class InviteRequest(BaseModel):
    host_url: str
    tenant_id: str = "default"


class InviteResponse(BaseModel):
    invite_code: str
    expires_in_seconds: int


class JoinRequest(BaseModel):
    invite_code: str
    my_peer_id: str
    my_public_url: str
    my_name: str


class JoinResponse(BaseModel):
    status: str
    host_peer_id: str
    host_token: str  # Token for the Joiner to use


class HandshakeRequest(BaseModel):
    # Sent by Joiner to Host
    invite_code: str
    peer_id: str
    peer_url: str
    peer_name: str
    peer_token: str  # Token for Host to use back


# --- Endpoints ---


@router.post("/invite", response_model=InviteResponse)
async def create_invite(
    request: InviteRequest, service: MeshService = Depends(get_mesh_service)
):
    """(Host) Create an invite code for someone to join."""
    code = service.create_invite(request.host_url, request.tenant_id)
    return InviteResponse(invite_code=code, expires_in_seconds=300)


@router.post("/join", response_model=JoinResponse)
async def join_mesh(
    request: JoinRequest, service: MeshService = Depends(get_mesh_service)
):
    """(Joiner) Consume an invite code and connect to a host."""
    try:
        # 1. Decode locally to find Host URL (Pre-check)
        # Note: We don't have the Host's secret, so we can't verify signature yet.
        # But standard JWT decode without verification allows reading the payload.
        import jwt

        payload = jwt.decode(request.invite_code, options={"verify_signature": False})
        host_url = payload.get("host")
        if not host_url:
            raise HTTPException(status_code=400, detail="Invalid invite: missing host")

        # 2. Perform Handshake with Host
        import httpx

        my_token = str(uuid.uuid4())  # Generate a token for Host to call us

        async with httpx.AsyncClient() as client:
            hs_payload = {
                "invite_code": request.invite_code,
                "peer_id": request.my_peer_id,
                "peer_url": request.my_public_url,
                "peer_name": request.my_name,
                "peer_token": my_token,
            }
            resp = await client.post(f"{host_url}/v2/mesh/handshake", json=hs_payload)
            if resp.status_code != 200:
                raise HTTPException(
                    status_code=400, detail=f"Handshake rejected: {resp.text}"
                )

            data = resp.json()

        # 3. Register Host as a peer locally
        service.register_peer(
            peer_id=data["host_id"],
            name="Host",
            url=host_url,
            token=data["token"],  # Token they gave us
        )

        return JoinResponse(
            status="connected",
            host_peer_id=data["host_id"],
            host_token=data["token"],
        )

    except Exception as e:
        logger.error("join_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/handshake")
async def receive_handshake(
    request: HandshakeRequest, service: MeshService = Depends(get_mesh_service)
):
    """(Host) Receive a handshake request from a Joiner."""
    try:
        # 1. Validate Invite Code
        service.validate_invite(request.invite_code)

        # 2. Register the Joiner as a trusted peer
        service.register_peer(
            peer_id=request.peer_id,
            name=request.peer_name,
            url=request.peer_url,
            token=request.peer_token,
        )

        # 3. Generate a token for the Joiner to use
        my_token_for_joiner = str(uuid.uuid4())

        # For MVP, we assume the token is valid if it matches what we generated.
        # In a real system, we'd store this token in a DB associated with the peer_id.

        return {
            "status": "accepted",
            "host_id": "rae-host",
            "token": my_token_for_joiner,
        }

    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error("handshake_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/peers")
async def list_peers(service: MeshService = Depends(get_mesh_service)):
    """List connected peers."""
    return service.list_peers()


@router.post("/sync/receive")
async def receive_sync_data(payload: dict[str, Any]):
    """Receive pushed memories from a peer."""
    # Placeholder for actual ingestion logic
    logger.info("received_sync_push", items=len(payload.get("memories", [])))
    return {"status": "accepted", "processed": len(payload.get("memories", []))}
