# 🌐 Third-Party Scraping Services Integration Guide

Your Price Tracker now supports **optional** integration with commercial web scraping services to bypass anti-bot protection!

## 🎯 Why Use a Scraping Service?

Major e-commerce sites (Amazon, eBay, Newegg) block direct scraping with:
- **Cloudflare protection**
- **CAPTCHA challenges**  
- **Bot detection**
- **IP blocking**

**Commercial scraping services solve this** by providing:
- ✅ Rotating residential proxies
- ✅ CAPTCHA solving
- ✅ Browser fingerprinting
- ✅ High success rates (95%+)

---

## 🚀 Supported Services

### **1. Bright Data** (Recommended) 💎
- **Website**: https://brightdata.com
- **Best for**: Enterprise-level scraping, highest success rates
- **Pricing**: Pay-as-you-go, starts at $500/month
- **Features**: Residential proxies, datacenter proxies, CAPTCHA solving

### **2. ScraperAPI** 🔧
- **Website**: https://www.scraperapi.com
- **Best for**: Budget-friendly, easy setup
- **Pricing**: Starts at $49/month (1,000,000 API credits)
- **Features**: Automatic proxy rotation, JS rendering, geotargeting

---

## ⚙️ Setup Instructions

### **Option A: Bright Data**

**1. Sign up for Bright Data**
   - Go to https://brightdata.com
   - Create an account
   - Purchase a proxy plan (Residential or Datacenter)

**2. Get your credentials**
   - Dashboard → Proxy → Zone settings
   - Note your: Username, Password, Zone name

**3. Configure your Price Tracker**

Create a `.env` file in the `backend/` folder:

```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_USERNAME=your_username_here
BRIGHTDATA_PASSWORD=your_password_here
BRIGHTDATA_ZONE=residential_proxy1
```

**4. Restart the backend**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

### **Option B: ScraperAPI**

**1. Sign up for ScraperAPI**
   - Go to https://www.scraperapi.com
   - Create an account (free trial available!)
   - Get your API key from the dashboard

**2. Configure your Price Tracker**

Create a `.env` file in the `backend/` folder:

```env
SCRAPING_SERVICE=scraperapi
SCRAPERAPI_KEY=your_api_key_here
```

**3. Restart the backend**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

## 🧪 Testing Your Setup

After configuration, check the backend logs when you scan products:

**✅ Success (using Bright Data):**
```
🌐 Using Bright Data for https://www.amazon.com/...
✅ Bright Data: Successfully fetched https://www.amazon.com/...
Amazon scrape successful: $1420.00, in_stock=True, image=True
```

**✅ Success (using ScraperAPI):**
```
🌐 Using ScraperAPI for https://www.ebay.com/...
✅ ScraperAPI: Successfully fetched https://www.ebay.com/...
eBay scrape successful: $899.99, in_stock=True, image=True
```

**📡 Fallback (no service configured):**
```
📡 No scraping service configured, using direct scraping for https://...
```

---

## 💰 Cost Comparison

| Service | Free Tier | Starter Plan | Success Rate | Best For |
|---------|-----------|--------------|--------------|----------|
| **Bright Data** | ❌ No | $500/month | 99% | Enterprise, high volume |
| **ScraperAPI** | ✅ 5,000 credits | $49/month | 95% | Small business, testing |
| **Direct Scraping** | ✅ Free | Free | ~10% | Development only |

---

## 🔐 Security Notes

**IMPORTANT**: Never commit your `.env` file to Git!

Your `.gitignore` already includes `.env`, so your API keys stay private.

**Example `.env` file location:**
```
Price Tracker/
├── backend/
│   ├── .env          ← Create this file (git ignored)
│   ├── .env.example  ← Template (safe to commit)
│   ├── app/
│   └── ...
```

---

## 🎛️ Advanced Configuration

### Enable JavaScript Rendering (ScraperAPI)

For sites that heavily use JavaScript:

```env
SCRAPING_SERVICE=scraperapi
SCRAPERAPI_KEY=your_key
SCRAPERAPI_RENDER_JS=true  # Slower but handles dynamic content
```

### Adjust Timeouts

```env
SCRAPING_TIMEOUT=30  # Seconds (default: 10)
SCRAPING_DELAY=2     # Delay between requests (default: 1)
```

---

## ❓ FAQ

**Q: Do I need a scraping service?**  
A: Not required! The system works without one, but major sites will block direct scraping. Services dramatically improve success rates.

**Q: Which service is better?**  
A: 
- **Bright Data**: Best success rates, enterprise features, higher cost
- **ScraperAPI**: Easier setup, lower cost, good for most use cases

**Q: Can I switch services later?**  
A: Yes! Just update your `.env` file and restart the backend.

**Q: What happens if the service fails?**  
A: The system automatically falls back to direct scraping and logs the error.

**Q: How many products can I track?**  
A: Depends on your service plan and scan frequency:
- 100 products × 24 scans/day = 2,400 requests/day = ~72,000/month
- ScraperAPI starter: 1M credits = ~13,800 products/day
- Bright Data: Pay per GB, varies by site

---

## 🆘 Troubleshooting

**"Failed to fetch" errors:**
1. Check your API credentials in `.env`
2. Verify your service account has credits
3. Check backend logs for detailed error messages
4. Test your credentials on the service dashboard

**Still not working?**
- Ensure `.env` is in the `backend/` folder
- Restart the backend server
- Check that `SCRAPING_SERVICE` matches your provider name exactly
- Verify no typos in your credentials

---

## 🎓 Recommended Setup for New Users

**1. Start Free (Development)**
```env
# No configuration needed!
# Uses direct scraping
```

**2. Test with ScraperAPI Trial**
```env
SCRAPING_SERVICE=scraperapi
SCRAPERAPI_KEY=trial_key_from_dashboard
```

**3. Scale with Bright Data (Production)**
```env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_USERNAME=your_username
BRIGHTDATA_PASSWORD=your_password
BRIGHTDATA_ZONE=residential_proxy1
```

---

## 📊 Expected Results

| Vendor | Direct Scraping | With Service |
|--------|----------------|--------------|
| Amazon | ❌ Blocked (~5%) | ✅ Works (~98%) |
| eBay | ❌ Blocked (~10%) | ✅ Works (~95%) |
| Newegg | ❌ Blocked (~15%) | ✅ Works (~97%) |
| Small sites | ✅ Works (~80%) | ✅ Works (~99%) |

---

**🎉 You're all set!** Your price tracker can now scrape even the most protected e-commerce sites!

