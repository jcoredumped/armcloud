# -*- coding: utf-8 -*-

'''
Created on 02/06/2013

@author: joan
'''

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db
from codeop import Compile

from google.appengine.ext.webapp import template
import os


 
class Programa(db.Model):
#     usuario = db.StringProperty(required=True)
#     programa = db.TextProperty(required=True)
#     titulo = db.StringListProperty(required=True)
    pass
 
class MainPage(webapp.RequestHandler):
     
    pass
         
     
     
     
#     def get(self):
#         self.user = users.get_current_user() # obtenemos el usuario en caso que no este logeado
#                                         # le mandamos a la pantalla de login
#  
#         if self.user: # si esta logeado 
#             pass
#         else:
#             self.redirect(users.create_login_url(self.request.uri))
#              
#              
#              
#  
#          
#          
#      
#                          
class NuevoPrograma(webapp.RequestHandler):
    pass
#     def get(self):
#         self.user = users.get_current_user()
#          
#         self.mostrarFormulario(self.user)
#          
#          
#     def post(self):
#         self.user = users.get_current_user()
#         if self.user: # si esta logeado
#             #self.response.out.write(self.request.get('programa').replace('\n', '<br />\n'))
#             # almacenamos en la bd
#              
#             programa = Programa()
#             #programa.usuario = self.user
#             programa.codigo = db.Text(self.request.get('programa'))
#             programa.put()  
#              
#              
#              
#         else:
#             self.redirect(users.create_login_url(self.request.uri))
#          
#          
#     def mostrarFormulario(self, usuario):
#         self.response.out.write(
#              
#         '''<html>
#             <head>
#                <title>Título
#                </title>
#             </head>
#            <body>
#                <div>
#                    <p>Estás logeado como %s</p>
#                </div>
#                <form method="post">
#                <div><textarea name="programa" rows="60" cols="60"></textarea></div>
#                <div>Nombre del Fichero
#                    <input type="text" name="nombreFichero"
#                </div>
#                 <div><input type="submit" value="Enviar programa"></div>
#                 
#                </form>
#            </body>
#            </html>
#         ''' 
#         %(usuario)
#                                 )
#          
 
class VerProgramas(webapp.RequestHandler):
    pass



class Ejecutar(webapp.RequestHandler):
    
    def get(self):
        #self.mostrarFormulario()
        temp = os.path.join(os.path.dirname(__file__), 'templates/execForm.html')
        titulo = "Traductor ARM"
        outstr = template.render(temp, {'titulo':titulo})
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(outstr)
        
        
        
        
    def post(self):
        
        import gramatica
        
        temp = os.path.join(os.path.dirname(__file__), 'templates/execResul.html')
        titulo = "Resultado de la simulacion"
        valueTemplate = {}
        valueTemplate['titulo'] = titulo
        codigoSalida = gramatica.traduccion(self.request.get("programa").replace("\r", ""))
        
        dicSalida={}
        try:
            exec codigoSalida   in dicSalida
            
            listaSalida = self.prepararResultado(dicSalida['registros'], dicSalida['memoria'])
            valueTemplate['registros'] = listaSalida[0]
            valueTemplate['memoria'] = listaSalida[1]
             

            outstr = template.render(temp, valueTemplate)
            self.response.write(outstr)
            
          #  self.response.write(listaSalida[0])
        except:
            #self.response.write(valueTemplate)
            print ""
        
        
                               
    
   
   
    def prepararResultado(self,registros, memoria):
        # imprimimos el diccionario de registros
        salidaReg=[]
        salidaMem=[]
        
        for i in range(32):
            salidaReg.append("r%d => %d" %(i, registros[i]))
    
        direcciones = memoria.keys()
        direcciones.sort() # las ordenamos
        for elemento in direcciones:
            salidaMem.append("0x%08x -> %d" % (elemento, memoria[elemento]))
        return [salidaReg,salidaMem]
   
   
   
   
        
    def imprimirResultado(self,registros, memoria):
        # imprimimos el diccionario de registros
        self.response.write("Registros: <br />")
        for i in range(32):
            self.response.write("\tr%d => %d<br />" %(i, registros[i]))
    
        self.response.write("<br />" * 2)
        self.response.write("Memoria: <br />")
        direcciones = memoria.keys()
        direcciones.sort() # las ordenamos
        for elemento in direcciones:
            self.response.write("\t0x%08x -> %d<br />" % (elemento, memoria[elemento]))
        


            


app = webapp.WSGIApplication([('/', MainPage), ('/new', NuevoPrograma), ('/view', VerProgramas), ('/exec', Ejecutar)],
                              debug=True
                              )

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
