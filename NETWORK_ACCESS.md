# Network Access Configuration

Guide for accessing your Price Tracker from other devices on your local network or through Tailscale VPN.

---

## 🏠 Local Network Access

By default, the Price Tracker is accessible from other devices on your local network.

### Backend (FastAPI)
✅ Already configured to listen on all network interfaces (`0.0.0.0`)

**Access from any device on your network:**
```
http://[pc-hostname]:8081
http://[pc-ip-address]:8081
```

Example: `http://geekom-gt1-a:8081` or `http://192.168.1.100:8081`

### Frontend (Vite/React)
✅ Configured to listen on all network interfaces (`0.0.0.0`)

**Access from any device on your network:**
```
http://[pc-hostname]:3000
http://[pc-ip-address]:3000
```

Example: `http://geekom-gt1-a:3000` or `http://192.168.1.100:3000`

---

## 🔒 Tailscale VPN Access

If you use Tailscale to access your network remotely, additional configuration is required.

### What is Tailscale?

Tailscale creates a secure VPN between your devices using WireGuard. It assigns hostnames like:
- `device-name.tailXXXXXX.ts.net`

### Configuration

The frontend is already configured to allow Tailscale access. In `frontend/vite.config.ts`:

```typescript
server: {
  host: '0.0.0.0',
  port: 3000,
  allowedHosts: [
    '.tail425a06.ts.net', // Allow Tailscale network
    'localhost',
  ],
  // ...
}
```

### Your Tailscale Network

If your Tailscale network ID is **different** from `tail425a06`, update the configuration:

1. **Find your Tailscale network ID:**
   - Open Tailscale on any device
   - Look at your device's full hostname: `device-name.tailXXXXXX.ts.net`
   - The `tailXXXXXX` part is your network ID

2. **Update `frontend/vite.config.ts`:**
   ```typescript
   allowedHosts: [
     '.tailYOURID.ts.net', // Replace with your network ID
     'localhost',
   ],
   ```

3. **Restart the frontend:**
   ```powershell
   user_tools\kill-all.bat
   user_tools\start-all.bat
   ```

### Access via Tailscale

Once configured, access from any device on your Tailscale network:

```
http://geekom-gt1-a.tail425a06.ts.net:3000
```

Replace with your actual hostname and Tailscale network ID.

---

## 🔧 Troubleshooting

### "Blocked request. This host is not allowed"

**Problem:** Vite is blocking the hostname for security reasons.

**Solution:** Add your hostname to `allowedHosts` in `frontend/vite.config.ts`:

```typescript
allowedHosts: [
  '.tail425a06.ts.net',  // Tailscale
  '.local',               // mDNS/Bonjour
  'localhost',
  // Add more as needed
],
```

### Cannot Access from Other Devices

**Check firewall settings:**

1. **Windows Firewall:** Allow ports 3000 and 8081
   ```powershell
   # Run as Administrator
   netsh advfirewall firewall add rule name="Price Tracker Frontend" dir=in action=allow protocol=TCP localport=3000
   netsh advfirewall firewall add rule name="Price Tracker Backend" dir=in action=allow protocol=TCP localport=8081
   ```

2. **Verify servers are listening:**
   ```powershell
   netstat -an | findstr "3000 8081"
   ```
   Should show `0.0.0.0:3000` and `0.0.0.0:8081`

### API Calls Failing from Remote Devices

**Problem:** Frontend on remote device can't reach backend API.

**Check:** The frontend proxies `/api` requests to `http://localhost:8081`, which works on the host machine but not from remote devices.

**Solution:** The frontend should use the same hostname for API calls. This is already handled by the proxy configuration.

---

## 🌐 Advanced: Custom Domain

If you want to use a custom domain (e.g., `prices.mynetwork.local`):

1. **Set up DNS/hosts entry** pointing to your server

2. **Add domain to allowedHosts:**
   ```typescript
   allowedHosts: [
     'prices.mynetwork.local',
     '.tail425a06.ts.net',
     'localhost',
   ],
   ```

3. **Update CORS if needed** (backend in `backend/app/main.py`):
   ```python
   origins = [
       "http://localhost:3000",
       "http://prices.mynetwork.local:3000",
   ]
   ```

---

## 📱 Mobile Access

Access your Price Tracker from mobile devices:

1. **Same WiFi network:** Use local network access
   - Open browser on phone
   - Navigate to `http://[pc-hostname]:3000`

2. **Via Tailscale:**
   - Install Tailscale app on mobile
   - Connect to your network
   - Navigate to `http://[pc-hostname].tailXXXXXX.ts.net:3000`

---

## 🔐 Security Considerations

### Development Mode Warning

⚠️ The current setup uses Vite's **development server** which is:
- NOT optimized for production
- NOT hardened for security
- Meant for **trusted networks only**

### Recommendations

1. **Only expose on trusted networks** (home network, VPN)
2. **Don't expose directly to the internet**
3. **Use Tailscale or similar VPN** for remote access
4. **Consider authentication** if sharing with multiple users
5. **For production deployment**, build and serve with proper web server (nginx, Apache)

### Firewall Best Practices

```powershell
# Windows: Only allow from private networks
netsh advfirewall firewall add rule name="Price Tracker" dir=in action=allow protocol=TCP localport=3000,8081 profile=private
```

---

## 🚀 Quick Reference

| Access Method | URL Format | Configuration |
|--------------|------------|---------------|
| **Local (same PC)** | `http://localhost:3000` | ✅ Works by default |
| **Local Network** | `http://[hostname]:3000` | ✅ Already configured |
| **Local IP** | `http://192.168.1.x:3000` | ✅ Already configured |
| **Tailscale** | `http://host.tailXXX.ts.net:3000` | ✅ Configured for tail425a06 |
| **Custom Domain** | `http://custom.domain:3000` | ⚙️ Requires setup |

---

**Related Documentation:**
- [README.md](README.md) - Main documentation
- [QUICK_START.md](QUICK_START.md) - Setup guide
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - Configuration options

