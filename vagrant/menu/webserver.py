from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind = engine)
session = DBsession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Create a new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestaurantName" type="text" placeholder="New restaurant name"><input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                
                restaurant_id = self.path.split("/")[2]

                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" %restaurant.name
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name="restaurantName" type="text" placeholder="Restaurant name" value = "%s" ><input type="submit" value="Rename"> </form>''' %(restaurant.id,restaurant.name)
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/delete"):
                
                restaurant_id = self.path.split("/")[2]

                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?</h1>" %restaurant.name
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input type="submit" value="Delete"> </form>''' %(restaurant.id)
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Create a new restaurant</a>"
                for restaurant in restaurants:
                    output += "<p>%s</p>" %restaurant.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br/><a href='/restaurants/%s/delete'>Delete</a>" %(restaurant.id,restaurant.id)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestaurantName = fields.get('newRestaurantName')
                    newRestaurant = Restaurant(name = newRestaurantName[0])
                    session.add(newRestaurant)
                    session.commit()
                    print newRestaurantName[0], " added in DB"
                
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantId = self.path.split("/")[2]
                    restaurantName = fields.get('restaurantName')[0]
                    restaurant = session.query(Restaurant).filter_by(id=restaurantId).one()
                    
                    if restaurant != []:
                        restaurant.name = restaurantName
                        session.add(restaurant)
                        session.commit()
                        print " edited in DB"
                    
                        self.send_response(301)
                        self.send_header('Content-type','text/html')
                        self.send_header('Location','/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    restaurantId = self.path.split("/")[2]
                    restaurant = session.query(Restaurant).filter_by(id=restaurantId).one()
                    
                    if restaurant != []:
                        session.delete(restaurant)
                        session.commit()
                        print "deleted from DB"
                    
                        self.send_response(301)
                        self.send_header('Content-type','text/html')
                        self.send_header('Location','/restaurants')
                        self.end_headers()
        except Exception, e:
            print e


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()