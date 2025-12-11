# User Tools

All day-to-day utilities for managing your Price Tracker application.

---

## 🚀 Quick Start Scripts (Double-click in Windows Explorer)

### Server Management

| Script | Description | When to Use |
|--------|-------------|-------------|
| **start-all.bat** | Start both backend and frontend | First time or full restart |
| **start-backend.bat** | Start backend only (port 8081) | Testing backend changes |
| **start-frontend.bat** | Start frontend only (port 3000) | Testing UI changes |
| **kill-all.bat** | Stop all Python and Node.js processes | Before restarting or closing |

### Data Management

| Script | Description | When to Use |
|--------|-------------|-------------|
| **clean-data.bat** | Clean bad price data from database | Fix incorrect price history |

---

## 🔧 Configuration Tools

### apply_config.py

Apply changes from `config.py` to `.env` file.

**Usage:**
```powershell
cd user_tools
python apply_config.py
```

**When to use:**
- After editing `config.py` (port, scan interval, etc.)
- To regenerate `.env` from defaults

---

## 📋 How to Use

### Windows File Explorer (Easiest!)
1. Open File Explorer
2. Navigate to `user_tools` folder
3. **Double-click** any `.bat` file to run it
4. Command window opens and executes

### From Cursor/VS Code Terminal
```powershell
cd user_tools
.\start-all.bat
```

**Note:** Double-clicking `.bat` files in Cursor **opens them for editing**, not running!

---

## 🔄 Typical Workflows

### Daily Start
```powershell
# In Windows Explorer:
Double-click: user_tools\start-all.bat
```

### Clean Restart
```powershell
# In Windows Explorer:
1. Double-click: user_tools\kill-all.bat
2. Double-click: user_tools\start-all.bat
```

### Configuration Change
```powershell
# 1. Edit config.py in root
# 2. Open terminal:
cd user_tools
python apply_config.py
# 3. In Windows Explorer:
Double-click: user_tools\kill-all.bat
Double-click: user_tools\start-all.bat
```

### Clean Bad Price Data
```powershell
# In Windows Explorer:
Double-click: user_tools\clean-data.bat

# Follow the interactive menu:
# 1. List all products
# 2. Delete ALL price history for a product
# 3. Delete records with specific bad price
# 4. Exit
```

---

## 🆘 Troubleshooting

### "Scripts don't run when I double-click"
- ✅ Make sure you're in **Windows File Explorer**, not Cursor/VS Code
- ✅ Right-click → **Run as Administrator** if needed

### "Port already in use"
- ✅ Run `kill-all.bat` first to stop any running processes
- ✅ Check Task Manager for lingering python.exe or node.exe processes

### "Changes don't take effect"
- ✅ Always run `kill-all.bat` before `start-all.bat` after config changes
- ✅ Make sure you ran `apply_config.py` after editing `config.py`

---

**See [../README.md](../README.md) for full documentation**


