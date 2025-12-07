# Railway Deployment Troubleshooting Guide

If your visualizations aren't working on Railway, follow these steps:

## Quick Checks

1. **Verify data files are committed:**
   ```bash
   git ls-files data/processed/
   ```
   You should see all CSV and JSON files listed.

2. **Check Railway logs:**
   - Go to Railway dashboard → Your project → Deployments → View Logs
   - Look for errors like "Failed to load data" or "File not found"
   - Check for Python tracebacks

3. **Test locally with deployment check:**
   ```bash
   python check_deployment.py
   ```

## Common Issues & Solutions

### Issue: "No visualizations loading" / Empty dashboard

**Possible causes:**
- Data files not found
- Path resolution issues
- JavaScript errors in browser

**Solutions:**
1. Check Railway logs for data loading errors
2. Open browser console (F12) and check for JavaScript errors
3. Verify `data/processed/` directory exists in your git repository
4. Check that files are not too large (Railway has file size limits)

### Issue: App crashes on startup

**Check Railway logs for:**
- Import errors (missing dependencies)
- Port binding errors
- Memory issues

**Solutions:**
1. Verify `requirements.txt` has all dependencies
2. Check Python version compatibility (project uses 3.10)
3. If memory issues, reduce gunicorn workers in `railway.json`:
   ```json
   "startCommand": "gunicorn src.app:server --bind 0.0.0.0:$PORT --workers 1 --threads 2"
   ```

### Issue: "502 Bad Gateway" or connection errors

**Possible causes:**
- App not starting correctly
- Port binding issues
- Timeout issues

**Solutions:**
1. Check Railway logs for startup errors
2. Verify start command in `railway.json` is correct
3. Increase timeout if needed (already set to 120 seconds)

## Alternative: Use Render.com

If Railway continues to have issues, try Render:

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.app:server --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
   - **Environment**: Python 3

## Alternative: Use Docker on Railway

Railway can use Dockerfile instead of Nixpacks:

1. In Railway project settings, switch to Dockerfile
2. Railway will automatically detect and use the `Dockerfile`
3. This provides more control over the build process

## Verify Deployment

After deploying, check:
1. App loads (you see the dashboard UI)
2. Data loads (check browser console for errors)
3. Filters work (try changing date range)
4. Visualizations render (maps, charts appear)

If any step fails, check the corresponding section above.

