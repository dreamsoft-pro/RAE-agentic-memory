# RAE Mesh Protocol: Privacy-First Synchronization

## 1. Overview
RAE Mesh allows decentralized synchronization between RAE instances (e.g., Laptop <-> Server, or User A <-> User B).
The core principle is **User Consent**. No instance can connect to another without an explicit "Trust Handshake".

## 2. Terminology
- **Host**: The instance generating an invitation.
- **Joiner**: The instance accepting the invitation.
- **Invite Code**: A short-lived, signed token used to establish trust.
- **Peer Token**: A long-lived API token scoped to `mesh:sync` permissions.

## 3. The Trust Handshake (User Consent Flow)

### Step 1: Invitation (Host)
User A (Host) requests an invite code via `POST /v2/mesh/invites`.
- RAE generates a JWT-based code containing: `{ "host_url": "...", "exp": 300, "nonce": "..." }`.
- This code is displayed to User A.

### Step 2: Joining (Joiner)
User B (Joiner) enters the code via `POST /v2/mesh/peers/join`.
- Joiner decodes the invite.
- Joiner sends a `POST /v2/mesh/handshake` to the Host's URL using the code.
- Payload includes Joiner's `public_url` and a generated `peer_token` for the Host to use back.

### Step 3: Confirmation (Host)
Host receives the handshake.
- Validates the invite code (nonce, expiration).
- Stores the Joiner's `peer_token`.
- Generates a `host_token` for the Joiner.
- Returns `host_token` in the response.

### Step 4: Established Trust
Both parties now have:
- The remote URL.
- A valid authentication token for that remote.
- A stored `peer_id`.

## 4. Synchronization Flow (API v2)
Once trusted, peers use the `ISyncProvider` interface over HTTP.

- **Push**: `POST /v2/mesh/sync/push`
- **Pull**: `POST /v2/mesh/sync/pull`

All requests MUST include the `X-RAE-Peer-Token` header.
