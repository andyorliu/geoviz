# Railway Deployment Guide

This guide will help you deploy the LA Crime Data Visualization Dashboard to Railway.

## Prerequisites

1. A Railway account ([railway.app](https://railway.app))
2. Your GitHub repository with the project code
3. Processed data files in `data/processed/` directory (must be committed to git)

## Step 1: Prepare Your Repository

Ensure all necessary files are committed to your repository:

```bash
# Check that processed data files are tracked
git ls-files data/processed/

# If files are missing, add them
git add data/processed/
git commit -m "Add processed data files"
git push
```

**Important**: Railway needs access to your processed data files. Make sure:
- `data/processed/cleaned_data_sample.csv` exists
- `data/processed/area_aggregations.csv` exists
- `data/processed/metadata.json` exists
- All other processed CSV files are present

## Step 2: Create a New Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect it's a Python project

## Step 3: Configure Deployment

Railway will automatically:
- Detect Python from `requirements.txt`
- Use Nixpacks builder (configured in `railway.json`)
- Use the start command from `railway.json`

**No additional configuration needed!** The `railway.json` file handles everything.

## Step 4: Set Environment Variables (Optional)

Railway will automatically set the `PORT` environment variable. You can optionally set:

- `DASH_DEBUG=False` (recommended for production)
- `PYTHON_VERSION=3.10` (if you want to specify Python version)

To set environment variables:
1. Go to your Railway project
2. Click on your service
3. Go to "Variables" tab
4. Add any environment variables you need

## Step 5: Deploy

Railway will automatically deploy when you:
- Push to your main branch (if auto-deploy is enabled)
- Or manually trigger a deployment from the Railway dashboard

## Step 6: Verify Deployment

1. Wait for the deployment to complete (check the "Deployments" tab)
2. Railway will provide a URL (e.g., `https://your-app.railway.app`)
3. Visit the URL to verify the dashboard loads
4. Check that:
   - The dashboard UI loads
   - Data visualizations appear
   - Filters work correctly

## Troubleshooting

### App won't start

1. **Check Railway logs**: Go to your service → "Deployments" → Click on latest deployment → View logs
2. **Common issues**:
   - Missing dependencies: Check `requirements.txt` is complete
   - Port binding errors: Railway sets `$PORT` automatically, don't hardcode it
   - Data files not found: Ensure `data/processed/` files are committed to git

### Data not loading

1. **Verify data files are in repository**:
   ```bash
   git ls-files data/processed/
   ```
2. **Check Railway logs** for "File not found" errors
3. **Verify file paths**: The app uses relative paths from project root

### 502 Bad Gateway

- Check Railway logs for startup errors
- Verify the start command in `railway.json` is correct
- Ensure gunicorn is installed (it's in `requirements.txt`)

### Memory Issues

If you encounter memory issues, reduce workers in `railway.json`:

```json
"startCommand": "gunicorn src.app:server --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120"
```

## File Structure

Railway deployment uses these files:

- `railway.json` - Railway configuration (build and deploy settings)
- `Procfile` - Alternative start command (Railway will use `railway.json` first)
- `requirements.txt` - Python dependencies
- `src/app.py` - Main application file
- `data/processed/` - Processed data files (must be in repository)

## Updating Your Deployment

To update your deployment:

1. Make changes to your code
2. Commit and push to your repository:
   ```bash
   git add .
   git commit -m "Update dashboard"
   git push
   ```
3. Railway will automatically detect the push and redeploy (if auto-deploy is enabled)
4. Or manually trigger a deployment from Railway dashboard

## Support

If you encounter issues:

1. Check Railway logs first
2. Verify all files are committed to git
3. Test locally: `python src/app.py` should work
4. Check Railway status page: [status.railway.app](https://status.railway.app)

