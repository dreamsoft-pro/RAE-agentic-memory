import subprocess

import pytest


@pytest.mark.integration
class TestAgentContainment:
    """
    Hard Frames Phase 1 & 2: Physical Impossibility & Protocol Exclusivity.
    These tests execute malicious code INSIDE the agent container to prove it cannot escape.
    """

    def _get_agent_id(self):
        try:
            cmd = [
                "docker",
                "ps",
                "--filter",
                "label=com.docker.compose.project=hard_frames",
                "--filter",
                "label=com.docker.compose.service=rae-agent-secure",
                "--filter",
                "status=running",
                "-q",
            ]
            return subprocess.check_output(cmd, text=True).strip()
        except:
            return None

    def _exec_in_agent(self, python_code):
        container_id = self._get_agent_id()
        if not container_id:
            pytest.skip("Agent container not running")

        cmd = ["docker", "exec", container_id, "python", "-c", python_code]
        return subprocess.run(cmd, capture_output=True, text=True)

    def test_sdk_escape_attempt(self):
        """
        Phase 1.3: SDK Escape Test.
        Verify that proprietary LLM SDKs are NOT installed.
        """
        # Try to import forbidden libraries
        code = """
try:
    import openai
    print("OPENAI_FOUND")
except ImportError:
    print("CLEAN")

try:
    import anthropic
    print("ANTHROPIC_FOUND")
except ImportError:
    print("CLEAN")
"""
        result = self._exec_in_agent(code)
        assert "OPENAI_FOUND" not in result.stdout, "SECURITY FAIL: openai SDK found!"
        assert (
            "ANTHROPIC_FOUND" not in result.stdout
        ), "SECURITY FAIL: anthropic SDK found!"
        assert result.returncode == 0

    def test_direct_socket_escape(self):
        """
        Phase 2.1: Direct Socket Test.
        Verify that opening a raw socket triggers the Monkey Patch RuntimeError.
        """
        # Try to connect to 1.1.1.1 (Cloudflare DNS) on port 80
        code = """
import socket
import sys
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("1.1.1.1", 80))
    print("CONNECTED")
except RuntimeError as e:
    print(f"PATCH_BLOCKED: {e}")
except Exception as e:
    print(f"ERROR: {e}")
"""
        result = self._exec_in_agent(code)
        # We accept either our custom patch error OR the OS-level "Network is unreachable"
        assert (
            "PATCH_BLOCKED" in result.stdout
            or "Network is unreachable" in result.stdout
        )
        assert "CONNECTED" not in result.stdout

    def test_protocol_bypass_attempt(self):
        """
        Phase 2.2: Protocol Bypass.
        Verify agent cannot probe internal localhost ports blindly.
        """
        # Try to scan localhost ports inside the container (should be empty except self)
        code = """
import socket
for port in [22, 80, 443, 5432, 6379]:
    try:
        s = socket.socket()
        s.settimeout(0.1)
        if s.connect_ex(("127.0.0.1", port)) == 0:
            print(f"OPEN:{port}")
        s.close()
    except:
        pass
"""
        result = self._exec_in_agent(code)
        assert (
            "OPEN:" not in result.stdout
        ), "SECURITY WARN: Agent found open ports on localhost!"
