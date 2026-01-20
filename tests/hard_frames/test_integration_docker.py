import pytest
import subprocess
import requests
import time

@pytest.mark.integration
class TestHardFramesIntegration:
    """
    These tests require the Docker environment to be running:
    docker compose -f docker-compose.secure.yml up -d
    """

    def _get_container_id(self, service_name):
        """Helper to get container ID more reliably."""
        try:
            # Look for the container in the 'hard_frames' project
            cmd = ["docker", "ps", "--filter", f"label=com.docker.compose.project=hard_frames", "--filter", f"label=com.docker.compose.service={service_name}", "--filter", "status=running", "-q"]
            output = subprocess.check_output(cmd, text=True).strip()
            if not output:
                # Fallback to compose ps with project name
                output = subprocess.check_output(
                    ["docker", "compose", "-f", "docker-compose.secure.yml", "-p", "hard_frames", "ps", "-q", service_name],
                    text=True
                ).strip()
            return output.split('\n')[0] if output else None
        except Exception:
            return None

    def test_agent_container_is_isolated(self):
        """
        Verify that the 'rae-agent-secure' container cannot access the internet.
        """
        container_id = self._get_container_id("rae-agent-secure")
        if not container_id:
            pytest.skip("Docker container rae-agent-secure is not running")

        # Attempt to access Google from INSIDE the container
        cmd = [
            "docker", "exec", container_id,
            "python", "-c", "import requests; print(requests.get('https://google.com', timeout=2).status_code)"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert "200" not in result.stdout, "SECURITY BREACH: Agent accessed Google!"
        assert result.returncode != 0 or "ConnectionError" in str(result.stderr) or "ConnectionError" in str(result.stdout)

    def test_agent_can_reach_kernel(self):
        """
        Verify that the agent CAN reach the RAE Kernel.
        """
        agent_id = self._get_container_id("rae-agent-secure")
        kernel_id = self._get_container_id("rae-kernel")
        
        if not agent_id or not kernel_id:
            pytest.skip("Docker containers are not running")

        # Dynamically get Kernel IP within the isolated network
        try:
            # We specifically want the IP on the internal network to verify connectivity there
            # Note: The network name is prefixed with the project name 'hard_frames'
            kernel_ip = subprocess.check_output(
                ["docker", "inspect", "-f", "{{.NetworkSettings.Networks.hard_frames_rae_internal.IPAddress}}", kernel_id],
                text=True
            ).strip()
        except Exception as e:
            pytest.fail(f"Could not inspect Kernel IP: {e}")

        # Retry loop for service readiness
        max_retries = 10
        success = False
        last_error = ""
        for i in range(max_retries):
            cmd = [
                "docker", "exec", agent_id,
                "python", "-c", f"import requests; print(requests.get('http://{kernel_ip}:8000/health').status_code)"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if "200" in result.stdout:
                success = True
                break
            last_error = result.stderr or result.stdout
            time.sleep(2)

        assert success, f"Agent could not reach Kernel at {kernel_ip}! Last output: {last_error}"

    def test_agent_has_no_forbidden_tools(self):
        """
        Verify that curl, wget, git are missing.
        """
        container_id = self._get_container_id("rae-agent-secure")
        if not container_id:
            pytest.skip("Docker container rae-agent-secure is not running")

        for tool in ["curl", "wget", "git", "ssh"]:
            cmd = ["docker", "exec", container_id, "which", tool]
            result = subprocess.run(cmd, capture_output=True)
            assert result.returncode != 0, f"SECURITY FAIL: {tool} found in container!"
