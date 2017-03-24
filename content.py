from helpers import *

def get_content( id, vars={} ):  
  template_path = "/layouts/" + id + ".html"
  if id == 'home':
    return(render_template("/layouts/home.html", username=get_user_name())) 
  else:
    return(render_template("/layouts/" + id + ".html"))
#  elif id == 'core':
#    return(render_template("/layouts/core.html")) 
#  elif id == 'layout':
#    return(render_template("/layouts/layout.html"))
#  elif id == 'elements':
#    return(render_template("/layouts/elements.html"))
#  elif id == 'tables':
#    return(render_template("/layouts/tables.html")) 
#  elif id == 'navigation':  
#    return(render_template("/layouts/navigation.html"))
#  elif id == 'indicators':
#    return(render_template("/layouts/indicators.html"))
#  elif id == 'containers':
#    return(render_template("/layouts/containers.html"))  
#  elif id == 'dialogs':
#    return(render_template("/layouts/dialogs.html"))   
#  elif id == 'configuration':
#    return(render_template("/layouts/configuration.html"))    
#  else:
#    return(render_template("/layouts/default.html"))
