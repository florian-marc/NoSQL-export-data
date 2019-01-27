import json

class Payload(object):
    def __init__(self, j, o):
        self.nlines = len(j.readlines())
        j.seek(0)
        #data =[]
        #for i in range(3):
        for i in range(self.nlines):
            line = j.readline()
            data = json.loads(line)
            #print(data)
            #data.append(json.loads(line))
            #idstring ="{\'$oid\':\'" + data['_id']['$oid'] + "\'}"
            idstring = "\'" + data['_id']['$oid'] + "\'"
            geometrystring = ""
            if not data['geometry']['coordinates']:
                geometrystring = "{type:\'" +data['geometry']['type'] + "\',coordinates:[]}"
            else:
                geometrystring = "{type:\'" +data['geometry']['type'] + "\',coordinates:[" + str(data['geometry']['coordinates'][0]) + ","+ str(data['geometry']['coordinates'][1]) + "]}"
            propertiesstring = "{"
            if data['properties']['status'] is None:
                propertiesstring += "status:null"
            else:
                propertiesstring += "status:\'" + data['properties']['status']+ "\'"
            if data['properties']['ok'] is None:
                propertiesstring += ",ok:null"
            else:
                propertiesstring += ",ok:" + str(data['properties']['ok'])
            if data['properties']['provider'] is None:
                propertiesstring += ",provider:null"
            else:
                propertiesstring += ",provider:\'" + data['properties']['provider']+ "\'"
            if data['properties']['location'] is None:
                propertiesstring += ",location:null"
            else:
                propertiesstring += ",location:\'" + data['properties']['location']+ "\'"
            if data['properties']['address'] is None:
                propertiesstring += ",address:null"
            else:
                propertiesstring += ",address:\'" + data['properties']['address']+ "\'"
            if data['properties']['accuracy'] is None:
                propertiesstring += ",accuracy:null"
            else:
                propertiesstring += ",accuracy:" + str(data['properties']['accuracy'])
            propertiesstring += "}"
            permitsstring = "{"
            if data['permits']['suffix'] is None:
                permitsstring += "suffix:null" 
            else:
                permitsstring += "suffix:\'" + data['permits']['suffix']  + "\'"
            if data['permits']['APPL_TYPE']  is None:
                permitsstring += ",APPL_TYPE:null"
            else:
                permitsstring += ",APPL_TYPE:\'" + data['permits']['APPL_TYPE'] + "\'"
            if data['permits']['BLG_TYPE'] is None:
                permitsstring += ",BLG_TYPE:null"
            else:
                permitsstring += ",BLG_TYPE:\'" + data['permits']['BLG_TYPE'] + "\'"
            if data['permits']['filename'] is None:
                permitsstring += ",filename:null" 
            else:
                permitsstring += ",filename:\'" + data['permits']['filename'] + "\'"
            if data['permits']['ISSUED_DATE'] is None:
                permitsstring += ",ISSUED_DATE:null"
            else:
                permitsstring += ",ISSUED_DATE:\'" + data['permits']['ISSUED_DATE'] + "\'"
            if data['permits']['VALUE_unit'] is None:
                permitsstring += ",VALUE_unit:null"
            else:
                permitsstring += ",VALUE_unit:" + str(data['permits']['VALUE_unit']) 
            if data['permits']['FT2'] is None:
                permitsstring += ",FT2:null"
            else:
                permitsstring += ",FT2:" + str(data['permits']['FT2']) 
            if data['permits']['TOTAL_unit'] is None:
                permitsstring += ",TOTAL_unit:null"
            else:
                permitsstring += ",TOTAL_unit:" + str(data['permits']['TOTAL_unit']) 
            if data['permits']['CONTRACTOR']  is None:
                permitsstring += ",CONTRACTOR:null"
            else:
                permitsstring += ",CONTRACTOR:\'" + data['permits']['CONTRACTOR'] + "\'"
            if data['permits']['PC']  is None:
                permitsstring += ",PC:null" 
            else:
                permitsstring += ",PC:\'" + data['permits']['PC'] + "\'"
            if data['permits']['location'] is None:
                permitsstring += ",location:null"
            else:
                permitsstring += ",location:\'" + data['permits']['location'] + "\'"
            if data['permits']['PERMIT'] is None:
                permitsstring += ",PERMIT:null"
            else:
                permitsstring += ",PERMIT:" + str(data['permits']['PERMIT']) 
            if data['permits']['direction'] is None:
                permitsstring += ",direction:null"
            else:
                permitsstring += ",direction:" + str(data['permits']['direction']) 
            if data['permits']['VALUE'] is None:
                permitsstring += ",VALUE:null" 
            else:
                permitsstring += ",VALUE:" + str(data['permits']['VALUE']) 
            if data['permits']['PLAN'] is None:
                permitsstring += ",PLAN:null" 
            else:
                permitsstring += ",PLAN:\'" + data['permits']['PLAN'] + "\'"
            if data['permits']['FT2_unit'] is None:
                permitsstring += ",FT2_unit:null"
            else:
                permitsstring += ",FT2_unit:" + str(data['permits']['FT2_unit']) 
            if data['permits']['WARD'] is None:
                permitsstring += ",WARD:null"
            else:
                permitsstring += ",WARD:\'" + data['permits']['WARD'] + "\'"
            if data['permits']['DU'] is None:
                permitsstring += ",DU:null"
            else:
                permitsstring += ",DU:" + str(data['permits']['DU']) 
            if data['permits']['COST_unit'] is None:
                permitsstring += ",COST_unit:null"
            else:
                permitsstring += ",COST_unit:" + str(data['permits']['COST_unit']) 
            if data['permits']['DESCRIPTION'] is None:
                permitsstring += ",DESCRIPTION:null"
            else:
                permitsstring += ",DESCRIPTION:\'" + data['permits']['DESCRIPTION'] + "\'"
            if data['permits']['keyword'] is None:
                permitsstring += ",keyword:null"
            else:
                permitsstring += ",keyword:\'" + data['permits']['keyword'] + "\'"
            permitsstring += "}"
            o.write("INSERT INTO Permit (id, geometry, properties, permits, housenumber, street, road, municipality, city, month, year, type) VALUES (")
            o.write(idstring + ",")
            o.write(geometrystring + ",")
            o.write(propertiesstring + ",")
            o.write(permitsstring + ",")
            o.write(str(data['housenumber'])+ ",")
            o.write("\'" + data['street']+ "\',")
            o.write("\'" + data['road']+ "\',")
            o.write("\'" + data['municipality']+ "\',")
            o.write("\'" + data['city']+ "\',")
            o.write("\'" + data['month']+ "\',")
            o.write(str(data['year'])+ ",")
            o.write("\'" + data['type'] + "\'")
            o.write(");\n")
            

j=open('data.json', 'r')
o=open('export.cql', 'w')
o.write("CREATE KEYSPACE IF NOT EXISTS ottawa WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 3};\n")
o.write("USE ottawa;\n")
#o.write("CREATE TYPE idtype ($oid text);\n")
o.write("CREATE TYPE geometrytype (type text, coordinates list<float>);\n")
o.write("CREATE TYPE propertiestype (status text, ok boolean, provider text, location text,address text, accuracy int);\n")
o.write("CREATE TYPE permitstype (suffix text, APPL_TYPE text, BLG_TYPE text, filename text, ISSUED_DATE date, VALUE_unit int, FT2 int, TOTAL_unit int, CONTRACTOR text, PC text, location text, PERMIT int, direction text, VALUE int, PLAN text, FT2_unit int, WARD text, DU int, COST_unit float, DESCRIPTION text, keyword text);\n")
#o.write("CREATE TABLE IF NOT EXISTS Permit (_id frozen idtype PRIMARY KEY,  geometry frozen geometrytype, properties frozen propertiestype, permits frozen permitstype, housenumber int, street text, road text, municipality text, city text, month text, year int, type text);\n")
o.write("CREATE TABLE IF NOT EXISTS Permit (id text PRIMARY KEY, geometry frozen geometrytype, properties frozen propertiestype, permits frozen permitstype, housenumber int, street text, road text, municipality text, city text, month text, year int, type text);\n")
p=Payload(j, o)
j.close()
o.close()