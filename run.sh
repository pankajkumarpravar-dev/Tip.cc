# For Railway/Heroku deployment
import os
import sys

# Ensure database is stored in a writable location
if not os.path.exists('data'):
    os.makedirs('data', exist_ok=True)

if __name__ == '__main__':
    # Import after ensuring directories exist
    import subprocess
    subprocess.run([sys.executable, 'bot.py'])
