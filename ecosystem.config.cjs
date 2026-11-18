module.exports = {
  apps: [
    {
      name: 'tai-worker',
      cwd: __dirname,
      script: 'run.py',
      interpreter: '.venv/bin/python',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      kill_timeout: 10000,
      env: {
        PYTHONUNBUFFERED: '1'
      }
    }
  ]
};
