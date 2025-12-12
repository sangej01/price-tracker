# ⚡ Quick Start Guide

Get your Price Tracker running in minutes!

---

## 🚀 Fastest Way (Windows)

**Double-click `user_tools\start-all.bat`** in File Explorer - Done! ✨

This automatically:
1. ✅ Installs backend dependencies (with pipenv)
2. ✅ Installs frontend dependencies (with npm)
3. ✅ Starts both servers

**To restart fresh:**
1. Run `user_tools\kill-all.bat` - Stops all Python and Node.js processes
2. Run `user_tools\start-all.bat` - Starts everything fresh

---

## 🛠️ Manual Setup

### Prerequisites
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **pipenv** (install: `pip install pipenv`)

### Option 1: Individual Scripts

**Start Backend:**
```powershell
# Double-click or run:
user_tools\start-backend.bat
```

**Start Frontend:**
```powershell
# Double-click or run:
user_tools\start-frontend.bat
```

### Option 2: Command Line

**Backend:**
```bash
cd .
# Use backend/Pipfile while running from the project root:
# PowerShell:
#   $env:PIPENV_PIPFILE="backend/Pipfile"
# CMD:
#   set PIPENV_PIPFILE=backend\\Pipfile
pipenv sync || pipenv install  # Install dependencies (backend Pipfile)
cd backend
pipenv run python run.py       # Start server (port 8081)
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Access Your Application

Once started, open your browser:

| Service | URL | Description |
|---------|-----|-------------|
| **Dashboard** | http://localhost:3001 | Main application UI |
| **Backend API** | http://localhost:8081 | REST API server |
| **API Docs** | http://localhost:8081/docs | Interactive API documentation |

## 📝 First-Time Setup

### 1️⃣ Add a Vendor

Navigate to **Vendors** → **Add Vendor**

**Example:**
- Name: `Amazon`
- Domain: `amazon.com`

Repeat for other vendors (eBay, Newegg, etc.)

### 2️⃣ Add a Product

Navigate to **Products** → **Add Product**

**Example:**
- Name: `NVIDIA RTX 4090`
- URL: `https://www.amazon.com/dp/B0BHH3DCSG`
- Vendor: `Amazon`
- Scan Frequency: `60` minutes

💡 **Pro Tip:** Click **"Test URL"** before saving to verify scraping works!

### 3️⃣ Start Tracking

1. Go to **Dashboard**
2. Click **"Scan All Products"**
3. Wait a few seconds
4. Refresh to see prices and charts! 📊

---

## 🌐 Optional: Commercial Scraping Setup

For protected sites (Amazon with CAPTCHA, eBay auctions), use commercial services:

### Bright Data (Pay-Per-Use)
```bash
# Add to your root .env file (project root)
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=your_api_key
BRIGHTDATA_PROXY_NAME=residential_proxy1
```

**Cost:** ~$0.001-0.01 per successful request

**Setup Guide:** [documentation/SCRAPING_SERVICES_GUIDE.md](documentation/SCRAPING_SERVICES_GUIDE.md)

---

## 💡 Usage Tips

- ✅ **Automatic scanning** runs every 15 minutes
- ✅ Each product scans at its own frequency
- ✅ Manual scans available on Dashboard or product pages
- ✅ Price history shows last 30 days by default
- ✅ Stock status updates with each scan
- ✅ Images auto-populate from product pages

---

## 🐛 Troubleshooting

### Need to Restart Servers

**Quick restart:**
```bash
# Stop all processes
user_tools\kill-all.bat

# Start fresh
user_tools\start-all.bat
```

### Port Already in Use

**Backend (port 8081):**
```bash
# Edit start-backend.bat or use different port:
uvicorn app.main:app --reload --port 8082
```

**Frontend (port 3001):**
```bash
# Edit frontend/vite.config.ts
server: { port: 3001 }
```

### Access from another device (LAN / Tailscale)
- **Backend**: must bind to **`0.0.0.0`** to be reachable remotely (binding to **`127.0.0.1`** is localhost-only).
- **Frontend (Vite)**: must bind to **`0.0.0.0`** and allow non-local hostnames.
  - This repo does that in `frontend/vite.config.ts` and `user_tools/start-frontend.bat`.

### Scraping Not Working

**Symptoms:**
- "Failed to fetch page"
- "Price not available"

**Solutions:**
1. ✅ Use **"Test URL"** feature to validate URLs
2. ✅ Try different product URLs
3. ✅ Enable commercial scraping ([guide](documentation/SCRAPING_SERVICES_GUIDE.md))
4. ✅ Check if website changed (update scraper selectors)

### Dependencies Won't Install

**Python:**
```bash
# Update pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Node.js:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database Issues

**Reset database:**
```bash
cd backend
rm price_tracker.db
# Restart backend - database recreates automatically
```

---

## 📚 Next Steps

- 📖 **User Guide:** [documentation/QUICK_USER_GUIDE.md](documentation/QUICK_USER_GUIDE.md)
- 🛠️ **Add Custom Scrapers:** [documentation/CUSTOM_SCRAPERS_GUIDE.md](documentation/CUSTOM_SCRAPERS_GUIDE.md)
- 🌐 **Setup Commercial APIs:** [documentation/SCRAPING_SERVICES_GUIDE.md](documentation/SCRAPING_SERVICES_GUIDE.md)
- 🏗️ **Architecture Overview:** [documentation/PROJECT_OVERVIEW.md](documentation/PROJECT_OVERVIEW.md)

---

## 📞 Need Help?

- 📚 Check [documentation/](documentation/) folder
- 🐛 Review error logs in terminal
- 📖 Visit http://localhost:8081/docs for API reference

---

**Happy Price Tracking! 🛒📉**
