from inspect import getargspec

def _cfg(f):
    if not hasattr(f, 'pecan'): f.pecan = {}
    return f.pecan


def expose(template      = None, 
           content_type  = 'text/html', 
           schema        = None, 
           json_schema   = None, 
           error_handler = None):
    
    if template == 'json': content_type = 'application/json'
    def decorate(f):
        # flag the method as exposed
        f.exposed = True
        
        # set a "pecan" attribute, where we will store details
        cfg = _cfg(f)
        cfg['content_type'] = content_type
        cfg.setdefault('template', []).append(template)
        cfg.setdefault('content_types', {})[content_type] = template
        
        # store the arguments for this controller method
        cfg['argspec'] = getargspec(f)
        
        # store the validator
        cfg['error_handler'] = error_handler
        if schema is not None: 
            cfg['schema'] = schema
            cfg['validate_json'] = False
        elif json_schema is not None: 
            cfg['schema'] = json_schema
            cfg['validate_json'] = True
        return f
    return decorate