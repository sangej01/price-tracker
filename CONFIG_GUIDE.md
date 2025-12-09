# 🔧 Configuration Guide

## Central Configuration System

All application settings are centralized in **`config.py`** at the root level.

---

## 📂 File Structure

```
Price Tracker/
├── config.py              ← EDIT THIS! (Central config)
├── apply_config.py        ← Run this after editing config.py
├── backend/
│   ├── .env              ← Auto-generated (don't edit directly)
│   └── .env.example      ← Template
└── frontend/
    ├── .env              ← Auto-generated (don't edit directly)
    └── .env.example      ← Template
```

---

## ⚙️ How to Configure

### Step 1: Edit `config.py`

Open `config.py` and modify the settings:

```python
class BackendConfig:
    HOST = "0.0.0.0"          # Server host
    PORT = 8081               # ← Change port here!
    
    SCRAPING_SERVICE = "brightdata"    # Enable Bright Data
    BRIGHTDATA_API_KEY = "your_key"    # Your API key
    BRIGHTDATA_ZONE = "residential_proxy1"
```

### Step 2: Apply Configuration

```bash
python apply_config.py
```

This generates `backend/.env` and `frontend/.env` from your `config.py` settings.

### Step 3: Restart Servers

```bash
# Stop current servers (Ctrl+C), then:
start-all.bat
```

---

## 📝 Configuration Sections

### Backend Configuration

```python
class BackendConfig:
    # Server
    HOST = "0.0.0.0"              # Listen on all interfaces
    PORT = 8081                    # API server port
    DEBUG = False                  # Enable debug logging
    
    # Database
    DATABASE_URL = "sqlite:///./backend/price_tracker.db"
    
    # Scheduler
    SCAN_INTERVAL_MINUTES = 15     # How often to check for scans
    
    # Scraping
    SCRAPING_DELAY = 1.0           # Seconds between requests
    SCRAPING_TIMEOUT = 10          # Request timeout
    
    # Commercial Scraping
    SCRAPING_SERVICE = "direct"    # "direct" or "brightdata"
    BRIGHTDATA_API_KEY = ""        # Your Bright Data key
    BRIGHTDATA_PROXY_NAME = ""     # Your proxy name
```

### Frontend Configuration

```python
class FrontendConfig:
    # Automatically uses BackendConfig.PORT
    API_BASE_URL = f"http://localhost:{BackendConfig.PORT}"
    
    DEV_PORT = 3000               # Frontend dev server port
    PRODUCTS_PER_PAGE = 20        # UI pagination
    CHART_DAYS = 30              # Price history days
    AUTO_REFRESH_SECONDS = 300    # Dashboard refresh
```

---

## 🎯 Common Configuration Tasks

### Change Backend Port

```python
# config.py
class BackendConfig:
    PORT = 9000  # ← Change this
```

Run `python apply_config.py`, restart servers. Frontend automatically connects!

### Enable Bright Data

```python
# config.py
class BackendConfig:
    SCRAPING_SERVICE = "brightdata"
    BRIGHTDATA_API_KEY = "brd_xxxxx..."
    BRIGHTDATA_PROXY_NAME = "residential_proxy1"
```

### Change Scan Frequency

```python
# config.py
class BackendConfig:
    SCAN_INTERVAL_MINUTES = 30  # Check every 30 minutes
```

---

## 🔍 View Current Configuration

```bash
python config.py
```

Shows current settings without applying them.

---

## 📋 Manual .env Editing (Advanced)

If you prefer, edit `.env` files directly:

**backend/.env:**
```env
SERVER_PORT=8081
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=your_key
```

**frontend/.env:**
```env
VITE_API_BASE_URL=http://localhost:8081
```

**Note:** Manual changes are overwritten when you run `apply_config.py`!

---

## 🔄 Configuration Priority

1. **Environment variables** (highest priority)
2. **`.env` files**
3. **Defaults in `backend/app/config.py`**

---

## 💡 Best Practices

1. ✅ **Use `config.py`** for all changes
2. ✅ **Run `apply_config.py`** after editing
3. ✅ **Commit `config.py`** to version control
4. ❌ **Don't commit `.env`** files (they contain secrets)
5. ✅ **Use `.env.example`** to show what's needed

---

## 🔒 Security

- `.env` files are in `.gitignore` (won't be committed)
- Never hardcode API keys in `config.py` if sharing publicly
- Use environment variables for production:

```bash
# Production
export SERVER_PORT=8081
export BRIGHTDATA_API_KEY=real_key_here
```

---

**Questions?** See [README.md](README.md) or [QUICK_START.md](QUICK_START.md)

