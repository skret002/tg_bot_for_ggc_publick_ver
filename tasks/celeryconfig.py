imports = ("tasks.tasks_notis","tasks.change_settings","tasks.repons_support")
task_ignore_result = True
#BROKER_HOST = "127.0.0.1"
#BROKER_PORT = 6379
broker_url = "redis://127.0.0.22:6378/0"
worker_hijack_root_logger = False
broker_connection_retry_on_startup=True
accept_content = ['application/json']
result_accept_content = ['json']
result_accept_content = ['application/json']

# redis из докера