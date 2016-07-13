import cherrypy
import mysql.connector
import os.path
import json

class table_loader(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Edid_test/public/html/index.html')
class Connection():
    def __init__(self,host,user,password,db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        
        self.Connection = mysql.connector.Connect(host = self.host , user = self.user , password = self.password , database = self.db)
        self.Cursor = self.Connection.cursor()
        print 'Database connected'
    
    def data_loader(self):
        query = 'select * from edid_semantics'
        self.Cursor.execute(query)
        result = self.Cursor.fetchall()
        self.Connection.commit()
        return result
    def header_loader(self):
        query = 'show columns from edid_semantics'
        print query
        self.Cursor.execute(query)
        result = [column[0] for column in self.Cursor.fetchall()]
        self.Connection.commit()
        return result
    
class Json():
    def header_json(self):
        pass
class Display_table():
    def __inti__(self , data):
        pass
        
if __name__=="__main__":
    conf = {
        '/':{
            'tools.staticdir.root':os.path.abspath(os.getcwd())
        },
        '/static':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir':'./public'
        }
    }
    cherrypy.config.update({'server.socket_port': 9090})
    print os.getcwd()
    webapp = table_loader()
    mysql = Connection('172.16.170.136','root','password123!','hdmi')
    table_data = mysql.data_loader()
    print table_data
    table_header = mysql.header_loader()
    print table_header
    display = Display_table()
    #cherrypy.quickstart(webapp,'/', conf)
#     cherrypy.tree.mount(webapp,'/', conf)
#     cherrypy.engine.start()
    
    
    