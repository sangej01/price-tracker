# 🛒 Price Tracker Application

**Automated price monitoring and tracking across multiple vendor websites**

A full-stack web application that monitors product prices, tracks historical data, and displays trends through an intuitive dashboard. Built with FastAPI backend and modern React frontend.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Tech Stack](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Tech Stack](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![Tech Stack](https://img.shields.io/badge/Tailwind-38B2AC?style=flat&logo=tailwind-css&logoColor=white)

---

## ✨ Key Features

- 🔍 **Smart Web Scraping** - Vendor-specific scrapers (Amazon, eBay, Newegg) with fallback support
- 🌐 **Commercial Scraping Integration** - Optional Bright Data for protected sites
- 📊 **Real-time Price Tracking** - Monitor prices with visual change indicators
- 📈 **Interactive Charts** - Historical price trends with Recharts
- 🔄 **Automated Scheduling** - Configurable scan frequencies per product
- 💼 **Multi-Vendor Support** - Track products across different websites
- 📱 **Modern UI** - Responsive design with Tailwind CSS
- 📦 **Stock Status Monitoring** - Track product availability
- 🧪 **URL Testing** - Pre-validate product URLs before adding

---

## 🚀 Quick Start

**See [QUICK_START.md](QUICK_START.md) for detailed setup instructions**

### Prerequisites
- Python 3.10+
- Node.js 18+

### Quick Setup (Windows)
```powershell
# Run everything with one command
start-all.bat
```

### Manual Setup
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🏗️ Technology Stack

### Backend
- **FastAPI** - High-performance async web framework
- **SQLAlchemy** - ORM for SQLite database
- **BeautifulSoup4** - HTML parsing and web scraping
- **APScheduler** - Background job scheduling
- **aiohttp** - Async HTTP client
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **React Router** - SPA routing
- **Vite** - Fast build tool

### Web Scraping
- **Vendor-specific scrapers** for Amazon, eBay, Newegg
- **Generic scraper** with price pattern detection
- **Bright Data integration** (optional, pay-per-use)

---

## 📖 Usage

### 1️⃣ Add Vendors
Navigate to **Vendors** → Create vendors for tracking (e.g., "Amazon", "eBay")

### 2️⃣ Add Products
Go to **Products** → Add product details:
- Product name
- Full product URL
- Select vendor
- Set scan frequency (minutes)

💡 **Pro Tip:** Use the **"Test URL"** feature to validate the URL extracts price correctly!

### 3️⃣ Monitor Dashboard
View all tracked products with:
- Current prices
- Price change indicators (↑↓→)
- Stock status
- Product images

### 4️⃣ Analyze Trends
Click **"View Details"** on any product for:
- Interactive price history chart
- Statistics (min, max, average)
- Manual scan trigger

### 5️⃣ Scan Products
- **Auto-scan**: Runs every 15 minutes for due products
- **Manual**: Click "Scan All Products" or scan individual items

---

## 🌐 Commercial Scraping Service

For protected sites (Amazon, eBay with CAPTCHA), integrate Bright Data:

### Bright Data
- **Pay-as-you-go pricing** (~$0.001-0.01 per request)
- **95%+ success rate** on protected sites
- **Datacenter & Residential proxies**
- **Unlocker API** handles JavaScript & CAPTCHAs automatically

**Setup Guide:** See [documentation/SCRAPING_SERVICES_GUIDE.md](documentation/SCRAPING_SERVICES_GUIDE.md)

**Quick Setup:**
```bash
# Create .env in backend/
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=your_api_key
BRIGHTDATA_ZONE=your_zone_name
```

---

## 📚 Documentation

### For Users
- **[QUICK_START.md](QUICK_START.md)** - Setup and installation
- **[documentation/QUICK_USER_GUIDE.md](documentation/QUICK_USER_GUIDE.md)** - How to use the app
- **[documentation/DEMO_SUMMARY.md](documentation/DEMO_SUMMARY.md)** - Visual walkthrough

### For Developers
- **[documentation/PROJECT_OVERVIEW.md](documentation/PROJECT_OVERVIEW.md)** - Architecture details
- **[documentation/CUSTOM_SCRAPERS_GUIDE.md](documentation/CUSTOM_SCRAPERS_GUIDE.md)** - Add vendor scrapers
- **[documentation/SCRAPING_SERVICES_GUIDE.md](documentation/SCRAPING_SERVICES_GUIDE.md)** - Commercial APIs setup
- **[documentation/README.md](documentation/README.md)** - Full documentation index

---

## 🛠️ Development

### Project Structure
```
Price Tracker/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── scrapers/         # Scraping logic
│   │   │   ├── amazon_scraper.py
│   │   │   ├── ebay_scraper.py
│   │   │   ├── newegg_scraper.py
│   │   │   ├── scraping_service.py
│   │   │   └── base_scraper.py
│   │   ├── services/         # Business logic
│   │   ├── config.py         # Configuration
│   │   ├── models.py         # Database models
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   └── test_scraper.py       # Testing tool
├── frontend/
│   └── src/
│       ├── api/              # API client
│       ├── components/       # React components
│       └── pages/            # Page views
├── documentation/            # Detailed guides
├── README.md                 # This file
└── QUICK_START.md           # Setup guide
```

### Adding Custom Scrapers

**Quick Example:**
```python
# backend/app/scrapers/mysite_scraper.py
from .base_scraper import BaseScraper

class MySiteScraper(BaseScraper):
    async def scrape(self):
        html = await self.fetch_page()
        soup = BeautifulSoup(html, 'lxml')
        
        price = self.parse_price(soup.find('span', class_='price').text)
        in_stock = 'out of stock' not in html.lower()
        
        return {
            "price": price,
            "in_stock": in_stock,
            "currency": "USD",
            "image_url": soup.find('img', class_='product-image')['src']
        }
```

Register in `scraper_factory.py` and test:
```bash
python backend/test_scraper.py https://product-url
```

**Full Guide:** [documentation/CUSTOM_SCRAPERS_GUIDE.md](documentation/CUSTOM_SCRAPERS_GUIDE.md)

---

## 🔧 Configuration

### Environment Variables (Optional)
Create `backend/.env`:
```env
# Database
DATABASE_URL=sqlite:///./sql_app.db

# Scheduler
SCAN_INTERVAL_MINUTES=15

# Commercial Scraping (Optional)
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=your_key
BRIGHTDATA_ZONE=your_zone
```

### Scan Frequency
- **Per-product**: Set when creating/editing products (default: 60 minutes)
- **Global check**: Scheduler runs every 15 minutes to find due products

---

## 🐛 Troubleshooting

### Scraping Failures
**Problem:** "Failed to fetch page" or "Price not available"

**Solutions:**
1. Check if URL is correct (use "Test URL" feature)
2. Website may block scrapers → Use Bright Data commercial service
3. Website structure changed → Update scraper selectors

### API Connection Errors
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`

### Database Reset
```bash
# Delete database and restart
cd backend
rm price_tracker.db
python -m app.main
```

---

## 🚧 Future Enhancements

- [ ] Email/SMS price drop alerts
- [ ] Multi-currency support
- [ ] Export to CSV/Excel
- [ ] Mobile app (React Native)
- [ ] Browser extension
- [ ] Price predictions with ML
- [ ] More vendor scrapers (Best Buy, Walmart, Target)

---

## 📄 License

MIT License - Free for personal and commercial use

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

- **Documentation:** [documentation/](documentation/)
- **Issues:** Create a GitHub issue
- **API Docs:** http://localhost:8000/docs (when running)

---

**Built with ❤️ using FastAPI and React**
