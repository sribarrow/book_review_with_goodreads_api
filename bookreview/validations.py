from email_validator import validate_email, EmailNotValidError
dict={'value':'', 'error':''}
def validate_email(email):
    try:
        # Validate.
        valid = validate_email(email)
        dict['value']=valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        dict['error']='Invalid Email'
    return dict

def validate_passwd(pwd, cpwd):
    if pwd == cpwd:
        


    
