# Setting Up GitHub Repository

You have a local git repository but need to connect it to GitHub. Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in:
   - **Repository name**: `crime-data-vis-project` (or any name you prefer)
   - **Description**: "LA Crime Data Visualization Dashboard - 2022"
   - **Visibility**: Choose **Public** (free) or **Private**
   - **DO NOT** check "Initialize with README" (you already have files)
4. Click **"Create repository"**

## Step 2: Connect Your Local Repository

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/crime-data-vis-project.git

# Push your code
git push -u origin main
```

## Quick Commands (Copy & Paste)

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/crime-data-vis-project.git
git branch -M main
git push -u origin main
```

## Alternative: Using SSH (If you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/crime-data-vis-project.git
git push -u origin main
```

## After Pushing

Once your code is on GitHub, you can:
1. Deploy to Railway/Render (they'll connect to your GitHub repo)
2. Share the repository URL with others
3. Continue pushing updates with `git push`

## Troubleshooting

**"Repository already exists" error?**
- You might have already created it. Just use the commands above.

**"Permission denied" error?**
- Make sure you're logged into GitHub
- Check that the repository name matches exactly
- Try using a personal access token instead of password

**Need to change the remote URL?**
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/crime-data-vis-project.git
```

