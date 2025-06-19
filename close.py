from dbFunc import cleanup_connections



def on_closing(root):
    cleanup_connections()
    root.quit()
    root.destroy()

def close_all():
    cleanup_connections()
    print("All connections closed and resources cleaned up.")
