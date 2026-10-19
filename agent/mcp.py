"""MCP registry boundary. v5.7 keeps transport separate from the core agent tools."""
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass
class MCPServer:
    name: str
    command: str = ""
    args: list[str] | None = None
    enabled: bool = True
    trusted: bool = False

class MCPRegistry:
    def __init__(self, servers=None):
        self.servers={s.name:s for s in (servers or [])}
    def register(self, server): self.servers[server.name]=server
    def remove(self, name): self.servers.pop(name, None)
    def enable(self, name, enabled=True):
        if name in self.servers: self.servers[name].enabled=enabled
    def list_servers(self): return [asdict(s) for s in self.servers.values()]
    def available(self): return [s for s in self.servers.values() if s.enabled]
    def manifest(self):
        return [{"name":s.name,"command":s.command,"args":s.args or [],"enabled":s.enabled,"trusted":s.trusted} for s in self.available()]
