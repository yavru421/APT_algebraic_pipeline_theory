# GitHub Copilot: Generate Complete FuseTor Onion Services Platform

## System Specification

You are tasked with implementing the complete **FuseTor Onion Services Platform** - a Raspberry Pi-hosted, Tor-native micro-SaaS platform that provides private AI agents, encrypted vaults, anonymous automation daemons, and owner-controlled fusebox service toggles with a subscription engine.

**Platform Identity:**

- Private AI agents (Groq/Llama integration)
- Encrypted vaults for file storage
- Anonymous automation daemons
- Owner-controlled fusebox service toggles
- Subscription engine with trials, billing states, and per-service fuses

**Technology Stack:**

- Raspberry Pi 4 / ARM64, Debian Bookworm
- Nginx (port 80), FastAPI backend (port 5001)
- Tor v3 Hidden Services, Tailscale HTTPS Funnel
- SQLite database with ORM models
- Docker containerization for per-user services

## APT Methodology Implementation

Implement the system using **Algebraic Pipeline Theory (APT)** with this exact modular decomposition:

```text
Y = m₁₂(m₁₁(...m₁(X)))
```

Where X = raw Raspberry Pi system, Y = production FuseTor platform

**Implementation Order (Critical - Follow Exactly):**

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
12. **m₁₂ — Migration + Onion Rotation**: maintenance and updates

## Database Schema (Implement First)

Create SQLite database with these exact tables:

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

## API Endpoints (Implement Second)

Create FastAPI application with these exact endpoints:

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

## Docker Architecture (Implement Third)

Each customer-selected fuse maps to an isolated Docker container:

- **Per-service Dockerfiles**: Generated for ARM64 + AMD64 compatibility
- **Container Management**: Start/stop/restart per fuse via API
- **Metadata Storage**: Container state stored in SQLite database
- **Directory Structure**: `/home/jdd/fusetor_containers/generated/<user>/<service>/`

## Directory Structure (Create This First)

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

## UI Specifications (Implement Fourth)

### FuseBox UI (index.html) - Realistic Breaker Panel

- Visual circuit breaker interface
- Each service = breaker switch
- Status indicators (green/red/yellow)
- Click to toggle services on/off
- Real-time status updates via WebSocket/polling

### Customer Portal (customer.html)

- Login/registration forms
- Service selection and management
- Billing information display
- Usage statistics and limits
- Subscription upgrade options

## Security Requirements (Implement Throughout)

### Fatal Error Handling

```python
# strict_mode.py - Import at top of ALL Python files
import sys, traceback
def strict_excepthook(exc_type, exc_value, exc_tb):
    print(f"\n❌ APT FATAL ERROR: {exc_type.name} – {exc_value}")
    traceback.print_tb(exc_tb)
    sys.exit(1)
sys.excepthook = strict_excepthook
print("⚙️ APT Fatal Mode Active: All exceptions are terminal.")
```

### No Hardcoded Credentials

- Use environment variables: `LLAMA_API_KEY`, `GROQ_API_KEY`
- Never commit secrets to repository
- Secure password hashing for user accounts

## Implementation Instructions

1. **Start with Database Layer** (m₂)
   - Create SQLAlchemy models matching exact schema above
   - Implement database initialization and migrations
   - Add proper indexing for performance

2. **Build FastAPI Backend** (m₃)
   - Implement all endpoints listed above
   - Add JWT authentication
   - Integrate with database models
   - Add request/response validation

3. **Add Fuse Logic** (m₄)
   - Service state management
   - Trial expiration handling
   - Usage limit enforcement
   - Billing state transitions

4. **Implement Docker Services** (m₅)
   - Container creation and management
   - ARM64 compatibility
   - Service isolation per user
   - Resource limits and monitoring

5. **Configure Tor Layer** (m₆)
   - v3 onion service generation
   - Automatic address assignment
   - Service routing and isolation

6. **Setup Nginx** (m₇)
   - Reverse proxy configuration
   - Static file serving
   - SSL termination (via Tailscale)

7. **Create UIs** (m₈, m₉)
   - FuseBox breaker panel interface
   - Customer portal with subscription management
   - Real-time status updates
   - Responsive design

8. **Add Deployment Tools** (m₁₀)
   - Automated deployment scripts
   - Service management wrappers
   - Configuration validation

9. **Implement Monitoring** (m₁₁)
   - Comprehensive logging
   - Fatal error handling throughout
   - Performance monitoring
   - Security incident detection

## Testing Requirements

- Unit tests for each module
- Integration tests for API endpoints
- Docker container testing
- UI functionality testing
- Security testing (no credential leaks)

## Final Deliverables

Produce a complete, production-ready FuseTor platform with:

1. **Complete source code** for all 12 APT modules
2. **Docker Compose** configuration for the entire stack
3. **Deployment scripts** for Raspberry Pi setup
4. **Documentation** matching the migration guide
5. **Test suite** with comprehensive coverage
6. **Security audit** confirming no hardcoded credentials

## Critical Success Criteria

- **Fatal Error Handling**: All exceptions terminate execution with full traceback
- **No Hardcoded Secrets**: Environment variables only for API keys
- **APT Compliance**: Each module implements its algebraic contract
- **Tor Native**: All services accessible via .onion addresses
- **Subscription Engine**: Complete trial/billing/user management
- **Docker Isolation**: Per-user service containerization
- **Real-time UI**: FuseBox interface with live status updates

Generate the complete FuseTor platform following this specification exactly.

