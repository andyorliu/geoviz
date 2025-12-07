# Deployment Guide

This guide covers different options for deploying the LA Crime Data Visualization Dashboard.

## Option 1: Local Development

The simplest way to run the dashboard is locally:

```bash
python src/app.py
```

Then access at `http://localhost:8050`

## Option 2: Streamlit Cloud (Alternative)

If you prefer Streamlit over Dash, you can convert the app to Streamlit and deploy to Streamlit Cloud:

1. Convert `app.py` to use Streamlit instead of Dash
2. Push to GitHub
3. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
4. Deploy automatically

## Option 3: Heroku

1. Create a `Procfile`:
```
web: gunicorn src.app:server
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Install gunicorn:
```bash
pip install gunicorn
```

4. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

## Option 4: Railway (Updated Configuration)

1. The project includes `railway.json` and `nixpacks.toml` for Railway deployment:
   - `railway.json`: Main Railway configuration
   - `nixpacks.toml`: Build configuration for Nixpacks
   - `Procfile`: Alternative process file

2. Connect GitHub repository to Railway:
   - Go to [railway.app](https://railway.app)
   - Create new project → Deploy from GitHub repo
   - Select your repository

3. Railway will automatically:
   - Detect Python project
   - Use the build command from `railway.json`
   - Deploy with the start command

4. **Troubleshooting Railway Issues:**
   - Check Railway logs for errors (View Logs in Railway dashboard)
   - Verify data files are committed to git (run `git ls-files data/processed/`)
   - Ensure `data/processed/` directory exists in repository
   - Check that PORT environment variable is set (Railway sets this automatically)
   - If visualizations don't load, check browser console for JavaScript errors
   - Run `python check_deployment.py` locally to verify paths

## Option 5: GitHub Pages (Static Export)

For GitHub Pages, you need to export the dashboard as static HTML. However, this will lose interactivity. A better approach is to:

1. Use Plotly's static export feature
2. Export individual visualizations as HTML
3. Create a static HTML page that links to these

**Note**: Full interactivity requires a running server, so GitHub Pages is not ideal for Dash apps.

## Option 6: Docker (Alternative Deployment)

A `Dockerfile` is included in the project. This is useful for:
- Local testing of deployment environment
- Alternative to Railway/Render
- Consistent deployment across platforms

Build and run:
```bash
docker build -t crime-dashboard .
docker run -p 8050:8050 -e PORT=8050 crime-dashboard
```

Or use with Railway:
- Railway can detect and use Dockerfile automatically
- Set Railway to use Dockerfile instead of Nixpacks if preferred

## Recommended: Railway or Heroku

For a fully interactive dashboard with cross-filtering, Railway or Heroku are recommended as they support Python web applications.

## Environment Variables

If needed, you can set environment variables for:
- `DASH_DEBUG`: Set to `False` for production
- `PORT`: Server port (usually set by hosting platform)

## Data Files

**Important**: Make sure processed data files are included in deployment:
- The `data/processed/` directory is tracked in git (see `.gitignore`)
- Files should be committed: `git add data/processed/ && git commit`
- Verify with: `git ls-files data/processed/`

If visualizations don't work after deployment:
1. Check Railway logs for "Failed to load data" messages
2. Verify data files exist: Check Railway file explorer or logs
3. Run `python check_deployment.py` to diagnose path issues
4. Ensure `data/processed/` directory structure is preserved

## Troubleshooting Common Issues

### Visualizations Not Loading
1. **Check browser console** (F12) for JavaScript errors
2. **Check Railway logs** for Python errors during data loading
3. **Verify data files**: Ensure `data/processed/*.csv` files are in repository
4. **Path issues**: The data loader tries multiple path strategies automatically

### App Crashes on Startup
1. Check Railway logs for import errors
2. Verify all dependencies in `requirements.txt` are correct
3. Check Python version compatibility (project uses Python 3.10)

### Port Binding Issues
- Railway automatically sets `$PORT` environment variable
- The start command uses `--bind 0.0.0.0:$PORT`
- If using Docker, ensure PORT env var is passed

### Gunicorn Worker Issues
- Current config: `--workers 2 --threads 4 --timeout 120`
- Adjust based on your Railway plan limits
- For free tier, you may need `--workers 1`

