# Yavru421: Math is a Verb - Site Deployment and Maintenance Guide

## Overview
This guide documents the process for maintaining and updating the Yavru421 site hosted on the Raspberry Pi. The site features an FFmpeg Command Generator with user-friendly colors to attract traffic, alongside APT Pipeline Tools for algebraic pipeline theory enthusiasts. The site disguises Tor access with modern UI design.

## Site Architecture
- **Host**: Raspberry Pi (ARM64, Debian Bookworm)
- **Web Server**: Nginx (port 80)
- **Backend API**: FastAPI/Uvicorn (port 5001, proxied via Nginx)
- **Public Access**: Tailscale Funnel (HTTPS via Let's Encrypt)
- **Anonymous Access**: Tor Hidden Service (.onion)
- **Static Files Root**: `/var/www/hybrid/`
- **API Directory**: `/home/jdd/hybrid_api/`
- **Logs Directory**: `/var/log/nginx/` and `/home/jdd/hybrid_api/logs/`

## File Structure
```
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

## Updating the Site (index.html)

### Local Development
1. Edit `index.html` in the APM workspace (`c:\Users\John\Desktop\APM\index.html`)
2. Test locally by opening in browser
3. Ensure all links and paths are relative or absolute as needed

### Deployment Steps
1. **Upload to Pi Home Directory**:
   ```
   scp C:\Users\John\Desktop\APM\index.html jdd@100.115.115.21:/home/jdd/index.html
   ```

2. **Copy to Nginx Root**:
   ```
   ssh jdd@100.115.115.21 "sudo cp /home/jdd/index.html /var/www/hybrid/index.html"
   ```

3. **Verify Update**:
   - Access site at `https://raspberrypitailnet.tail85f090.ts.net/`
   - Hard refresh browser (Ctrl+F5) if cached

### AI-Assisted Updates (Copilot Interface)
When updating index.html via VS Code Copilot tools:

1. **Edit Locally**: Use `replace_string_in_file` to modify `c:\Users\John\Desktop\APM\index.html` with exact old and new strings, including 3-5 lines of context.

2. **Deploy via Tools**:
   - Run SCP: `run_in_terminal` with `scp C:\Users\John\Desktop\APM\index.html jdd@100.115.115.21:/home/jdd/index.html`
   - Copy to Nginx: `run_in_terminal` with `ssh jdd@100.115.115.21 "sudo cp /home/jdd/index.html /var/www/hybrid/index.html"`
   - Restart Nginx if needed: `run_in_terminal` with `ssh jdd@100.115.115.21 "sudo systemctl restart nginx"`

3. **Verify Deployment**:
   - Check file size: `run_in_terminal` with `ssh jdd@100.115.115.21 "wc -c /var/www/hybrid/index.html"`
   - Check nginx logs: `run_in_terminal` with `ssh jdd@100.115.115.21 "tail -20 /var/log/nginx/access.log"`
   - Ensure no JS errors by reviewing console or agent logs.

4. **Troubleshooting**:
   - Path mismatches: Always SCP to `/home/jdd/index.html`, then cp to `/var/www/hybrid/index.html`.
   - Caching: Restart nginx after cp.
   - Permissions: Use `sudo` for cp and systemctl.
   - Fatal enforcement: If errors occur, halt and report; no retries unless specified.

### Troubleshooting Updates
- If site doesn't update: Check Nginx root is `/var/www/hybrid/`
- Permission issues: Use `sudo` for file operations in `/var/www/`
- Caching: Restart Nginx (`sudo systemctl restart nginx`) or Tailscale (`sudo systemctl restart tailscaled`)

## Tailscale Funnel Management

### Enable Public Access

```bash
ssh jdd@100.115.115.21 "sudo tailscale funnel 80"
```

- Provides HTTPS at `https://raspberrypitailnet.tail85f090.ts.net/`
- Automatic Let's Encrypt certificates

### Check Status

```bash
ssh jdd@100.115.115.21 "tailscale serve status"
```

### Disable Funnel

```bash
ssh jdd@100.115.115.21 "sudo tailscale serve reset"
```

## Nginx Configuration

### Config Location
`/etc/nginx/sites-enabled/hybrid`

### Current Config

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

### Restart Nginx

```bash
ssh jdd@100.115.115.21 "sudo systemctl restart nginx"
```

## API Management

### Start API

```bash
ssh jdd@100.115.115.21 "cd /home/jdd/hybrid_api && python main.py"
```

(Run in background/screen/tmux)

### Check API Status

```bash
curl http://127.0.0.1:5001/health
```

## Nexus Agent (Log Monitoring)

### Start Agent

```bash
ssh jdd@100.115.115.21 "sudo systemctl start nexus-agent"
```

### Check Agent Status

```bash
ssh jdd@100.115.115.21 "sudo systemctl status nexus-agent"
```

### View Logs

```bash
ssh jdd@100.115.115.21 "tail -f /home/jdd/hybrid_api/apt_nexus_incidents.log"
```

### Agent Service Config
Located at `/etc/systemd/system/nexus-agent.service`

## Traffic Logging

### View Traffic Data

```bash
ssh jdd@100.115.115.21 "cat /home/jdd/hybrid_api/traffic_log.csv"
```

### Download Logs

Available at `/logs.html` on the site

## Tor Hidden Service

### Onion Address

`http://wmwejh36zcvsgmesq34nwdcmvef3rxfskfbw62sz4ppg3feb23moofad.onion`

### Tor Config Location

`/etc/tor/torrc` (HiddenServiceDir and HiddenServicePort)

### Restart Tor

```bash
ssh jdd@100.115.115.21 "sudo systemctl restart tor"
```

## Security Considerations

- All exceptions are fatal (strict_mode.py)
- Logs monitor for suspicious activity
- No hardcoded credentials
- Regular log rotation
- Access via Tailscale VPN for admin

## Backup and Recovery

- Backup `/var/www/hybrid/` and `/home/jdd/hybrid_api/`
- Tailscale config persists across restarts
- Tor keys are in `/var/lib/tor/hidden_service/`

## Future Enhancements

- Expand FFmpeg generator with more options (filters, audio processing)
- Improve APT tools with real pipeline execution
- Add more traffic-attracting utilities
- Enhance UI with animations and modern design
- Integrate with GitHub repos for live code examples

## Contact

For issues: Check logs, restart services, verify file paths.
Site maintainer: JD Dondlinger (APT Theorist & Carpenter)
