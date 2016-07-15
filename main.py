import cherrypy
import numpy
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
        self.Cursor.execute(query)
        result = [column[0] for column in self.Cursor.fetchall()]
        self.Connection.commit()
        return result
    
class Json():
    def json_loader(self, table_header , table_data):
        data = numpy.array(table_data)
        b = json.dumps(table_data)
        print b 
        print len(data)
        with open('data.json' , 'w') as outfile:
            json.dump("[",outfile,indent=1)
            for a in range(0,len(data)):
                for i in range(0,9):
                    json.dump('"'+table_header[i]+'"'+':'+'"'+data[a,i]+'"', outfile)
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
    webapp = table_loader()
    mysql = Connection('172.16.170.136','root','password123!','hdmi')
    table_data = mysql.data_loader()
    table_header = mysql.header_loader()
    print "table header :" 
    print table_header
    print "table data :" 
    print table_data
    Format_json = Json()
    output = Format_json.json_loader(table_header, table_data)
    display = Display_table()
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.server.socket_host = '172.16.170.164'
    cherrypy.quickstart(webapp,'/', conf)
#     cherrypy.tree.mount(webapp,'/', conf)
#     cherrypy.engine.start()
    
    
    