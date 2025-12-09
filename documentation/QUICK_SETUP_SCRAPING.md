# ⚡ Quick Setup: Commercial Scraping

## 🎯 Quick Start (3 Steps)

### **Bright Data Setup** (Pay-per-use, ~$0.001-0.01/request)

**1. Get Credentials**
- Sign up: https://brightdata.com
- Navigate to **Proxies & Scraping Infrastructure**
- Choose **Unlocker API**
- Get your **API Key** and **Zone Name**

**2. Create `.env` file in `backend/` folder:**
```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=your_api_key_here
BRIGHTDATA_PROXY_NAME=residential_proxy1
```

**3. Restart backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Or just use:**
```bash
start-backend.bat
```

---

## 📋 Configuration Reference

### Bright Data - Unlocker API (Recommended)
```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=brd_xxxxxxxxxxxxxxxxxxxxxxxxxx
BRIGHTDATA_ZONE=residential_proxy1
```

**Features:**
- ✅ Pay-per-success (~$0.001-0.01 per request)
- ✅ Automatic CAPTCHA solving
- ✅ JavaScript rendering
- ✅ 95%+ success rate
- ✅ No monthly minimums

### Bright Data - Traditional Proxy (Alternative)
```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_USERNAME=brd-customer-xxx-zone-residential_proxy1
BRIGHTDATA_PASSWORD=your_password
BRIGHTDATA_HOST=brd.superproxy.io
BRIGHTDATA_PORT=33335
```

---

## 🧪 Testing

### Method 1: Use Test Script
```bash
cd backend
python test_scraper.py https://www.ebay.com/itm/your-product-url
```

### Method 2: Check Backend Logs

**❌ Without Service:**
```
📡 No scraping service configured, using direct scraping
Failed to fetch Amazon page (Cloudflare protection)
```

**✅ With Bright Data:**
```
🔓 Using Bright Data Unlocker API for https://www.ebay.com/...
✅ Bright Data Unlocker API: Successfully fetched...
✅ Successfully scanned product: $1349.95
```

---

## 💰 Cost Estimation

### Example: 50 Products Tracked

**Assumptions:**
- 50 products × 24 scans/day = **1,200 requests/day**
- Monthly: **~36,000 requests**

**Bright Data Cost:**
- Low estimate: 36,000 × $0.001 = **$36/month** ✅
- High estimate: 36,000 × $0.01 = **$360/month**
- Typical: **~$50-100/month** for residential proxies

**Cost Reduction Tips:**
1. Use Datacenter proxies when possible ($0.60/GB vs $8.40/GB)
2. Reduce scan frequency (e.g., every 2 hours instead of hourly)
3. Only use service for protected sites (eBay, Amazon with CAPTCHA)

---

## 🔄 Switching Services

### Enable Bright Data
```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=your_key
BRIGHTDATA_PROXY_NAME=residential_proxy1
```

### Disable (Use Direct Scraping)
```env
SCRAPING_SERVICE=direct
```

Or simply comment out:
```env
# SCRAPING_SERVICE=brightdata
# BRIGHTDATA_API_KEY=...
# BRIGHTDATA_PROXY_NAME=...
```

**Remember to restart backend after changes!**

---

## 🚀 Best Practices

1. **Start with Free Trial**
   - Test before committing
   - Verify your scrapers work

2. **Use Service Selectively**
   - Enable only for sites that block you
   - Direct scraping is free!

3. **Monitor Costs**
   - Check Bright Data dashboard regularly
   - Set spending alerts

4. **Optimize Scan Frequency**
   - Hourly scans: High cost
   - Every 2-4 hours: Balanced
   - Once/twice daily: Low cost

---

## 📚 Full Documentation

For detailed setup and troubleshooting:
- **[SCRAPING_SERVICES_GUIDE.md](SCRAPING_SERVICES_GUIDE.md)** - Complete Bright Data guide

---

**🎉 You're ready to scrape any site!**
