import sys

def error_message_details(error):
    _, _, exc_tb = sys.exc_info()

    if exc_tb is None:
        return str(error)

    file_name = exc_tb.tb_frame.f_code.co_filename

    return (
        f"Error occurred in python script [{file_name}], "
        f"line number [{exc_tb.tb_lineno}], "
        f"error message [{error}]"
    )


class CustomException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message)

    def __str__(self):
        return self.error_message