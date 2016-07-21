import cherrypy
import mysql.connector
import os.path
import json
from timeit import itertools

class table_loader(object):
    @cherrypy.expose
    def index(self):
        return open('/home/development/workspace/Edid_test/index.html')
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
        #query = 'select concat("[", group_concat( concat("{id:'",id,"'"),concat(",prd_manufacturer_name:'",prd_manufacturer_name,"'"),concat(",prd_code:'",prd_code,"'"),concat(",prd_serial_no:'",prd_serial_no,"'"),concat(",prd_week_of_manufacture:'",prd_week_of_manufacture,"'"),concat(",prd_year_of_manufacture:'",prd_year_of_manufacture,"'"),concat(",str_version_no:'",str_version_no,"'"),concat(",str_revision_no:'",str_revision_no,"'"),concat(",monitor_name_tag:'",monitor_name_tag,"'}")),"]") as json from edid_semantics'
        query = 'select * from edid_semantics'
        print 'query:' + query
        self.Cursor.execute(query)
        desc = self.Cursor.description
        return [dict(itertools.izip([col[0] for col in desc], row))
                for row in self.Cursor.fetchall()]
    def header_loader(self):
        query = 'show columns from edid_semantics'
        self.Cursor.execute(query)
        result = [column[0] for column in self.Cursor.fetchall()]
        self.Connection.commit()
        return result
    
class Json():
    def json_loader(self, table_header , table_data):
        with open('data.json' , 'w') as outfile:
            json.dump(table_data, outfile)
        
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
    print table_data
    table_header = mysql.header_loader()
    Format_json = Json()
    output = Format_json.json_loader(table_header, table_data)

#     cherrypy.config.update({'server.socket_port': 9090})
#     cherrypy.server.socket_host = '172.16.170.175'
#     cherrypy.quickstart(webapp,'/', conf)
#     cherrypy.tree.mount(webapp,'/', conf)
#     cherrypy.engine.start()
    
    
    