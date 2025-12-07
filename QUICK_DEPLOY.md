# Quick Deployment Guide

This guide shows you the **fastest ways** to host your dashboard online so others can access it.

## 🚀 Option 1: Railway (Recommended - Easiest & Free)

**Time: ~5 minutes**

1. **Sign up**: Go to [railway.app](https://railway.app) and sign up with GitHub

2. **Create new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure** (Railway auto-detects, but verify):
   - Railway will automatically detect it's a Python app
   - It will use the `Procfile` we created
   - Make sure the start command is: `gunicorn src.app:server --bind 0.0.0.0:$PORT`

4. **Deploy**:
   - Railway will automatically build and deploy
   - You'll get a URL like: `https://your-app-name.up.railway.app`

5. **Done!** Share the URL with others

**Free tier**: 500 hours/month (plenty for a dashboard)

---

## 🚀 Option 2: Render (Also Easy & Free)

**Time: ~5 minutes**

1. **Sign up**: Go to [render.com](https://render.com) and sign up with GitHub

2. **Create new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure**:
   - **Name**: `crime-dashboard` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.app:server --bind 0.0.0.0:$PORT`

4. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - You'll get a URL like: `https://crime-dashboard.onrender.com`

5. **Done!** Share the URL

**Free tier**: Free tier available (may spin down after inactivity, but wakes up on first request)

---

## 🚀 Option 3: PythonAnywhere (Simple & Free)

**Time: ~10 minutes**

1. **Sign up**: Go to [pythonanywhere.com](https://www.pythonanywhere.com) (free account)

2. **Upload files**:
   - Go to "Files" tab
   - Upload your project files (or use Git clone)

3. **Create Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.11
   - Click "Next" → "Next"

4. **Configure**:
   - Edit the WSGI file to point to your app:
   ```python
   import sys
   path = '/home/yourusername/crime-data-vis-project'
   if path not in sys.path:
       sys.path.append(path)
   
   from src.app import server as application
   ```

5. **Install dependencies**:
   - Go to "Tasks" tab
   - Run: `pip3.11 install --user -r requirements.txt`

6. **Reload**:
   - Go back to "Web" tab
   - Click "Reload" button

7. **Done!** Your app will be at: `https://yourusername.pythonanywhere.com`

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [x] ✅ `Procfile` exists (for Railway/Render)
- [x] ✅ `requirements.txt` includes `gunicorn`
- [x] ✅ `src/app.py` has `server = app.server` line
- [x] ✅ Data files are in `data/processed/` (or will be generated)
- [ ] ⚠️ **Important**: Check if processed data files are too large for Git

### If data files are large:

**Option A**: Include them in Git (if < 100MB total)
```bash
git add data/processed/
git commit -m "Add processed data"
```

**Option B**: Generate on first run (add to deployment)
- Add a startup script that runs `preprocess_data.py` if files don't exist
- Or use a cloud storage service (S3, etc.)

**Option C**: Use Git LFS for large files
```bash
git lfs install
git lfs track "data/processed/*.parquet"
git add .gitattributes
```

---

## 🔧 Quick Fixes for Common Issues

### Issue: "Module not found"
**Fix**: Make sure all dependencies are in `requirements.txt`

### Issue: "Port already in use"
**Fix**: The `$PORT` environment variable should be set by the hosting platform automatically

### Issue: "Data files not found"
**Fix**: 
1. Make sure `data/processed/` is committed to Git, OR
2. Add a startup script to generate data if missing

### Issue: "App crashes on startup"
**Fix**: Check logs in your hosting platform's dashboard

---

## 🎯 Recommended: Railway

**Why Railway?**
- ✅ Easiest setup (just connect GitHub)
- ✅ Free tier (500 hours/month)
- ✅ Auto-deploys on git push
- ✅ Good documentation
- ✅ No credit card required

**Steps**:
1. Push your code to GitHub
2. Sign up at railway.app
3. Connect GitHub repo
4. Deploy!
5. Share the URL

---

## 📝 After Deployment

1. **Test the URL**: Make sure all visualizations load
2. **Check performance**: First load might be slow (data loading)
3. **Share**: Send the URL to others
4. **Monitor**: Check your hosting platform's dashboard for usage/errors

---

## 🔐 Optional: Custom Domain

Most platforms allow you to add a custom domain:
- Railway: Settings → Domains
- Render: Settings → Custom Domains
- PythonAnywhere: Web tab → Static files / Misc

---

## Need Help?

- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **PythonAnywhere Docs**: https://help.pythonanywhere.com

