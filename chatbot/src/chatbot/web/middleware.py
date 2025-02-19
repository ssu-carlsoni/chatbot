import ipaddress
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class IPRestrictionMiddleware:
    def __init__(self):
        # Define allowed IP networks: localhost, IPv6 loopback, 172.16.0.0/12, and 130.157.0.0/16
        self.allowed_networks = [
            ipaddress.ip_network("127.0.0.1/32"),
            ipaddress.ip_network("::1/128"),
            ipaddress.ip_network("172.16.0.0/12"),
            ipaddress.ip_network("130.157.0.0/16"),
        ]

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host

        try:
            ip_addr = ipaddress.ip_address(client_ip)
        except ValueError:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid IP address"}
            )

        # Check if the client's IP is within any allowed network
        if not any(ip_addr in network for network in self.allowed_networks):
            return JSONResponse(
                status_code=403,
                content={"detail": "Access denied: IP not in allowed range"}
            )

        response = await call_next(request)
        return response
