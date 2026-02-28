"""Service for managing Mesh Federation (Peer-to-Peer Trust)."""

import secrets
import time
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


class PeerInfo(BaseModel):
    peer_id: str
    name: str
    url: str
    token: str  # The token we use to call them
    created_at: float


class MeshInvite(BaseModel):
    code: str
    expires_at: float
    host_url: str
    tenant_id: str


class MeshService:
    """
    Manages the 'Trust Handshake' protocol.
    Stores trusted peers and active invite codes.
    """

    def __init__(self, secret_key: str = "mesh-secret-change-me"):
        self.secret_key = secret_key
        # In-memory storage for MVP. In production, use DB/Redis.
        self._peers: Dict[str, PeerInfo] = {}
        self._active_invites: Dict[str, dict] = {}

    def create_invite(
        self, host_url: str, tenant_id: str, duration_minutes: int = 5
    ) -> str:
        """Generate a signed invite code."""
        nonce = secrets.token_hex(8)
        exp = datetime.now() + timedelta(minutes=duration_minutes)
        payload = {
            "iss": "rae-mesh",
            "host": host_url,
            "tenant": tenant_id,
            "nonce": nonce,
            "exp": exp.timestamp(),
        }

        # Sign JWT
        code = jwt.encode(payload, self.secret_key, algorithm="HS256")

        # Store for validation (nonce check)
        self._active_invites[nonce] = {
            "tenant": tenant_id,
            "expires": exp.timestamp(),
        }

        logger.info("mesh_invite_created", nonce=nonce, tenant=tenant_id)
        return code

    def validate_invite(self, code: str) -> dict[str, Any]:
        """Verify an invite code is valid and active."""
        try:
            payload = jwt.decode(code, self.secret_key, algorithms=["HS256"])
            nonce = payload.get("nonce")

            if nonce not in self._active_invites:
                raise ValueError("Invalid or expired invite (nonce not found)")

            stored = self._active_invites[nonce]
            if time.time() > stored["expires"]:
                del self._active_invites[nonce]
                raise ValueError("Invite expired")

            from typing import cast

            return cast(dict[str, Any], payload)

        except jwt.PyJWTError as e:
            raise ValueError(f"Invalid token: {e}")

    def register_peer(self, peer_id: str, name: str, url: str, token: str):
        """Register a trusted peer after successful handshake."""
        # Clean up invite if used? (Optional, kept for multiple peers or one-time)
        self._peers[peer_id] = PeerInfo(
            peer_id=peer_id,
            name=name,
            url=url,
            token=token,
            created_at=time.time(),
        )
        logger.info("mesh_peer_registered", peer_id=peer_id, name=name)

    def get_peer(self, peer_id: str) -> PeerInfo | None:
        return self._peers.get(peer_id)

    def list_peers(self) -> list[PeerInfo]:
        return list(self._peers.values())

    def revoke_peer(self, peer_id: str):
        if peer_id in self._peers:
            del self._peers[peer_id]
            logger.info("mesh_peer_revoked", peer_id=peer_id)
