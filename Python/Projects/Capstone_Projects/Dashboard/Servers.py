servers = [
    {
        "hostname": "web-prod-01",
        "ip": "10.0.1.1",
        "role": "web",
        "cpu_percent": 72.5,
        "mem_percent": 65.0,
        "disk_percent": 40.2,
        "uptime_days": 120,
        "open_ports": [80, 443, 22],
        "tags": {"prod", "us-east-1"}
    },
    {
        "hostname": "web-prod-02",
        "ip": "10.0.1.2",
        "role": "web",
        "cpu_percent": 91.3,
        "mem_percent": 88.7,
        "disk_percent": 55.1,
        "uptime_days": 95,
        "open_ports": [80, 443, 22],
        "tags": {"prod", "us-east-1"}
    },
    {
        "hostname": "db-prod-01",
        "ip": "10.0.2.1",
        "role": "db",
        "cpu_percent": 45.0,
        "mem_percent": 78.4,
        "disk_percent": 83.9,
        "uptime_days": 200,
        "open_ports": [5432, 22],
        "tags": {"prod", "us-west-2"}
    },
    {
        "hostname": "db-prod-02",
        "ip": "10.0.2.2",
        "role": "db",
        "cpu_percent": 38.2,
        "mem_percent": 55.1,
        "disk_percent": 91.0,
        "uptime_days": 200,
        "open_ports": [5432, 22],
        "tags": {"prod", "us-west-2"}
    },
    {
        "hostname": "cache-prod-01",
        "ip": "10.0.3.1",
        "role": "cache",
        "cpu_percent": 20.1,
        "mem_percent": 92.3,
        "disk_percent": 15.0,
        "uptime_days": 60,
        "open_ports": [6379, 22],
        "tags": {"prod", "us-east-1"}
    },
    {
        "hostname": "worker-prod-01",
        "ip": "10.0.4.1",
        "role": "worker",
        "cpu_percent": 85.6,
        "mem_percent": 60.0,
        "disk_percent": 30.4,
        "uptime_days": 45,
        "open_ports": [22],
        "tags": {"prod", "eu-west-1"}
    },
    {
        "hostname": "worker-staging-01",
        "ip": "10.0.4.2",
        "role": "worker",
        "cpu_percent": 12.3,
        "mem_percent": 34.5,
        "disk_percent": 22.0,
        "uptime_days": 10,
        "open_ports": [22],
        "tags": {"staging", "eu-west-1"}
    },
    {
        "hostname": "cache-staging-01",
        "ip": "10.0.3.2",
        "role": "cache",
        "cpu_percent": 5.0,
        "mem_percent": 41.0,
        "disk_percent": 10.5,
        "uptime_days": 8,
        "open_ports": [6379, 22],
        "tags": {"staging", "us-east-1"}
    }
]


