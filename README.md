# WASTE SOTOR

A Django web application for waste management and recycling tips.

## Accessing the Application via IP Address

### Quick Start

1. **First-time setup:** Make sure the virtual environment is activated and all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```

2. **Run the server** (this will automatically detect your IP address):
   ```
   run_server.bat
   ```
   
   Or with static files collection:
   ```
   run_with_static.bat
   ```

3. **Important:** If this is the first time running the server with network access, you may need to **allow the application through your firewall** when prompted.

4. The application will be accessible at:
   - Local: http://127.0.0.1:8000
   - Network: http://YOUR_IP_ADDRESS:8000 (the script will display your actual IP)

5. Share the network URL with others on the same network to access the application.

### Troubleshooting

If you're having trouble accessing the app from other devices:

1. Run the network check script:
   ```
   check_network.bat
   ```

2. See the detailed troubleshooting guide:
   ```
   NETWORK_TROUBLESHOOTING.md
   ```

### Finding Your IP Address

You can find your IP address using:

```
ipconfig
```

Look for the IPv4 Address under your active network adapter.

### Manual Server Start

If you prefer to run the server manually:

```
cd waste-sotor
.\env\Scripts\python manage.py collectstatic --noinput  # Optional, for static files
.\env\Scripts\python manage.py runserver 0.0.0.0:8000
```

## Note on Security

The current configuration allows access from any IP address. This is suitable for development and local network use, but not for production deployment.

For production, you should:
- Set DEBUG = False in settings.py
- Configure specific ALLOWED_HOSTS
- Use a proper web server (like Nginx or Apache) with WSGI
- Set up HTTPS
