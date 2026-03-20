# Auto Tech News Scraper → LinkedIn Poster

## Setup Guide

Follow these steps to get the auto-poster running 24/7 on GitHub Actions.

---

## Step 1: Create a LinkedIn Developer App

1. Go to [LinkedIn Developers](https://developer.linkedin.com/)
2. Click **Create App**
3. Fill in:
   - **App name**: `Tech News Auto Poster` (or anything you like)
   - **LinkedIn Page**: Select your LinkedIn company page (create one if needed — it can be a simple placeholder page)
   - **App logo**: Upload any image
   - **Legal agreement**: Check the box
4. Click **Create App**

## Step 2: Request API Permissions

1. In your new app, go to the **Products** tab
2. Request access to:
   - ✅ **Share on LinkedIn** → grants `w_member_social` scope
   - ✅ **Sign In with LinkedIn using OpenID Connect** → grants `openid`, `email` scopes
3. Wait for approval (usually instant for Share on LinkedIn)

## Step 3: Get Your OAuth2 Access Token

### 3a. Note your Client ID and Client Secret
- Go to the **Auth** tab in your LinkedIn app
- Copy your **Client ID** and **Client Secret**
- Note your **Redirect URL** — add `http://localhost:8080/callback` if not already there

### 3b. Authorize via Browser
Open this URL in your browser (replace `YOUR_CLIENT_ID`):

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080/callback&scope=openid%20email%20w_member_social
```

- Log in to LinkedIn and click **Allow**
- You'll be redirected to localhost — the URL will contain `?code=XXXXXXX`
- **Copy that code** (everything after `code=` and before `&` if present)

### 3c. Exchange Code for Access Token
Run this in your terminal (replace the placeholders):

```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_AUTH_CODE" \
  -d "redirect_uri=http://localhost:8080/callback" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

**On Windows PowerShell**, use:
```powershell
Invoke-RestMethod -Method Post -Uri "https://www.linkedin.com/oauth/v2/accessToken" -Body @{
    grant_type    = "authorization_code"
    code          = "YOUR_AUTH_CODE"
    redirect_uri  = "http://localhost:8080/callback"
    client_id     = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
}
```

You'll get a JSON response with `access_token`. **Save this token — it expires in 60 days.**

## Step 4: Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your token
# Linux/Mac:
export LINKEDIN_ACCESS_TOKEN="your_token_here"
# Windows PowerShell:
$env:LINKEDIN_ACCESS_TOKEN="your_token_here"

# Dry run (no actual posting — test scraping and formatting)
python main.py --dry-run

# Live run (actually posts to LinkedIn)
python main.py
```

## Step 5: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: auto tech news poster"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 6: Add GitHub Secret

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `LINKEDIN_ACCESS_TOKEN`
4. Value: paste your access token from Step 3c
5. Click **Add secret**

## Step 7: Enable GitHub Actions

1. Go to your repo → **Actions** tab
2. You should see the **Auto Post Tech News to LinkedIn** workflow
3. Click **Enable workflow** if prompted
4. To test immediately: click **Run workflow** → **Run workflow**

✅ **Done!** The workflow will now run every hour automatically, even when your laptop is off.

---

## 🔄 Token Refresh (Every ~55 Days)

LinkedIn access tokens expire after **60 days**. To refresh:

1. Repeat **Step 3b** and **Step 3c** to get a new token
2. Update the `LINKEDIN_ACCESS_TOKEN` secret in GitHub (Step 6)

> **Tip**: Set a calendar reminder for 55 days from now so you don't forget!

---

## 📋 Troubleshooting

| Problem | Solution |
|---------|----------|
| `LINKEDIN_ACCESS_TOKEN not set` | Make sure the secret is added in GitHub repo settings |
| `HTTP 401 Unauthorized` | Your token has expired — refresh it (see above) |
| `HTTP 403 Forbidden` | Ensure "Share on LinkedIn" product is approved in your app |
| `No new articles found` | All recent articles were already posted — wait for new ones |
| Workflow not running | Check Actions tab → ensure workflow is enabled |
