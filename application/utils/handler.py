from flask import current_app
import sys
import logging
from sqlalchemy import exc
import gc

logging.basicConfig(
    stream=sys.stdout, 
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s - %(message)s',
)
env = current_app.config.get('ENV')

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    logging.error(*args)

class AppMessageException(Exception):
    pass

def exception_handler(e, res_code=500, default_data={}, message='something went wrong'):
    # print('err: ', sys.exc_info())
    # print('err: ', type(e).__name__)
    eprint(str(e))

    context = {
        'express21': {
            'status': {
                'message': message,
                'status_code': res_code
            },
            'results': {
                'data': default_data
            }
        }
    }

    err_msg = str(e)
    err_code = 1001

    try:
        raise e
    except exc.SQLAlchemyError:
        err_code = 3001
        if env == 'development':
            pass
        else:
            err_msg = 'something went wrong'
    except AppMessageException:
        err_code = 2001
    except:
        if env == 'development':
            pass
        else:
            err_msg = ''

    context['express21']['status']['error_message'] = err_msg
    context['express21']['status']['error_code'] = err_code

    gc.collect()

    return context

def success_handler(results, res_code=200, message='ok'):
    context = {
        'express21': {
            'status': {
                'message': message,
                'status_code': res_code,
                'error_message': 'no error',
                'error_code': -1
            },
            'results': results
        }
    }

    gc.collect()

    return context