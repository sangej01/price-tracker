# 🎯 Feature Highlights

## Recently Added (December 2025)

### 🔨 eBay Auction Tracking
**Status:** ✅ Complete

Track live eBay auctions with comprehensive bidding information:

- **Automatic Detection:** Distinguishes auctions from Buy It Now listings
- **Bid Monitoring:** Shows current bid count and price
- **Time Remaining:** Displays auction end date/time in your local timezone  
- **Buy It Now Price:** Shows both auction bid and BIN price when available
- **Historical Tracking:** Chart displays bid progression over time
- **Smart Cost Optimization:** Uses paid scraping only for first scan to get end time, then switches to free scraping

**Cost Savings:** ~$0.0015 one-time per auction, then FREE forever after!

**Settings:** Recommended scan frequency 5-15 minutes for active auctions

---

### 💱 Multi-Currency Support
**Status:** ✅ Complete

Full support for tracking products in different currencies:

- **Currency Symbol Detection:** Automatically identifies $ € £ ¥ and more
- **Price Change Display:** Shows correct currency symbol in price deltas
- **Currency Formatting:** Uses `Intl.NumberFormat` for proper display
- **Per-Product Currency:** Each product tracks its own currency independently

**Supported Currencies:** USD, EUR, GBP, JPY, CAD, AUD, and all standard ISO codes

---

### ⚙️ Per-Vendor Scan Frequencies
**Status:** ✅ Complete

Flexible scanning control with vendor-level defaults:

- **Vendor Defaults:** Set scan frequency per vendor (e.g., eBay: 15 min, Amazon: 60 min)
- **Product Overrides:** Individual products can override vendor default
- **Settings Page:** Centralized UI to manage all frequencies at once
- **Bulk Updates:** Apply vendor frequency to all existing products with one click
- **Quick Edit:** Change product frequency directly from dashboard cards

**Use Case:** Monitor fast-changing eBay auctions every 15 minutes while checking stable Amazon prices hourly

---

### 🛠️ Developer Experience Improvements

#### Pipenv Migration
**Status:** ✅ Complete

Switched from `venv` to `pipenv` for better dependency management:

- **Consistent Python Version:** Locked to Python 3.11
- **Deterministic Builds:** `Pipfile.lock` ensures reproducible environments
- **Simplified Commands:** `pipenv run` instead of activating venvs
- **Developer Preference:** Documented in `.cursor/rules/dev-preferences.mdc`

**Migration:** Automatic via `start-backend.bat` - no manual setup needed!

---

#### Enhanced Products Table
**Status:** ✅ Complete

Major UX improvements to product management:

- **Sortable Columns:** Click headers to sort by ID, Name, Vendor, or Frequency
- **Filter Panel:** Filter by Status (Active/Inactive) and Type (Auction/Regular)
- **ID Column:** First column shows product ID for easy reference
- **Type Column:** Visual badge shows 🔨 Auction or Regular
- **Product Counter:** Shows "X of Y products" when filters active
- **Responsive UI:** Hover effects and visual sort indicators

**Benefit:** Easily manage large product catalogs with hundreds of items

---

### 🏗️ Technical Improvements

#### Cost-Optimized Scraping
**Status:** ✅ Complete

Smart scraping strategy minimizes API costs:

- **Free-First:** Always tries direct scraping before paid services
- **Selective Paid:** Uses Bright Data only when necessary (blocked sites)
- **One-Time Auction Scan:** Fetches static auction data once, then uses free scraping
- **Estimated Savings:** 75%+ compared to always using paid services

**Example:** 4 products @ hourly = ~$14/month instead of $60/month

---

#### Database Migrations
**Status:** ✅ Complete

Proper database change management:

- **Migration Scripts:** Located in `backend/migrations/`
- **Version Control:** Each schema change has a dedicated script
- **Instructions Included:** Clear steps for applying migrations
- **Rollback Info:** Documentation includes how to reverse changes

**Current Migrations:**
- `add_auction_fields.py` - Added eBay auction tracking columns

---

#### Utility Scripts
**Status:** ✅ Complete

Helpful development tools:

- **`reset_ebay_product.py`:** Delete and recreate eBay products for testing
- **`check_auction_status.py`:** View auction data in database
- **`clean_price_data.py`:** Remove erroneous price history
- **`.bat` scripts:** One-click server management on Windows

**Location:** `backend/` for Python scripts, `user_tools/` for user-facing tools

---

## Upcoming Features

### 📧 Price Drop Alerts
**Status:** 🚧 Planned

- Email notifications when price drops below threshold
- SMS alerts via Twilio integration
- Configurable alert frequency to avoid spam

### 📊 Export Functionality
**Status:** 🚧 Planned

- Export price history to CSV/Excel
- Generate PDF reports with charts
- Scheduled email reports (weekly/monthly summaries)

### 🤖 Price Prediction
**Status:** 💡 Idea

- ML model to predict future price trends
- "Best time to buy" recommendations
- Historical pattern analysis

---

## Feature Requests

Have an idea? Open an issue on GitHub with the `feature-request` label!

**Priority factors:**
- ⭐ User demand (upvotes on GitHub)
- 🛠️ Implementation complexity
- 💰 Cost implications (API usage)
- 🎯 Alignment with core mission (price tracking)

---

*Last Updated: December 11, 2025*

