# 🌐 Bright Data Integration Guide

Your Price Tracker supports **optional** integration with Bright Data to bypass anti-bot protection on protected websites!

## 🎯 Why Use Bright Data?

Major e-commerce sites (Amazon, eBay, Newegg) block direct scraping with:
- **Cloudflare protection**
- **CAPTCHA challenges**  
- **Bot detection**
- **IP blocking**

**Bright Data solves this** by providing:
- ✅ Rotating residential proxies
- ✅ Automatic CAPTCHA solving
- ✅ Browser fingerprinting
- ✅ High success rates (95%+)
- ✅ JavaScript rendering
- ✅ Pay-per-success pricing

---

## 💰 Pricing

### Unlocker API (Recommended)
- **Pay-as-you-go**: ~$0.001 - $0.01 per successful request
- **No monthly minimums** for low volume
- **Free trial credits** available
- **Perfect for**: Price monitoring (low frequency scans)

### Datacenter Proxies
- **$0.60 per GB**
- **Good for**: Basic scraping, less expensive
- **May be blocked** by some protected sites

### Residential Proxies
- **$8.40 per GB**
- **Best for**: Highly protected sites
- **95%+ success rate** guaranteed

**Website**: https://brightdata.com

---

## ⚙️ Setup Instructions

### Step 1: Create Bright Data Account

1. Go to https://brightdata.com
2. Sign up for an account
3. Navigate to **Proxies & Scraping Infrastructure**

### Step 2: Choose Unlocker API

1. Click **Get Proxies** → **Unlocker**
2. Select **API** method (not Web Scraper IDE)
3. Choose your proxy type:
   - **Datacenter** (cheaper, may be blocked occasionally)
   - **Residential** (more expensive, higher success rate)
4. Select **Shared (Pay per GB)** for low volume

### Step 3: Get Your Credentials

After setup, you'll receive:
- **API Key** (long string starting with `brd_`)
- **Zone Name** (e.g., `residential_proxy1`, `datacenter_proxy1`)
- **Host**: `brd.superproxy.io`
- **Port**: (e.g., `33335`)

### Step 4: Configure Price Tracker

Add to your root `.env` file (project root):

```env
# Enable Bright Data
SCRAPING_SERVICE=brightdata

# Unlocker API credentials
BRIGHTDATA_API_KEY=brd_xxxxxxxxxxxxxxxxxxxxxxxxxx
BRIGHTDATA_PROXY_NAME=residential_proxy1
```

**Note:** You don't need username, password, host, or port for Unlocker API - just API key and zone!

### Step 5: Restart Backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Or simply use:
```bash
start-backend.bat
```

---

## 🧪 Testing Your Setup

### Check Backend Logs

When scanning products, you should see:

**✅ Success:**
```
🔓 Using Bright Data Unlocker API for https://www.ebay.com/itm/...
✅ Bright Data Unlocker API: Successfully fetched https://www.ebay.com/itm/...
✅ Successfully scanned New NVIDIA RTX 4000 SFF Ada 20GB: $1349.95
```

**❌ Configuration Error:**
```
⚠️ Bright Data not configured, falling back to direct scraping
```

### Use the Test Tool

```bash
cd backend
python test_scraper.py https://www.ebay.com/itm/your-product-url
```

Expected output:
```
🔓 Using Bright Data Unlocker API for https://www.ebay.com/itm/...
✅ Bright Data Unlocker API: Successfully fetched
----------------------------------------
Price: $1349.95
In Stock: False
Currency: USD
Image URL: https://i.ebayimg.com/...
```

---

## 📊 How It Works

### Without Bright Data (Direct Scraping)
```
Your App → Target Website
           ↓
        ❌ Blocked by Cloudflare/CAPTCHA
```

### With Bright Data
```
Your App → Bright Data API → Real Browser → Target Website
           ↓
        ✅ Returns clean HTML
```

Bright Data:
1. Routes request through residential IP
2. Renders JavaScript if needed
3. Solves CAPTCHAs automatically
4. Returns clean HTML to your scraper
5. You only pay if successful!

---

## 🔧 Advanced Configuration

### Alternative: Traditional Proxy Method

If you prefer using proxy credentials instead of API:

```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_USERNAME=brd-customer-xxx-zone-residential_proxy1
BRIGHTDATA_PASSWORD=your_password_here
BRIGHTDATA_HOST=brd.superproxy.io
BRIGHTDATA_PORT=33335
```

**Note:** Unlocker API is simpler and recommended!

### Timeout Settings

Adjust scraping timeout (default: 10 seconds):

```env
SCRAPING_TIMEOUT=30
```

---

## 💡 Usage Tips

### 1. **Start with Free Trial**
   - Bright Data offers free trial credits
   - Test with a few products before committing

### 2. **Choose Right Proxy Type**
   - **Datacenter**: Try first, cheaper ($0.60/GB)
   - **Residential**: Use if datacenter gets blocked ($8.40/GB)

### 3. **Monitor Costs**
   - Each successful request: ~$0.001 - $0.01
   - Scanning 100 products: ~$0.10 - $1.00
   - Daily scans (4 products, 4x/day): ~$0.05/day = $1.50/month

### 4. **Scan Frequency**
   - Lower frequency = lower costs
   - Set scan frequency to 60-120 minutes for most products
   - Use manual scans when needed

---

## 🐛 Troubleshooting

### Issue: "Bright Data not configured"

**Check:**
1. Root `.env` file exists (project root)
2. `SCRAPING_SERVICE=brightdata` is set
3. Both `BRIGHTDATA_API_KEY` and `BRIGHTDATA_PROXY_NAME` are set
4. No typos in variable names
5. Backend was restarted after creating `.env`

### Issue: HTTP 400 "zone is required"

**Solution:** Ensure `BRIGHTDATA_PROXY_NAME` is set in `.env`
```env
BRIGHTDATA_PROXY_NAME=residential_proxy1
```

### Issue: HTTP 401 "Unauthorized"

**Solution:** Check your API key
- API key should start with `brd_`
- Copy from Bright Data dashboard
- No extra spaces or quotes

### Issue: HTTP 407 "Proxy Authentication Required"

**Solution:** You're mixing proxy method with API method
- Remove `BRIGHTDATA_USERNAME`, `PASSWORD`, `HOST`, `PORT`
- Keep only `BRIGHTDATA_API_KEY` and `BRIGHTDATA_PROXY_NAME`

### Issue: Still getting blocked

**Solution:** Upgrade to Residential proxies
```env
# Change zone from datacenter to residential
BRIGHTDATA_ZONE=residential_proxy1
```

---

## 📈 Cost Examples

### Low Volume (Hobby)
- **Products**: 5
- **Scans per day**: 24 (every hour)
- **Cost**: ~$0.12 - $1.20/day = $3.60 - $36/month

### Medium Volume (Small Business)
- **Products**: 50
- **Scans per day**: 96 (every 15 min)
- **Cost**: ~$0.48 - $4.80/day = $14.40 - $144/month

### High Volume (Enterprise)
- **Products**: 500
- **Scans per day**: 2,000
- **Cost**: ~$2 - $20/day = $60 - $600/month

**Remember:** You only pay for successful requests!

---

## 🔄 Switching Back to Direct Scraping

To disable Bright Data and use direct scraping:

```env
# Comment out or remove these lines
# SCRAPING_SERVICE=brightdata
# BRIGHTDATA_API_KEY=...
# BRIGHTDATA_PROXY_NAME=...
```

Or set to direct:
```env
SCRAPING_SERVICE=direct
```

Restart backend and your scrapers will use direct HTTP requests.

---

## 🆚 When to Use Bright Data

| Scenario | Use Bright Data? |
|----------|------------------|
| Testing new scrapers | ❌ No, try direct first |
| Amazon blocked you | ✅ Yes |
| eBay showing CAPTCHA | ✅ Yes |
| Newegg working fine | ❌ No, direct is cheaper |
| High-value products | ✅ Yes, ensure data |
| Low-frequency scans | ✅ Yes, very affordable |

---

## 📞 Support

- **Bright Data Docs**: https://docs.brightdata.com/
- **API Reference**: https://docs.brightdata.com/api-reference
- **Support**: support@brightdata.com
- **Price Tracker Issues**: See main [README](../README.md)

---

**🎉 Happy scraping with Bright Data!**

*Now you can track prices on any website, no matter how protected!*
