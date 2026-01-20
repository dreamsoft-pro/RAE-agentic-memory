import sys
import socket
import os

# --- HARD FRAME: PROTOCOL EXCLUSIVITY (Phase 2.1) ---
_real_socket = socket.socket
_kernel_host = None # Lazy init
_allowed_ips = set()

def _get_kernel_host():
    global _kernel_host
    if _kernel_host is None:
        url = os.getenv("RAE_KERNEL_URL", "172.29.99.2")
        # Strip protocol
        if "//" in url:
            host_part = url.split("//")[-1]
        else:
            host_part = url
        # Strip port and path
        _kernel_host = host_part.split(":")[0].split("/")[0]
        
        # Resolve to IP to allow socket level whitelisting
        try:
            # Resolve both IPv4 and IPv6
            info = socket.getaddrinfo(_kernel_host, None)
            for res in info:
                _allowed_ips.add(res[4][0])
            print(f"🔒 HARD FRAMES: Whitelisted IPs for {_kernel_host}: {_allowed_ips}")
        except Exception as e:
            print(f"⚠️  HARD FRAMES WARNING: Could not resolve {_kernel_host}: {e}")
            
    return _kernel_host

class SecureSocket(_real_socket):
    """
    A Secure Wrapper around standard Python socket.
    Enforces Hard Frames protocol exclusivity at the application layer.
    """
    def connect(self, address):
        host = address[0] # IP or Hostname
        
        # Ensure whitelist is populated
        allowed_hostname = _get_kernel_host()
        
        # Whitelist Logic
        is_allowed = (
            host == allowed_hostname or 
            host in _allowed_ips or
            host == "127.0.0.1" or 
            host == "localhost"
        )
        
        if not is_allowed:
             # Strict Enforcement
             raise RuntimeError(f"🚨 HARD FRAME BREACH: Connection to {host} denied. Only {allowed_hostname} ({list(_allowed_ips)}) allowed.")
             
        # Proceed with connection
        return super().connect(address)

def apply_hard_frames():
    """Enable process-level network restrictions. MUST BE CALLED BEFORE other imports."""
    target = _get_kernel_host()
    print(f"🔒 APPLYING HARD FRAMES: Network restricted to Kernel ({target}).")
    socket.socket = SecureSocket
