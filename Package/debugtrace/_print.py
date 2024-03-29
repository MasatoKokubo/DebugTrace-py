# print.py
# (C) 2020 Masato Kokubo
__author__  = 'Masato Kokubo <masatokokubo@gmail.com>'

def _print(message: str, file) -> None:
    """
    Outputs the message to the file.

    Args:
        message (str): The message to output
        file: Output destination
    """
    print(message, file=file, flush=True)
