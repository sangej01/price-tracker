# ⚡ Quick Setup: Commercial Scraping Services

## 🎯 Quick Start (3 Steps)

### **Option 1: ScraperAPI** (Easiest, $49/month)

**1. Get API Key**
- Sign up: https://www.scraperapi.com
- Free trial available!
- Copy your API key from dashboard

**2. Create `.env` file in `backend/` folder:**
```env
SCRAPING_SERVICE=scraperapi
SCRAPERAPI_KEY=paste_your_key_here
```

**3. Restart backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**✅ Done!** Amazon, eBay, Newegg will now work!

---

### **Option 2: Bright Data** (Enterprise, $500/month)

**1. Get Credentials**
- Sign up: https://brightdata.com
- Dashboard → Proxy → Zone settings
- Note: Username, Password, Zone name

**2. Create `.env` file in `backend/` folder:**
```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_USERNAME=your_username
BRIGHTDATA_PASSWORD=your_password
BRIGHTDATA_ZONE=residential_proxy1
```

**3. Restart backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**✅ Done!** 99% success rate on all sites!

---

## 🆓 No Service (Free - Limited)

**Don't create a `.env` file** - direct scraping is the default!

**Works on:**
- ✅ Small e-commerce sites
- ✅ Sites without bot protection
- ❌ Amazon (~5% success)
- ❌ eBay (~10% success)  
- ❌ Newegg (~15% success)

---

## 🧪 Test Your Setup

Run a scan and check the logs:

**✅ With Service:**
```
🌐 Using ScraperAPI for https://www.amazon.com/...
✅ ScraperAPI: Successfully fetched...
Amazon scrape successful: $1420.00
```

**📡 Without Service:**
```
📡 No scraping service configured, using direct scraping
Failed to fetch Amazon page
```

---

## 💰 Cost Calculator

**Example: Track 50 products, scan every hour**
- 50 products × 24 scans/day = **1,200 requests/day**
- Monthly: **~36,000 requests**

**ScraperAPI**: $49/month includes 1M credits ✅  
**Bright Data**: Pay per GB, ~$50-100/month ✅

---

## 🔐 Security

**✅ Safe:** `.env` is already in `.gitignore`  
**❌ Never:** Commit API keys to Git  
**✅ Check:** `.env` file is in `backend/` folder  

---

**Full Guide:** See `SCRAPING_SERVICES_GUIDE.md`  
**Need Help?** Check backend logs for detailed errors

