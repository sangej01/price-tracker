# Changelog

All notable changes to the Price Tracker project.

---

## [1.2.0] - 2025-12-10

### 🎯 Single .env Configuration

#### Simplified Configuration Structure
- **Consolidated to single `.env` file** at project root
- Both backend and frontend now read from the same `.env` file
- Eliminates confusion from multiple configuration files
- Clearer separation of defaults (in `config.py`) vs secrets (in `.env`)

#### Configuration Updates
- Updated `backend/app/config.py` to load `.env` from project root
- Updated `frontend/vite.config.ts` to read from parent directory `.env`
- Updated `config.py` to generate single `.env` file
- Renamed `BRIGHTDATA_ZONE` → `BRIGHTDATA_PROXY_NAME` (more intuitive)
- Clarified that API keys should NEVER be in `config.py`, only in `.env`

#### Documentation Updates
- Updated `CONFIG_GUIDE.md` with single `.env` structure
- Updated `README.md` configuration section
- All guides now reference single `.env` file location
- Fixed UTF-8 encoding issue in `.env` generation

### 🐛 Bug Fixes
- Fixed backend startup issue (wrong directory for uvicorn command)
- Fixed products not displaying (backend wasn't starting correctly)
- Fixed environment variable loading in `run.py`

---

## [1.1.0] - 2025-12-09

### 🎉 Major Features

#### Smart Cost-Saving Scraping
- **75% cost reduction!** App now tries FREE direct scraping first, only uses Bright Data when blocked
- Automatic fallback logic with intelligent content validation
- Detailed logging shows which method succeeded
- Real-world savings: $60/month → $14/month for typical 4-product setup

#### Central Configuration System
- New `config.py` at root with clear Backend/Frontend separation
- One-command configuration: `python apply_config.py`
- Auto-generates `.env` files for both backend and frontend
- Cost calculator table directly in config file
- Port changes automatically propagate to frontend

#### Documentation Improvements
- Added `CONFIG_GUIDE.md` - comprehensive configuration documentation
- Added `CHANGELOG.md` - this file!
- Updated all scraping guides with cost-saving information
- Added cost calculator tables to help users estimate expenses

### 🔧 Improvements

- Backend port changed from 8000 to 8081 (configurable)
- Removed all ScraperAPI references (using Bright Data only)
- Removed outdated Playwright references
- Organized all detailed guides into `/documentation` folder
- Switched from `master` to `main` branch
- Enhanced `.gitignore` for frontend

### 🐛 Bug Fixes

- Fixed scraper order (was trying paid service first)
- Fixed configuration priority (environment variables now properly loaded)
- Cleaned up vestigial code and variables

---

## [1.0.0] - 2025-12-09

### 🎉 Initial Release

#### Core Features
- Full-stack price tracker (FastAPI + React)
- Vendor-specific scrapers for Amazon, eBay, Newegg
- Automated scheduled scanning (APScheduler)
- Price history tracking with interactive charts
- Stock status monitoring
- Modern UI with Tailwind CSS
- Bright Data integration for protected sites

#### Backend
- FastAPI REST API
- SQLite database with SQLAlchemy ORM
- APScheduler for background scanning
- Vendor-specific and generic scrapers
- Commercial scraping service integration

#### Frontend
- React 18 with TypeScript
- Tailwind CSS styling
- Recharts for data visualization
- Real-time dashboard
- Product management with URL testing
- Price history charts

#### Documentation
- Comprehensive README
- Quick start guide
- Scraper development guides
- Commercial scraping setup guide
- Project architecture documentation

#### Deployment
- GitHub repository created
- Batch scripts for Windows (start-all.bat, etc.)
- Comprehensive .gitignore
- Production-ready configuration

---

## Future Roadmap

### Planned Features
- [ ] Email/SMS price drop alerts
- [ ] Multi-currency support
- [ ] Export to CSV/Excel
- [ ] Mobile app (React Native)
- [ ] Browser extension for easy product adding
- [ ] More vendor scrapers (Best Buy, Walmart, Target)
- [ ] Per-product scraping service selection
- [ ] Price predictions with ML
- [ ] Price comparison between vendors

---

**Repository:** https://github.com/sangej01/price-tracker  
**Documentation:** [README.md](README.md) | [QUICK_START.md](QUICK_START.md) | [CONFIG_GUIDE.md](CONFIG_GUIDE.md)


