if __name__ == "__main__":
    from tracer.store.log_reader import LogReader
    from tracer.config import get_log_file, LogDomain
    reader = LogReader(LogDomain.FS) 
    # for log in reader.reverse_iter():
    #     print(log)    

    reader.print_logs()