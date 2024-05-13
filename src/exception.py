import sys

def error_message_details(error_message, error_detail:sys):
    __,__,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="error occured in python script name[{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,error_message)
    
    return error_message


class CustomException(Exception):
    def __init__(self, error_message:str, error_detail:sys):
        self.error_message=error_message_details(error_message, error_detail)
        super().__init__(self.error_message)
        
    def __str__(self):
        return self.error_message