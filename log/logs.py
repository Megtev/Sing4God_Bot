log_file = ''

def init_log_file(file_log_name):                   # Initialize log_file
    global log_file
    log_file = open(file_log_name, mode='w', encoding='utf-8')