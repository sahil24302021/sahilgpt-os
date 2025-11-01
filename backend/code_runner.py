import subprocess
import tempfile
import os

def run_code_safely(code: str) -> dict:
    """
    Runs Python code in a temporary file and captures the output.
    This provides a basic level of sandboxing.

    Args:
        code: A string containing the Python code to execute.

    Returns:
        A dictionary with "stdout", "stderr", and "returncode".
    """
    # Create a temporary file to write the code to
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            filepath = tmp_file.name
            tmp_file.write(code)
        
        # Execute the python script as a separate process with a timeout
        result = subprocess.run(
            ['python3', filepath],
            capture_output=True,
            text=True,
            timeout=15  # 15-second timeout to prevent infinite loops
        )
        
        # Clean up the temporary file
        os.remove(filepath)
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        os.remove(filepath) # Ensure cleanup even on timeout
        return {"stdout": "", "stderr": "Error: Code execution timed out after 15 seconds.", "returncode": -1}
    except Exception as e:
        # If the temp file was created, try to remove it
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return {"stdout": "", "stderr": f"An unexpected error occurred: {e}", "returncode": -1}