# AzizAuto Telegram Bot Documentation

## Quick Start Guide

### Prerequisites
- Python 3.7+
- Telegram Bot Token from @BotFather

### Installation Steps

1. **Install Python library:**
   ```bash
   pip install python-telegram-bot
   ```
   Or if pip doesn't work:
   ```bash
   py -m pip install python-telegram-bot
   ```

2. **Set up your bot token:**
   - Open `azizauto_bot.py`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual token from BotFather

3. **Run the bot:**
   ```bash
   python azizauto_bot.py
   ```
   Or:
   ```bash
   py azizauto_bot.py
   ```

4. **Test your bot:**
   - Go to Telegram and search for your bot (@AzizAuto_bot)
   - Send `/start` command
   - Keep the Python script running - bot stops if you close command prompt

---

## Bot Features

### Main Menu Options
- 🔍 **Browse Cars** - View car categories and inventory
- 💰 **Get Quote** - Budget-based recommendations
- 📞 **Contact Us** - Business contact information
- ℹ️ **About Us** - Company information

### Car Categories
- **SUVs** (3 cars): Toyota RAV4, Honda CR-V, Mazda CX-5
- **Sedans** (3 cars): Toyota Camry, Honda Accord, Nissan Altima  
- **Sports Cars** (2 cars): BMW M3, Audi RS5

### Conversation Flow
```
/start → Main Menu
├── Browse Cars → Categories → Car List → Car Details
├── Get Quote → Budget Selection → Personalized Response
├── Contact Us → Contact Information
└── About Us → Company Information
```

---

## 24/7 Heroku Deployment Guide

### Step 1: Prepare Files

Create these files in your project folder:

**requirements.txt:**
```
python-telegram-bot
```

**Procfile** (no extension):
```
worker: python azizauto_bot.py
```

**runtime.txt** (optional):
```
python-3.11.9
```

### Step 2: Modify Bot Code for Production

Update `azizauto_bot.py` to use environment variables:

```python
import os
# Replace this line:
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# With this:
BOT_TOKEN = os.environ.get('BOT_TOKEN')
```

### Step 3: Heroku Account Setup

1. **Create Heroku account:** https://signup.heroku.com/
2. **Install Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli
3. **Login to Heroku:**
   ```bash
   heroku login
   ```

### Step 4: Git Setup

```bash
# Navigate to your project folder
cd "C:\Users\Owner\Documents\01_Projects\Telegram Bot"

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit"
```

### Step 5: Create Heroku App

```bash
# Create new Heroku app (replace 'your-bot-name' with unique name)
heroku create your-azizauto-bot

# Set bot token as environment variable
heroku config:set BOT_TOKEN=your_actual_bot_token_here

# Deploy to Heroku
git push heroku main
```

### Step 6: Start the Bot

```bash
# Scale up the worker
heroku ps:scale worker=1

# Check if bot is running
heroku logs --tail
```

### Step 7: Verify Deployment

- Bot should be running 24/7 on Heroku
- Test by messaging your bot on Telegram
- Check logs: `heroku logs --tail`

---

## Alternative Deployment: Railway

### Easier than Heroku:

1. **Sign up:** https://railway.app/
2. **Connect GitHub:** Upload your code to GitHub first
3. **Deploy:** Railway auto-detects Python and deploys
4. **Add environment variable:** BOT_TOKEN in Railway dashboard

---

## Customization Guide

### Adding New Cars
Edit the `CARS` dictionary in `azizauto_bot.py`:

```python
CARS = {
    'suvs': [
        {'name': 'New SUV Model', 'price': '$35,000', 'year': '2024'}
    ]
}
```

### Changing Contact Information
Update the `show_contact()` function:

```python
text = (
    "📞 *Contact AzizAuto*\n\n"
    "📱 Phone: YOUR_PHONE_NUMBER\n"
    "📧 Email: YOUR_EMAIL\n"
    # ... rest of contact info
)
```

### Adding New Menu Options
1. Add button to main menu keyboard
2. Add handler in `button_handler()` function
3. Create new async function for the feature

---

## File Structure
```
Telegram Bot/
├── azizauto_bot.py          # Main bot code
├── README.md                # This documentation
├── requirements.txt         # Dependencies (for deployment)
├── Procfile                 # Heroku deployment file
├── runtime.txt              # Python version (optional)
└── .git/                    # Git repository (created during deployment)
```

---

## Troubleshooting

### Local Issues

**Bot doesn't respond:**
- Check if script is running
- Verify bot token is correct
- Check internet connection

**Import errors:**
```bash
py -m pip install --upgrade python-telegram-bot
```

**Python 3.13 compatibility issues:**
- The bot code has been updated to work with Python 3.13
- If issues persist, downgrade: `py -m pip install python-telegram-bot==20.7`

### Heroku Issues

**Bot not starting:**
```bash
heroku logs --tail
```

**Check dyno status:**
```bash
heroku ps
```

**Restart bot:**
```bash
heroku restart
```

### Getting Help
- Check the error messages in console/logs
- Telegram Bot API documentation: https://core.telegram.org/bots/api
- python-telegram-bot library docs: https://docs.python-telegram-bot.org/
- Heroku documentation: https://devcenter.heroku.com/

---

## Security Notes

- Never share your bot token publicly
- Use environment variables for production
- Consider rate limiting for high traffic
- Keep your Heroku app private

---

## Cost Information

- **Telegram Bot API:** FREE
- **Heroku Eco Dynos:** $5/month (512 MB RAM, sleeps after 30 min inactivity)
- **Heroku Basic Dynos:** $7/month (512 MB RAM, never sleeps)
- **Railway:** $5/month (512 MB RAM, never sleeps)

---

## Next Steps

### Potential Enhancements
1. **Database integration** - Store car inventory in database
2. **User data collection** - Save customer inquiries  
3. **Image support** - Add car photos
4. **Payment integration** - Online payments
5. **Admin panel** - Manage inventory through bot
6. **Appointment booking** - Schedule test drives
7. **Location sharing** - Show dealership location

### Advanced Features
- Webhook instead of polling
- Multiple language support
- Analytics and user tracking
- Integration with CRM systems

---

*Last updated: August 2025*