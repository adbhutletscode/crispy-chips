# Crispy Chips Production Deployment Guide

This document provides comprehensive instructions for DevOps engineers to deploy and maintain the Crispy Chips e-commerce application on a production server.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Server Setup](#server-setup)
3. [Application Installation](#application-installation)
4. [Web Server Configuration](#web-server-configuration)
5. [Database Management](#database-management)
6. [Security Configuration](#security-configuration)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)
9. [Maintenance Procedures](#maintenance-procedures)
10. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Hardware Requirements
- CPU: 2+ cores
- RAM: 4GB minimum, 8GB recommended
- Storage: 20GB minimum

### Software Requirements
- Operating System: Ubuntu 20.04 LTS or newer
- Python: 3.8 or newer
- Web Server: Nginx
- WSGI Server: Gunicorn
- Database: SQLite (default) or PostgreSQL for production
- SSL Certificate: Let's Encrypt recommended

## Server Setup

### 1. Update System and Install Dependencies

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git
```

### 2. Create Application Directory and Clone Repository

```bash
# Create application directory
sudo mkdir -p /var/www/crispychips
sudo chown $(whoami):$(whoami) /var/www/crispychips
cd /var/www/crispychips

# Clone the repository
git clone https://github.com/yourusername/crispy-chips.git .
```

## Application Installation

### 1. Set Up Python Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### 2. Configure Application

Create or update the `config.py` file:

```python
# Production configuration
SECRET_KEY = 'your-secure-random-key'  # Generate a secure random key
ADMIN_USERNAME = 'admin'  # Change this
ADMIN_PASSWORD = 'secure-password'  # Change this
DEBUG = False
```

You can generate a secure random key with:

```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
```

## Web Server Configuration

### 1. Set Up Gunicorn Service

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/crispychips.service
```

Add the following content:

```
[Unit]
Description=Gunicorn instance to serve Crispy Chips application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/crispychips
Environment="PATH=/var/www/crispychips/venv/bin"
ExecStart=/var/www/crispychips/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 run:app
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 2. Configure Nginx

Create a new Nginx site configuration:

```bash
sudo nano /etc/nginx/sites-available/crispychips
```

Add the following content:

```
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/crispychips/static;
        expires 30d;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/crispychips /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### 3. Set Up SSL with Let's Encrypt (Recommended)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 4. Set Proper Permissions

```bash
sudo chown -R www-data:www-data /var/www/crispychips
sudo chmod -R 755 /var/www/crispychips
```

### 5. Start and Enable Services

```bash
sudo systemctl daemon-reload
sudo systemctl start crispychips
sudo systemctl enable crispychips
sudo systemctl restart nginx
```

## Database Management

The application uses SQLite by default, which is suitable for low to medium traffic sites. For higher traffic, consider migrating to PostgreSQL.

### SQLite Backup (Default Database)

```bash
# Create backup directory
sudo mkdir -p /var/backups/crispychips

# Backup SQLite database
sudo cp /var/www/crispychips/instance/database.db /var/backups/crispychips/database_$(date +%Y%m%d).db
```

### PostgreSQL Migration (Optional for Higher Traffic)

1. Install PostgreSQL:
```bash
sudo apt install -y postgresql postgresql-contrib
```

2. Create database and user:
```bash
sudo -u postgres psql
postgres=# CREATE DATABASE crispychips;
postgres=# CREATE USER crispychipsuser WITH PASSWORD 'secure-password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE crispychips TO crispychipsuser;
postgres=# \q
```

3. Install Python PostgreSQL adapter:
```bash
source /var/www/crispychips/venv/bin/activate
pip install psycopg2-binary
```

4. Update the application configuration to use PostgreSQL (requires code changes).

## Security Configuration

### 1. Firewall Configuration

```bash
# Install and configure UFW
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### 2. Secure Cookies and HTTPS

Update the Flask application to use secure cookies when deployed with HTTPS by adding the following to your configuration:

```python
SESSION_COOKIE_SECURE = True
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True
```

### 3. Rate Limiting

Add rate limiting to Nginx to prevent abuse:

```bash
sudo nano /etc/nginx/sites-available/crispychips
```

Add the following to the server block:

```
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
location / {
    limit_req zone=one burst=5;
    # other configurations...
}
```

### 4. Content Security Policy

Add a Content Security Policy header to Nginx:

```
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'";
```

## Monitoring and Logging

### 1. Configure Log Directories

```bash
# Create log directory
sudo mkdir -p /var/www/crispychips/logs
sudo chown www-data:www-data /var/www/crispychips/logs
```

### 2. Configure Log Rotation

```bash
sudo nano /etc/logrotate.d/crispychips
```

Add the following content:

```
/var/www/crispychips/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload crispychips
    endscript
}
```

### 3. Basic Monitoring

```bash
# Monitor CPU and memory usage
htop

# Monitor disk usage
df -h

# Monitor application logs
tail -f /var/www/crispychips/logs/app.log
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
journalctl -u crispychips
```

### 4. Advanced Monitoring (Recommended)

For production environments, consider setting up:

- **Prometheus**: For metrics collection
- **Grafana**: For visualization
- **Alertmanager**: For alerts
- **ELK Stack**: For centralized logging

## Backup and Recovery

### 1. Automated Backups

Create a backup script:

```bash
sudo nano /usr/local/bin/backup-crispychips.sh
```

Add the following content:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/crispychips"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
cp /var/www/crispychips/instance/database.db $BACKUP_DIR/database_$TIMESTAMP.db

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$TIMESTAMP.tar.gz /var/www/crispychips/static/uploads

# Backup configuration
cp /var/www/crispychips/config.py $BACKUP_DIR/config_$TIMESTAMP.py

# Remove backups older than 30 days
find $BACKUP_DIR -type f -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -type f -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -type f -name "*.py" -mtime +30 -delete
```

Make it executable and add to crontab:

```bash
sudo chmod +x /usr/local/bin/backup-crispychips.sh
echo "0 2 * * * /usr/local/bin/backup-crispychips.sh" | sudo tee -a /etc/crontab
```

### 2. Recovery Procedure

```bash
# Stop services
sudo systemctl stop crispychips

# Restore database
sudo cp /var/backups/crispychips/database_YYYYMMDD.db /var/www/crispychips/instance/database.db

# Restore uploads
sudo tar -xzf /var/backups/crispychips/uploads_YYYYMMDD.tar.gz -C /

# Restore configuration
sudo cp /var/backups/crispychips/config_YYYYMMDD.py /var/www/crispychips/config.py

# Set proper permissions
sudo chown -R www-data:www-data /var/www/crispychips

# Start services
sudo systemctl start crispychips
```

## Maintenance Procedures

### 1. Updating the Application

```bash
# Navigate to application directory
cd /var/www/crispychips

# Pull latest changes
sudo git pull

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Restart services
sudo systemctl restart crispychips
```

### 2. Regular Security Updates

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Restart services if needed
sudo systemctl restart nginx crispychips
```

### 3. Database Maintenance

For SQLite:

```bash
# Vacuum the database to optimize performance
sqlite3 /var/www/crispychips/instance/database.db "VACUUM;"
```

For PostgreSQL:

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Vacuum the database
postgres=# VACUUM ANALYZE crispychips;
postgres=# \q
```

## Troubleshooting

### 1. Application Not Starting

```bash
# Check logs
sudo journalctl -u crispychips

# Verify Python environment
source /var/www/crispychips/venv/bin/activate
python -c "import flask; print(flask.__version__)"

# Check file permissions
sudo ls -la /var/www/crispychips
```

### 2. Nginx Returning 502 Bad Gateway

```bash
# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify Gunicorn is running
ps aux | grep gunicorn

# Restart Gunicorn
sudo systemctl restart crispychips
```

### 3. Static Files Not Loading

```bash
# Check Nginx configuration
sudo nginx -t

# Verify file permissions
sudo ls -la /var/www/crispychips/static

# Check Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### 4. Database Issues

```bash
# Check if database file exists
ls -la /var/www/crispychips/instance/database.db

# Verify database permissions
sudo chown www-data:www-data /var/www/crispychips/instance/database.db
sudo chmod 644 /var/www/crispychips/instance/database.db
```

### 5. Memory or CPU Issues

```bash
# Check system resources
htop

# Check for memory leaks
sudo ps aux --sort=-%mem | head -10

# Restart the application if needed
sudo systemctl restart crispychips
```

## Performance Tuning

### 1. Gunicorn Workers

Adjust the number of Gunicorn workers based on your server's CPU cores:

```bash
sudo nano /etc/systemd/system/crispychips.service
```

Update the ExecStart line:

```
ExecStart=/var/www/crispychips/venv/bin/gunicorn --workers $(( 2 * $(nproc) + 1 )) --bind 127.0.0.1:8000 run:app
```

### 2. Nginx Caching

Add caching for static assets:

```
location /static {
    alias /var/www/crispychips/static;
    expires 30d;
    add_header Cache-Control "public, max-age=2592000";
}
```

### 3. Database Optimization

For SQLite:
- Regular VACUUM operations
- Consider moving to PostgreSQL for high traffic

For PostgreSQL:
- Tune shared_buffers, work_mem, and other parameters
- Set up proper indexing

## Contact Information

For urgent issues or questions, contact:
- DevOps Team: devops@crispychips.com
- Development Team: dev@crispychips.com
- Emergency Support: +1 (555) 123-4567

---

*This documentation was last updated on: June 2023*