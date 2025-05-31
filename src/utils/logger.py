import logging
import inspect
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')

def log(message):
    # Get the caller's stack frame
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    
    # Correctly get timestamp using datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    filename = os.path.basename(frame.filename)
    module_name = module.__name__ if module else 'UnknownModule'
    class_name = None
    if 'self' in frame[0].f_locals:
        class_name = frame[0].f_locals['self'].__class__.__name__
    function_name = frame.function
    
    # Ensure message is string
    msg = str(message)
    
    # Build log parts
    parts = [
        f"[{timestamp}]",
        f"File: {filename}",
        f"Module: {module_name}",
        f"{'Class: ' + class_name if class_name else ''}",
        f"Function: {function_name}",
        f"Message: {msg}"
    ]
    
    # Filter empty parts and join nicely
    log_message = " | ".join(part for part in parts if part)
    
    logging.info(log_message)
