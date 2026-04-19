class Servers:
    def __init__(self,hostname,ip, role, cpu_percent, mem_percent, disk_percent, 
                 uptime_days, *open_ports, tags):
           
          if not isinstance(hostname, str):
              raise ValueError ("Hostname must be str")
          self.hostname = hostname
          if not isinstance(ip, str):
               raise ValueError ("IP must be str")
          self.ip = ip
          if not isinstance(role, str):
               raise ValueError ("Role must be str")
          self.role = role
          self.cpu_percent = cpu_percent
          self.mem_percent = mem_percent 
          self.disk_percent = disk_percent
          self.uptime_days = uptime_days
          self.open_ports = open_ports 
          self.tags = tags
    - Create a list of at least 8 server dictionaries, each containing: `hostname` (str), `ip` (str), 
    `role` (str — `"web"`, `"db"`, `"cache"`, `"worker"`), `cpu_percent` (float), 
    `mem_percent` (float), `disk_percent` (float), `uptime_days` (int), `open_ports` (list of ints),
    `tags` (set of strings like `{"prod", "us-east-1"}`)


        
        

#class ServerInventory:
