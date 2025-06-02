from dbFunc import cleanup_connections
from tkinter import Tk


def on_closing(root):
    """Handle window closing event"""
    cleanup_connections()
    root.quit()
    root.destroy()

def close_all():
    """Close all connections and clean up resources"""
    cleanup_connections()
    print("All connections closed and resources cleaned up.")
