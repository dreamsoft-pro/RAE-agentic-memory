import asyncio
import aiohttp
import json
import sys

async def main():
    base_url = "http://localhost:9001"
    sse_url = f"{base_url}/sse"
    
    print(f"Connecting to SSE: {sse_url}")
    
    async with aiohttp.ClientSession() as session:
        # 1. Connect to SSE stream
        async with session.get(sse_url) as response:
            if response.status != 200:
                print(f"Failed to connect: {response.status}")
                return

            print("Connected to SSE stream.")
            
            # Read the first event to get the session endpoint (endpoint)
            endpoint_url = None
            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith("event: endpoint"):
                    # The next line should be data: <url>
                    continue
                if line.startswith("data:"):
                    # Extract relative path
                    path = line[5:].strip()
                    endpoint_url = f"{base_url}{path}"
                    print(f"Session Endpoint found: {endpoint_url}")
                    break
            
            if not endpoint_url:
                print("Could not find session endpoint.")
                return

            # 2. Send 'initialize' request via POST
            init_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "gemini-cli", "version": "1.0"}
                }
            }
            
            print("Sending initialize...")
            async with session.post(endpoint_url, json=init_payload) as post_resp:
                print(f"Init response: {post_resp.status}")
                # We expect response on SSE stream, but for now let's just assume it works 
                # and send tools/list immediately if 200/202.
            
            # 3. Send 'get_latest_telemetry' for TJ02
            call_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_latest_telemetry",
                    "arguments": {
                        "machine_code": "TJ02"
                    }
                }
            }
            
            print("Sending get_latest_telemetry for TJ02...")
            async with session.post(endpoint_url, json=call_payload) as post_resp:
                print(f"Call response: {post_resp.status}")

            # 4. Listen for responses on SSE
            print("Listening for responses (Ctrl+C to stop)...")
            try:
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                        try:
                            data = json.loads(data_str)
                            print("\n=== MESSAGE RECEIVED ===")
                            print(json.dumps(data, indent=2))
                            
                            # If we got the result for id 2 (tools/list), we are done
                            if data.get("id") == 2:
                                break
                        except:
                            pass
            except KeyboardInterrupt:
                pass

if __name__ == "__main__":
    asyncio.run(main())
