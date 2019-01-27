import json

class Payload(object):
    def __init__(self, j, o):
        self.nlines = len(j.readlines())
        j.seek(0)
        #data =[]
        for i in range(self.nlines):
            line = j.readline()
            data = json.loads(line)
            #data.append(json.loads(line))
            #idstring = 
            o.write("INSERT INTO Permit (_id, geometry, properties, permits, housenumber, street, road, municipality, city, month, year, type) VALUES (")
            o.write(");\n")
            

j=open('data.json', 'r')
o=open('export.cql', 'w')
o.write("CREATE KEYSPACE IF NOT EXISTS ottawa WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 3};\n")
o.write("USE ottawa;\n")
o.write("CREATE TYPE idtype ($oid text);\n")
o.write("CREATE TYPE geometrytype (type text, coordinates list<float>);\n")
o.write("CREATE TYPE propertiestype (status text, ok boolean, provider text, location text,address text, accuracy int);\n")
o.write("CREATE TYPE permitstype (suffix text, APPL_TYPE text, BLG_TYPE text, filename text, ISSUED_DATE date, VALUE_unit int, FT2 int, TOTAL_unit int, CONTRACTOR text, PC text, location text, PERMIT int, direction text, VALUE int, PLAN text, FT2_unit int, WARD text, DU int, COST_unit float, DESCRIPTION text, keyword text);\n")
o.write("CREATE TABLE IF NOT EXISTS Permit (_id frozen idtype PRIMARY KEY,  geometry frozen geometrytype, properties frozen propertiestype, permits frozen permitstype, housenumber int, street text, road text, municipality text, city text, month text, year int, type text);\n")
p=Payload(j, o)
j.close()
o.close()