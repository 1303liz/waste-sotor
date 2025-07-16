# Network Access Troubleshooting Guide

If you're having trouble accessing your Django application from other devices on your network, follow these troubleshooting steps:

## Basic Checks

1. **Run the check_network.bat script**
   ```
   check_network.bat
   ```
   This will display your IP address and check if port 8000 is available.

2. **Ensure the server is running with the correct binding**
   ```
   run_server.bat
   ```
   Make sure it shows "Starting server on 0.0.0.0:8000..."

## Common Issues and Solutions

### 1. Firewall Blocking Access

Windows Firewall often blocks incoming connections. To allow Django through:

1. Run Command Prompt as Administrator
2. Execute this command (adjust the path if needed):
   ```
   netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow program="%USERPROFILE%\Downloads\waste-sotor\env\Scripts\python.exe" protocol=TCP localport=8000
   ```

### 2. Antivirus Software

Some antivirus software might block incoming connections. Try temporarily disabling your antivirus to test.

### 3. Router Issues

- Some routers have "client isolation" or "AP isolation" enabled, which prevents devices from communicating with each other
- Check your router settings and disable this feature if needed

### 4. Incorrect IP Address

Make sure you're using the correct IP address:
1. Open Command Prompt
2. Type `ipconfig`
3. Look for "IPv4 Address" under your active network adapter (Ethernet or Wi-Fi)
4. Use this IP address followed by :8000 (e.g., http://192.168.1.100:8000)

### 5. Django Configuration

Ensure Django's settings.py has the correct configuration:
- ALLOWED_HOSTS should include '*' or your specific IP address
- DEBUG should be True for development

### 6. Network Type

Make sure your network is set as "Private" in Windows:
1. Go to Settings > Network & Internet
2. Click on your active connection
3. Set network profile to "Private"

## Advanced Checks

1. **Test if the port is accessible**
   On the server machine:
   ```
   netstat -an | find "0.0.0.0:8000"
   ```
   Should show the port is LISTENING

2. **Test with curl**
   On the server machine:
   ```
   curl http://localhost:8000
   ```
   Should return the HTML content of your site

## Still Having Issues?

If none of these solutions work:

1. Try accessing using just the IP (without the hostname)
2. Check if any proxy settings are configured in your browser
3. Try a different browser
4. Check Windows Event Viewer for any relevant firewall or security alerts

## Note on Production Deployment

For a proper production setup, consider:
1. Using Gunicorn or uWSGI instead of the development server
2. Setting up Nginx or Apache as a reverse proxy
3. Configuring HTTPS
4. Setting DEBUG=False and specific ALLOWED_HOSTS
