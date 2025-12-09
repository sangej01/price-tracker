# Price Tracker - Quick User Guide

## 🎯 New Features You Can Use NOW!

### 1. See Which Scraper is Used 🔧

**Where:** Product Detail Page

**What you'll see:**
```
Product Name
🔧 Using: AmazonScraper [Optimized]
```

**What it means:**
- **AmazonScraper/EbayScraper/NeweggScraper** + [Optimized] = ✅ Great accuracy!
- **GenericScraper** + [Generic] = ⚠️ May be less accurate

---

### 2. Test URLs Before Adding 🧪

**Where:** Add Product Modal → URL field

**How to use:**
1. Click "Add Product"
2. Enter product URL
3. Click "Test URL" (appears next to URL field)
4. See results in blue panel:
   - Which scraper will be used
   - Price found (if successful)
   - Stock status
   - Quality indicator

**When to use:**
- Before adding new products
- To verify price can be extracted
- To check if you need vendor-specific scraper

---

### 3. Manual Scanning 🔄

**Two Ways:**

**Dashboard** → "Scan All Products" button
- Scans all products
- Shows "Scanning..." with spinner
- Updates all prices

**Product Detail** → "Scan Now" button  
- Scans single product
- Shows "Scanning..." with spinner
- Updates price immediately

---

## 📋 Quick Workflows

### Adding Your First Product

```
1. Click "Vendors" → "Add Vendor"
   Example: Name="Amazon", Domain="amazon.com"

2. Click "Products" → "Add Product"
   - Name: "Product Name"
   - URL: Full product URL
   - Click "Test URL" to verify ✨ NEW!
   - Select vendor
   - Click "Create"

3. Go to Dashboard → "Scan All Products"
   Wait a few seconds

4. Refresh → See price!
```

### Checking Price History

```
1. Dashboard → Click product card "View Details"

2. See on product page:
   - 🔧 Scraper type ✨ NEW!
   - Current/Lowest/Highest/Average prices
   - Price history chart
   - Time range buttons (7/14/30/90 days)

3. Click "Scan Now" to update
```

### Understanding Scraper Quality

```
[Optimized] Badge = Green
├─ Vendor-specific scraper
├─ 90%+ accuracy
├─ Multi-currency support
└─ Best choice!

[Generic] Badge = Yellow
├─ Fallback scraper
├─ 50-70% accuracy
├─ Works, but may miss prices
└─ Consider finding different URL
```

---

## 🎨 Visual Guide

### Dashboard Layout
```
┌───────────────────────────────────────┐
│ Dashboard        [Scan All Products]  │ ← Scan everything
├───────────────────────────────────────┤
│ [Stat Cards: Products, Vendors, etc.] │
├───────────────────────────────────────┤
│ Tracked Products:                     │
│ ┌─────┐ ┌─────┐ ┌─────┐              │
│ │ $99 │ │ $49 │ │ N/A │ ← Products   │
│ └─────┘ └─────┘ └─────┘              │
└───────────────────────────────────────┘
```

### Product Detail
```
┌───────────────────────────────────────┐
│ [← Back]              [Scan Now]      │ ← Scan this one
├───────────────────────────────────────┤
│ Product Name                          │
│ 🔧 Using: AmazonScraper [Optimized]  │ ← NEW!
├───────────────────────────────────────┤
│ Current: $299  Lowest: $249  High:$349│
│                                       │
│ [Price History Chart] ────────────    │
└───────────────────────────────────────┘
```

### Add Product with Tester
```
┌───────────────────────────────────────┐
│ Add New Product                       │
│                                       │
│ Name: [____________]                  │
│ URL:  [____________] [Test URL] ← NEW!│
│                                       │
│ ┌──────────────────────────────────┐ │
│ │ 🧪 Test URL Scraper         [×] │ │ ← NEW Panel
│ │                                  │ │
│ │ ✓ Scraping Successful!           │ │
│ │   Scraper: AmazonScraper         │ │
│ │   [Optimized Scraper]            │ │
│ │   Price: USD $299.99             │ │
│ └──────────────────────────────────┘ │
│                                       │
│ [Cancel]              [Create]        │
└───────────────────────────────────────┘
```

---

## ⚡ Quick Tips

### ✅ Do This
- ✅ Test URLs before adding
- ✅ Use optimized scrapers when possible
- ✅ Set reasonable scan frequencies (60+ minutes)
- ✅ Check scraper type on detail page
- ✅ Monitor "Recently Scanned" stat

### ❌ Avoid This
- ❌ Adding products without testing
- ❌ Very frequent scans (< 30 min)
- ❌ Ignoring generic scraper warnings
- ❌ Adding broken/invalid URLs

---

## 🔍 Troubleshooting

### "Price Not Found"
**Try:**
1. Check URL is correct and not expired
2. Test URL before adding
3. Try different product page from same site
4. Check if generic scraper (may need custom scraper)

### "Scraper Shows Generic"
**Means:**
- No vendor-specific scraper available
- May work, but less accurate
- Consider requesting custom scraper

**Solutions:**
- Try different site with optimized scraper
- Test URL to verify it works
- Accept lower accuracy for that site

### "Scan Fails"
**Possible reasons:**
- Website blocking scraper
- Product page changed
- Invalid URL
- Network issue

**Solutions:**
1. Test URL manually
2. Try "Scan Now" again
3. Update product URL
4. Check if site requires JavaScript (advanced)

---

## 📊 Understanding Stats

### Dashboard Stats
- **Total Products** - Products you're tracking
- **Total Vendors** - Vendors you've added
- **Recently Scanned** - Scanned in last 24 hours
- **Price Records** - Total price history entries

### Product Stats
- **Current Price** - Most recent scan
- **Lowest Price** - Best deal found
- **Highest Price** - Peak price seen
- **Average Price** - Mean over time period

---

## 🎯 Best Practices

### For Accurate Tracking
1. Use vendor-specific scrapers (Optimized badge)
2. Test URLs before adding
3. Set scan frequency based on price change frequency
4. Monitor success via "Recently Scanned"

### For Best Results
1. Add multiple products from optimized sites (Amazon, eBay, Newegg)
2. Check price history regularly
3. Use manual scan before making purchase decisions
4. Keep product URLs up to date

### For System Health
1. Don't scan too frequently (< 30 min)
2. Remove inactive products
3. Update broken URLs promptly
4. Use reasonable scan frequencies

---

## 🚀 Pro Tips

### Tip 1: Test First, Add Second
Always test URLs before adding products. Saves time and ensures tracking works!

### Tip 2: Check the Badge
Green "Optimized" = High confidence  
Yellow "Generic" = Verify with test

### Tip 3: Smart Scan Frequencies
- Electronics (slow price changes): 120+ minutes
- Deals/Flash sales (fast changes): 30-60 minutes
- Regular products: 60 minutes (default)

### Tip 4: Use Manual Scans
Before making purchase: Manual scan for latest price!

### Tip 5: Monitor Your Stats
Dashboard shows "Recently Scanned" - should equal your active products!

---

## 🎓 Learning More

### Full Documentation
- **README.md** - Complete system documentation
- **CUSTOM_SCRAPERS_GUIDE.md** - For developers
- **DEMO_SUMMARY.md** - Visual feature guide
- **FRONTEND_SCRAPER_INTEGRATION.md** - Technical details

### Need Help?
1. Check troubleshooting section above
2. Refer to full documentation
3. Test URLs to diagnose issues
4. Check scraper type on detail pages

---

## ⌨️ Keyboard Shortcuts

Currently manual navigation only. Future versions may include:
- `Ctrl/Cmd + S` - Scan all
- `R` - Refresh dashboard
- `Esc` - Close modals

---

## 📱 Mobile Tips

All features work on mobile:
- Touch-friendly buttons
- Responsive tables
- Scrollable charts
- Tap to expand details

---

**That's it! You're ready to track prices like a pro! 🎉**

**Key Takeaways:**
- ✅ Always test URLs before adding
- ✅ Check scraper type (Optimized > Generic)
- ✅ Use manual scans before purchases
- ✅ Monitor your dashboard stats

**Happy Price Tracking! 💰**

