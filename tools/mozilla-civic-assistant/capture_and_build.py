import asyncio
from playwright.async_api import async_playwright
import time
import os
import subprocess

async def capture():
    print("🎬 Starting screen capture process...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        # 1. Initial State
        print("📸 Capturing initial state...")
        await page.goto("http://localhost:8502")
        await asyncio.sleep(5) # Wait for connect
        await page.screenshot(path="slides/final_01.png")
        
        # 2. Results State
        print("📸 Capturing query results...")
        await page.fill("input[placeholder='e.g., Summary of budget changes']", "Mozilla strategy")
        await page.click("text=Audit Records")
        await asyncio.sleep(10) # Wait for Qwen/DeepSeek
        await page.screenshot(path="slides/final_02.png")
        
        # 3. Stats State (Refresh)
        print("📸 Capturing stats state...")
        await page.click("i:has-text('refresh')")
        await asyncio.sleep(5)
        await page.screenshot(path="slides/final_03.png")
        
        await browser.close()

def build_video():
    print("🎞️ Assembling video from slides...")
    # Use the ffmpeg we found earlier
    ffmpeg = "/tmp/videoenv/bin/ffmpeg"
    cmd = [
        ffmpeg, "-y", "-framerate", "1/5", 
        "-pattern_type", "glob", "-i", "slides/final_*.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25",
        "-movflags", "+faststart", "../../../mozilla_presentation.mp4"
    ]
    subprocess.run(cmd)
    print("✅ Video created: mozilla_presentation.mp4")

if __name__ == "__main__":
    os.makedirs("slides", exist_ok=True)
    asyncio.run(capture())
    build_video()
