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
            fobiddencharacter = dict.fromkeys(map(ord, '/#\'&éÉàèÈ'), None)
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
            properties = ['status', 'ok', 'provider', 'location', 'address', 'accuracy']
            for i in range(len(properties)):
                if data['properties'][properties[i]] is not None:
                    if not isinstance(data['properties'][properties[i]], str):
                        propertiesstring += "," + properties[i] + ":" + str(data['properties'][properties[i]])
                    else:
                        if i==0:
                            propertiesstring += properties[i] + ":\'"+ data['properties'][properties[i]].translate(fobiddencharacter) + "\'"
                        else:
                            propertiesstring += "," + properties[i] + ":\'"+ data['properties'][properties[i]].translate(fobiddencharacter) + "\'"
                else:
                    if i==0:
                        propertiesstring +=  properties[i] + ":null"  
                    else:
                        propertiesstring += "," + properties[i] + ":null"  

            propertiesstring += "}"
            permitsstring = "{"
            permitstype = ['suffix', 'APPL_TYPE', 'BLG_TYPE', 'filename', 'ISSUED_DATE', 'VALUE_unit', 'FT2', 'TOTAL_unit', 'CONTRACTOR', 'PC', 'location', 'PERMIT', 'direction', 'VALUE', 'PLAN', 'FT2_unit', 'WARD', 'DU', 'COST_unit', 'DESCRIPTION', "keyword"]
            
            for i in range(len(permitstype)):
                if data['permits'][permitstype[i]] is not None:
                    if not isinstance(data['permits'][permitstype[i]], str):
                        permitsstring += "," + permitstype[i] + ":" + str(data['permits'][permitstype[i]])
                    else:
                        if i==0:
                            permitsstring += permitstype[i] + ":\'"+ data['permits'][permitstype[i]].translate(fobiddencharacter) + "\'"
                        else:
                            permitsstring += "," + permitstype[i] + ":\'"+ data['permits'][permitstype[i]].translate(fobiddencharacter) + "\'"
                else:
                    if i==0:
                        permitsstring += permitstype[i] + ":null"
                    else:
                        permitsstring += "," + permitstype[i] + ":null"  

            permitsstring += "}"
            o.write("INSERT INTO permit (id, geometry, properties, permits, housenumber, street, road, municipality, city, month, year, type) VALUES (")
            o.write(idstring + ",")
            o.write(geometrystring + ",")
            o.write(propertiesstring + ",")
            o.write(permitsstring + ",")
            o.write(str(data['housenumber'])+ ",")
            o.write("\'" + data['street']+ "\',")
            o.write("\'" + data['road'].translate(fobiddencharacter)+ "\',")
            o.write("\'" + data['municipality'].translate(fobiddencharacter)+ "\',")
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
o.write("CREATE TYPE IF NOT EXISTS geometrytype (type text, coordinates list<float>);\n")
o.write("CREATE TYPE IF NOT EXISTS propertiestype (status text, ok boolean, provider text, location text,address text, accuracy int);\n")
o.write("CREATE TYPE IF NOT EXISTS permitstype (suffix text, APPL_TYPE text, BLG_TYPE text, filename text, ISSUED_DATE date, VALUE_unit int, FT2 int, TOTAL_unit int, CONTRACTOR text, PC text, location text, PERMIT int, direction text, VALUE int, PLAN text, FT2_unit int, WARD text, DU int, COST_unit float, DESCRIPTION text, keyword text);\n")
#o.write("CREATE TABLE IF NOT EXISTS Permit (_id frozen idtype PRIMARY KEY,  geometry frozen geometrytype, properties frozen propertiestype, permits frozen permitstype, housenumber int, street text, road text, municipality text, city text, month text, year int, type text);\n")
o.write("CREATE TABLE IF NOT EXISTS Permit (id text PRIMARY KEY, geometry frozen <geometrytype>, properties frozen <propertiestype>, permits frozen <permitstype>, housenumber int, street text, road text, municipality text, city text, month text, year int, type text);\n")
p=Payload(j, o)
j.close()
o.close()