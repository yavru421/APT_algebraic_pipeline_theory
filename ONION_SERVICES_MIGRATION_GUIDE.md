# FuseTor Onion Services Migration Guide

## FuseTor Unified Master Specification

This migration guide is now **canonically aligned** with the FuseTor Unified Master Prompt. The FuseTor system is a Raspberry Pi-hosted, Tor-native micro-SaaS platform that provides private AI agents, encrypted vaults, anonymous automation daemons, and owner-controlled fusebox service toggles with a subscription engine.

### System Identity

FuseTor provides:

- Private AI agents (Groq/Llama integration)
- Encrypted vaults for file storage
- Anonymous automation daemons
- Owner-controlled fusebox service toggles
- Subscription engine with trials, billing states, and per-service fuses

**Platform Stack:**

- Raspberry Pi 4 / ARM64, Debian Bookworm
- Nginx (port 80), FastAPI backend (port 5001)
- Tor v3 Hidden Services, Tailscale HTTPS Funnel
- SQLite database with ORM models
- Docker containerization for per-user services

### APT Modular Decomposition

The complete FuseTor system follows APT methodology:

```bash
Y = m₁₂(m₁₁(...m₁(X)))
```

Where X = raw Raspberry Pi system, Y = production FuseTor platform

**Modules (mₖ):**

1. **m₁ — System Bootstrap**: directories, users, dependencies
2. **m₂ — Database Layer**: SQLite schema + ORM models
3. **m₃ — Backend API**: FastAPI + routing + auth + billing
4. **m₄ — Fuse Engine**: service state logic, trial countdowns
5. **m₅ — Docker Services**: per-user containers, isolation
6. **m₆ — Tor Layer**: onion service generation + routing
7. **m₇ — Nginx Layer**: reverse proxy and static hosting
8. **m₈ — FuseBox UI**: realistic breaker panel interface
9. **m₉ — Customer Portal UI**: subscription and service management
10. **m₁₀ — Deployment Pipeline**: scp, cp, systemctl wrappers
11. **m₁₁ — Monitoring + Strict Mode**: logging, fatal handling
12. **m₁₂ — Migration + Onion Rotation**: this guide and maintenance

## Overview

This document provides exact instructions for implementing and maintaining the FuseTor platform on the specific Raspberry Pi system. FuseTor is a complete micro-SaaS platform with subscription management, Docker containerization, and Tor anonymity.

**System Context:**

- Hardware: Raspberry Pi 4 (ARM64 architecture)
- OS: Debian Bookworm
- Hostname: raspberrypitailnet.tail85f090.ts.net (via Tailscale)
- SSH Access: jdd@100.115.115.21 (password: 5211)
- User: jdd (sudo access)
- Platform: Complete FuseTor micro-SaaS with AI agents, vaults, and fusebox controls

## API Specifications

### Netlify Llama Proxy OpenAPI Specification

```yaml
# Algebraic Pipeline Theory (APT) Methodology Applied
# Step 1: Modular Pipeline Construction
# Let x_1 = Netlify universal proxy OpenAPI spec
# Let y_1 = {info, servers, tags, paths, components} = modular pipeline sections
openapi: 3.0.0
info: # y_1[0]
  title: Netlify Llama Universal Proxy API
  version: 1.0.0
  description: |
    Universal proxy API for Llama endpoints, served via Netlify Functions. Drag-and-drop compatible for any frontend project. All Llama API endpoints are accessible via a single Netlify function endpoint.
servers: # y_1[1]
  - url: https://llama-universal-netlify-project.netlify.app/.netlify/functions/llama-proxy
    description: Production Netlify Proxy
  - url: http://localhost:8888/.netlify/functions/llama-proxy
    description: Local Netlify Dev Proxy

# Step 2: Paths as Pipeline Modules
paths: # y_1[3]
  /:
    post:
      # Let p_1 = /, r_1 = request, q_1 = response
      tags: [Proxy]
      summary: Proxy any Llama API endpoint
      description: |
        Forwards the request to the Llama API endpoint specified by the `path` query parameter (e.g., /chat/completions, /upload-image).
      parameters:
        - in: query
          name: path
          required: true
          schema:
            type: string
          description: Llama API path to proxy (e.g., /chat/completions)
      requestBody: # r_1
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProxyRequest' # s_1
      responses: # q_1
        '200':
          description: Success (proxied response from Llama API)
          content:
            application/json:
              schema:
                type: object
        '400':
          description: Bad request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse' # s_2
        '500':
          description: Internal error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse' # s_2

# Step 3: Components as Pipeline Modules
components: # y_1[4]
  schemas:
    ProxyRequest: # s_1
      type: object
      description: Request body is passed directly to the Llama API endpoint.
      additionalProperties: true
    ErrorResponse: # s_2
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [message]
          properties:
            message:
              type: string
```

## Database Schema (SQLite)

FuseTor uses SQLite with ORM models for complete subscription and service management:

### users table

```sql
id INTEGER PRIMARY KEY
username TEXT UNIQUE
password_hash TEXT
api_key TEXT UNIQUE
created_at TIMESTAMP
trial_ends TIMESTAMP
subscription_status TEXT      -- trial | active | expired
deleted BOOLEAN
```

### services table

```sql
id INTEGER PRIMARY KEY
user_id INTEGER REFERENCES users(id)
service_name TEXT
onion_address TEXT
status TEXT                  -- running | stopped | disabled
last_change TIMESTAMP
plan TEXT                    -- free_trial | basic | pro
usage_limit INTEGER
usage_current INTEGER
```

### logs table

```sql
id INTEGER PRIMARY KEY
user_id INTEGER
service_name TEXT
event TEXT
timestamp TIMESTAMP
```

### billing table

```sql
id INTEGER PRIMARY KEY
user_id INTEGER
service_name TEXT
renewal_date TIMESTAMP
status TEXT
payment_method TEXT
```

## Backend API (FastAPI)

FuseTor implements comprehensive REST API endpoints:

### Authentication Endpoints

- `POST /api/customer/create` - User registration
- `POST /api/customer/login` - User authentication
- `POST /api/customer/logout` - Session termination

### Subscription & Trials

- `GET /api/customer/services` - Fetch user services from DB
- `POST /api/customer/upgrade` - Change billing plan
- `POST /api/customer/delete` - Delete account + disable services

### Fuse Control

- `POST /api/toggle` - Enable/disable service (fuse control)
- `GET /api/status` - Fetch fuse states + system load

### Agent Services

- `POST /api/agents/generate` - Call Groq/Llama API for AI generation

### Vault Services

- `POST /api/vault/upload` - Encrypted file storage

### API Logging

- `GET /api/logs` - Retrieve user activity logs

Backend enforces subscription validation, trial expiration, and attaches onion addresses per service.

## Docker Service Architecture

Each customer-selected fuse maps to an isolated Docker container:

- **Per-service Dockerfiles**: Generated for ARM64 + AMD64 compatibility
- **Container Management**: Start/stop/restart per fuse via API
- **Metadata Storage**: Container state stored in SQLite database
- **Directory Structure**: `/home/jdd/fusetor_containers/generated/<user>/<service>/`

## Directory Structure (FuseTor Authoritative)

```bash
/var/www/hybrid/                    # Nginx static root
    index.html                      # FuseBox UI (breaker panel)
    customer.html                   # Customer-facing portal
    css/                            # FuseBox + Portal styling
    js/                             # FuseBox + Portal scripts

/home/jdd/hybrid_api/              # FastAPI backend
    main.py
    db.py
    models.py
    fuse_logic.py
    billing.py
    strict_mode.py
    logs/

/home/jdd/fusetor_containers/      # Docker services for users
    templates/
    generated/

/etc/nginx/sites-enabled/hybrid    # Nginx config
/etc/tor/torrc                     # Tor hidden service configuration
```

### Core Services

- **Nginx Web Server**: Port 80, serves static files from `/var/www/hybrid/`
- **FastAPI Backend**: Port 5001, proxied via Nginx at `/api/`
- **Tor Hidden Services**: Onion addresses for anonymous access
- **Tailscale Funnel**: HTTPS at `https://raspberrypitailnet.tail85f090.ts.net/`

### Directory Structure

```bash
/var/www/hybrid/          # Nginx root for static files
├── index.html           # Main portal page
├── admin.html           # Admin dashboard
├── dashboard.html       # User dashboard
├── ffmpeg.html          # FFmpeg service page
├── apt.html            # APT pipeline page
├── logs.html           # Logs page
├── hidden.html         # Hidden services page
├── chat.html           # Chat service page
├── llama.html          # Llama API page
├── mitmproxy.html      # MITM proxy page
└── hybrid.html         # Hybrid API page

/home/jdd/
├── index.html          # Staging area for deployments
├── hybrid_api/         # FastAPI application
│   ├── main.py         # FastAPI app
│   ├── nexus_agent.py  # Log monitoring
│   ├── strict_mode.py  # Fatal error handler
│   ├── traffic_log.csv # Traffic data
│   └── apt_nexus_incidents.log # Security logs
└── chat_app/           # Chat service
    └── app.py          # Flask-SocketIO chat app

/etc/nginx/sites-enabled/hybrid  # Nginx config
/etc/tor/torrc                   # Tor config
/var/log/nginx/                  # Nginx logs
```

## User Interface (UI) Specifications

### Portal Page (index.html)

- **Purpose**: Main landing page with service selection
- **Features**:
  - Service cards for FFmpeg, APT, Logs, Chat, Llama, MITM
  - Real-time status indicators
  - User authentication (if enabled)
  - Responsive design with modern UI

### Admin Dashboard (admin.html)

- **Purpose**: Administrative interface for system management
- **Features**:
  - User management
  - Service monitoring
  - Log viewing
  - Configuration management
  - System health metrics

### User Dashboard (dashboard.html)

- **Purpose**: User-specific interface for service interaction
- **Features**:
  - Service usage history
  - Personal settings
  - API key management
  - Billing information (if applicable)

### Service Pages

- **FFmpeg Generator** (ffmpeg.html): Command generation interface
- **APT Pipeline** (apt.html): Pipeline construction and execution
- **Logs Viewer** (logs.html): Log analysis and monitoring
- **Chat Service** (chat.html): Real-time chat interface
- **Llama API** (llama.html): AI model interaction
- **MITM Proxy** (mitmproxy.html): Network traffic analysis
- **Hybrid API** (hybrid.html): Unified API interface

## Tor Hidden Service Configuration

### Current Active Onion Addresses

- **Primary v3 Onion**: `http://wmwejh36zcvsgmesq34nwdcmvef3rxfskfbw62sz4ppg3feb23moofad.onion`
  - Status: Active, all pages return HTTP 200
  - Used for: ffmpeg.html, apt.html, logs.html, hidden.html

- **Deprecated Onions** (do not use):
  - `http://5q4m6ejy7237m4cimsxagpyfbk4nhc6n5ipeehsaklb7mhalaifp3myd.onion` (returns 502)
  - `http://4wcmad.onion` (v2, unsupported by modern Tor)

### Tor Configuration (/etc/tor/torrc)

```bash
# Tor Hidden Service Configuration
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:80
```

**Note**: The onion address is auto-generated and stored in `/var/lib/tor/hidden_service/hostname`. Do not modify this file manually.

### Tor Service Management

```bash
# Check status
sudo systemctl status tor

# Restart after config changes
sudo systemctl restart tor

# View logs
sudo journalctl -u tor -f
```

## Nginx Configuration

### Site Config (/etc/nginx/sites-enabled/hybrid)

```nginx
server {
    listen 80;
    server_name _;

    root /var/www/hybrid;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:5001/;
    }
}
```

### Nginx Management

```bash
# Test config
sudo nginx -t

# Reload config
sudo systemctl reload nginx

# Restart
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx
```

## Deployment Workflow

### Static File Deployment

1. **Upload to staging**:

   ```bash
   scp /path/to/file.html jdd@100.115.115.21:/home/jdd/file.html
   ```

2. **Copy to production**:

   ```bash
   ssh jdd@100.115.115.21 "sudo cp /home/jdd/file.html /var/www/hybrid/file.html"
   ```

3. **Restart Nginx**:

   ```bash
   ssh jdd@100.115.115.21 "sudo systemctl restart nginx"
   ```

4. **Verify deployment**:

   ```bash
   ssh jdd@100.115.115.21 "wc -c /var/www/hybrid/file.html"
   ssh jdd@100.115.115.21 "tail -20 /var/log/nginx/access.log"
   ```

### API Deployment

1. **Upload code**:

   ```bash
   scp -r /path/to/api/ jdd@100.115.115.21:/home/jdd/
   ```

2. **Install dependencies** (if needed):

   ```bash
   ssh jdd@100.115.115.21 "cd /home/jdd/api && pip install -r requirements.txt"
   ```

3. **Start service**:

   ```bash
   ssh jdd@100.115.115.21 "cd /home/jdd/api && python main.py"
   ```

   (Use screen/tmux for background execution)

## Tailscale Funnel Setup

### Enable Public HTTPS

```bash
ssh jdd@100.115.115.21 "sudo tailscale funnel 80"
```

- Provides HTTPS at: `https://raspberrypitailnet.tail85f090.ts.net/`
- Automatic Let's Encrypt certificates

### Check Funnel Status

```bash
ssh jdd@100.115.115.21 "tailscale serve status"
```

### Disable Funnel

```bash
ssh jdd@100.115.115.21 "sudo tailscale serve reset"
```

## Deployment and Maintenance Guide

### Site Maintenance Procedures

**Overview:**
This guide documents the process for maintaining and updating the Yavru421 site hosted on the Raspberry Pi. The site features an FFmpeg Command Generator with user-friendly colors to attract traffic, alongside APT Pipeline Tools for algebraic pipeline theory enthusiasts. The site disguises Tor access with modern UI design.

**Site Architecture:**

- **Host**: Raspberry Pi (ARM64, Debian Bookworm)
- **Web Server**: Nginx (port 80)
- **Backend API**: FastAPI/Uvicorn (port 5001, proxied via Nginx)
- **Public Access**: Tailscale Funnel (HTTPS via Let's Encrypt)
- **Anonymous Access**: Tor Hidden Service (.onion)
- **Static Files Root**: `/var/www/hybrid/`
- **API Directory**: `/home/jdd/hybrid_api/`
- **Logs Directory**: `/var/log/nginx/` and `/home/jdd/hybrid_api/logs/`

**File Structure:**

```bash
c:\Users\John\Desktop\APM\
├── index.html          # Main site (FFmpeg Generator & APT Tools)
├── SITE_MAINTENANCE.md # This guide
└── Other APT files...

/var/www/hybrid/
├── index.html          # Deployed main site (FFmpeg Generator & APT Tools)
├── logs.html           # Logs and analysis page
└── files/              # Downloadable artifacts

/home/jdd/hybrid_api/
├── main.py             # FastAPI app
├── nexus_agent.py      # Log monitoring agent
├── strict_mode.py      # Fatal error handler
├── traffic_log.csv     # Traffic data
└── apt_nexus_incidents.log  # Security incidents
```

**Updating the Site (index.html):**

1. **Local Development:**
   - Edit `index.html` in the APM workspace (`c:\Users\John\Desktop\APM\index.html`)
   - Test locally by opening in browser
   - Ensure all links and paths are relative or absolute as needed

2. **Deployment Steps:**
   - Upload to Pi Home Directory: `scp C:\Users\John\Desktop\APM\index.html jdd@100.115.115.21:/home/jdd/index.html`
   - Copy to Nginx Root: `ssh jdd@100.115.115.21 "sudo cp /home/jdd/index.html /var/www/hybrid/index.html"`
   - Verify Update: Access site at `https://raspberrypitailnet.tail85f090.ts.net/`, hard refresh browser (Ctrl+F5) if cached

**AI-Assisted Updates (Copilot Interface):**

- Edit Locally: Use `replace_string_in_file` to modify `c:\Users\John\Desktop\APM\index.html` with exact old and new strings, including 3-5 lines of context
- Deploy via Tools: Run SCP and SSH commands as documented
- Verify Deployment: Check file size and nginx logs
- Troubleshooting: Path mismatches, caching, permissions, fatal enforcement

**Tailscale Funnel Management:**

- Enable: `ssh jdd@100.115.115.21 "sudo tailscale funnel 80"`
- Check Status: `ssh jdd@100.115.115.21 "tailscale serve status"`
- Disable: `ssh jdd@100.115.115.21 "sudo tailscale serve reset"`

**Nginx Configuration:**

- Config Location: `/etc/nginx/sites-enabled/hybrid`
- Restart: `ssh jdd@100.115.115.21 "sudo systemctl restart nginx"`

**API Management:**

- Start API: `ssh jdd@100.115.115.21 "cd /home/jdd/hybrid_api && python main.py"`
- Check Status: `curl http://127.0.0.1:5001/health`

**Security Considerations:**

- All exceptions are fatal (strict_mode.py)
- Logs monitor for suspicious activity
- No hardcoded credentials
- Regular log rotation
- Access via Tailscale VPN for admin

## Security and Monitoring

### Fatal Error Handling

- All exceptions are fatal (no graceful degradation)
- Use `strict_mode.py` for exception handling
- Import `strict_mode` at the top of all Python scripts

### Logging

- **Nginx Logs**: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- **API Logs**: `/home/jdd/hybrid_api/logs/`
- **Traffic Monitoring**: `/home/jdd/hybrid_api/traffic_log.csv`
- **Security Incidents**: `/home/jdd/hybrid_api/apt_nexus_incidents.log`

### No Hardcoded Credentials

- Use environment variables for API keys
- Never commit secrets to repo
- Example: `LLAMA_API_KEY` must be set in environment

## Testing Onion Services

### Local Testing

```bash
# Test local pages
curl -sSI http://127.0.0.1/page.html | head -n 1
```

### Onion Testing via Tor

```bash
# Via SOCKS proxy (if Tor is running locally on Pi)
curl -sS --socks5-hostname 127.0.0.1:9050 -o /dev/null -w '%{http_code}\n' 'http://onion-address.onion/page.html'
```

### Browser Testing

- Use Tor Browser to access onion URLs
- Verify all links work and pages load

## Migration Checklist

### Files to Copy to New Repo

- `/var/www/hybrid/*.html` (all static pages)
- `/home/jdd/hybrid_api/` (API code)
- `/home/jdd/chat_app/app.py` (chat service)
- `/etc/nginx/sites-enabled/hybrid` (nginx config)
- `/etc/tor/torrc` (tor config, but regenerate keys for new setup)
- `SITE_MAINTENANCE.md` (deployment guide)
- This migration guide

### Environment Variables

- `LLAMA_API_KEY`: Required for chat service
- Any other API keys used in services

### Dependencies

- Python packages: flask, flask-socketio, fastapi, uvicorn, requests, eventlet
- System packages: nginx, tor, python3-dev, etc.

### DNS/Networking

- Tailscale node: raspberrypitailnet.tail85f090.ts.net
- SSH: jdd@100.115.115.21
- Ports: 80 (nginx), 5001 (api), 22 (ssh)

## Troubleshooting

### Common Issues

- **Site not updating**: Restart Nginx after file copy
- **Onion not working**: Check Tor service status, verify config
- **API not responding**: Check port 5001, restart API service
- **Permissions errors**: Use `sudo` for system operations

### Log Analysis

```bash
# Nginx errors
ssh jdd@100.115.115.21 "tail -50 /var/log/nginx/error.log"

# API logs
ssh jdd@100.115.115.21 "tail -50 /home/jdd/hybrid_api/logs/*.log"

# Tor logs
ssh jdd@100.115.115.21 "sudo journalctl -u tor -n 50"
```

## Future Enhancements

### Additional Onion Services

1. Generate new v3 onion keypair
2. Add HiddenServiceDir entry to `/etc/tor/torrc`
3. Configure Nginx server block for new service
4. Deploy content to new root directory
5. Restart Tor and Nginx

### Scaling

- Consider separate Nginx configs for multiple services
- Use systemd for API services
- Implement load balancing if needed

## Contact and Maintenance

- **Maintainer**: JD Dondlinger (APT Theorist & Carpenter)
- **SSH Access**: jdd@100.115.115.21 (password: 5211)
- **HTTPS Access**: `https://raspberrypitailnet.tail85f090.ts.net/`
- **Onion Access**: `http://wmwejh36zcvsgmesq34nwdcmvef3rxfskfbw62sz4ppg3feb23moofad.onion`

---

**Migration Complete**: This document captures all essential information for the TorFuse onion services system. Use it as the foundation for the new dedicated repo.
