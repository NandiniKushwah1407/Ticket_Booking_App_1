import os
from flask import Flask, render_template, request, redirect, url_for, current_app, flash
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.secret_key='Nandini'

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+ os.path.join(current_dir, "database.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
app.app_context().push()

#------------------------- Models of the application -----------------------------

class Login(db.Model):
    __tablename__ = 'login'
    Email = db.Column(db.String(200), nullable=False)
    UserName = db.Column(db.String(500), primary_key=True)
    Password = db.Column(db.String(500), nullable=False)
    TicketR = db.relationship('Ticket', backref='login', lazy=True)

class City(db.Model):
    __tablename__ = 'city'
    StateName = db.Column(db.String(100), nullable=False)
    CityName = db.Column(db.String(100), primary_key=True)
    VenueR = db.relationship('Venue', backref='city', lazy=True)

class Venue(db.Model):
    __tablename__ = 'venue'
    VenueID = db.Column(db.String(50), primary_key=True)
    VenueName = db.Column(db.String(200), nullable=False)
    VenuePlace = db.Column(db.String(200), nullable=False)
    VenueCapacity = db.Column(db.Integer, nullable=False)
    ShowR = db.relationship('Show', backref='venue', lazy=True)
    TicketR = db.relationship('Ticket', backref='venue', lazy=True)
    CityName = db.Column(db.String(100), db.ForeignKey('city.CityName'), nullable=False)

class Show(db.Model):
    __tablename__ = 'show'
    ShowID = db.Column(db.String(50), primary_key=True)
    ShowName = db.Column(db.String(200), nullable=False)
    ShowRating = db.Column(db.Integer, nullable=True)
    ShowTag = db.Column(db.String(50), nullable=False)
    ShowLanguage = db.Column(db.String(50), nullable=False)
    ShowTime = db.Column(db.String(50), nullable=False)
    ShowPrice = db.Column(db.Integer, nullable=False)
    TicketR = db.relationship('Ticket', backref='show', lazy=True)
    VenueID = db.Column(db.String(50), db.ForeignKey('venue.VenueID'), nullable=False)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    sno = db.Column(db.Integer, primary_key= True)
    tno = db.Column(db.Integer)
    Booked = db.Column(db.Integer, default = 0)
    ShowID = db.Column(db.String(50), db.ForeignKey('show.ShowID'))
    Rate = db.Column(db.Integer, default = 0)
    UserName = db.Column(db.String(500), db.ForeignKey('login.UserName'), nullable=True)
    VenueID = db.Column(db.String(50), db.ForeignKey('venue.VenueID'))

class Update(db.Model):
    __tablename__ ='update'
    no = db.Column(db.Integer, primary_key = True)
    StateName = db.Column(db.String(100), nullable=True)
    CityName = db.Column(db.String(100), nullable=True)
    VenueID = db.Column(db.String(50), nullable= True)
    VenueName = db.Column(db.String(200), nullable= True)
    VenuePlace = db.Column(db.String(200), nullable= True)
    VenueCapacity = db.Column(db.Integer, nullable= True)
    ShowID = db.Column(db.String(50), nullable= True)
    ShowName = db.Column(db.String(200), nullable= True)
    ShowRating = db.Column(db.Integer, nullable=True)
    ShowTag = db.Column(db.String(50), nullable= True)
    ShowLanguage = db.Column(db.String(50), nullable= True)
    ShowTime = db.Column(db.String(50), nullable= True)
    ShowPrice = db.Column(db.Integer, nullable= True)
    sno = db.Column(db.Integer,nullable= True )
    tno = db.Column(db.Integer, nullable= True)
    Booked = db.Column(db.Integer, nullable = True)
    Email = db.Column(db.String(200), nullable= True)
    UserName = db.Column(db.String(500), nullable=True)
    Password = db.Column(db.String(500), nullable= True)

#------------------------- Controllers of the application -----------------------------

# For rendering index page and signup
@app.route('/', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        Email = request.form['email']
        UserName = request.form['username']
        Password = request.form['password']
        login = Login(Email = Email, UserName = UserName, Password= Password)
        db.session.add(login)
        db.session.commit()

        user = Login.query.filter_by(UserName=UserName).first()
        
        CityName= 'Gwalior'
        venue= Venue.query.filter_by(CityName=CityName).all()
        show=[]
        for v in venue:
            s = Show.query.filter_by(VenueID=v.VenueID).all()
            for i in s:
                show.append(i)
        return render_template('index.html', CityName=CityName, show=show, venue=venue, user=user)
    
    CityName= 'Gwalior'
    user=Login.query.filter_by(UserName="default").first()
    venue= Venue.query.filter_by(CityName=CityName).all()
    show=[]
    for v in venue:
        s = Show.query.filter_by(VenueID=v.VenueID).all()
        for i in s:
            show.append(i)
    return render_template('index.html', CityName=CityName, show=show, venue=venue, user=user)

# For login
@app.route('/login/<CityName>', methods=['GET','POST'])
def login(CityName):
    if request.method=='POST':
        UserName = request.form['username']
        Password = request.form['password']
        a = Login.query.filter_by(UserName='admin').first()
        if  a.UserName == UserName and a.Password == Password:
            allCity = City.query.all()
            return render_template('admin.html', allCity=allCity, user =a)
        else:
            CityName= CityName
            venue= Venue.query.filter_by(CityName=CityName).all()
            show=[]
            for v in venue:
                s = Show.query.filter_by(VenueID=v.VenueID).all()
                for i in s:
                    show.append(i)
            user= Login.query.filter_by(UserName=UserName).first()
            if user == None:
                user = Login.query.filter_by(UserName='default')
                flash("User Not Found, Please SignUp To Continue.")
                return render_template('index.html', CityName=CityName, show=show, venue=venue, user=user)

            elif user.UserName == UserName and user.Password == Password:
                return render_template('index.html', CityName=CityName, show=show, venue=venue, user=user)
            else:
                user = Login.query.filter_by(UserName='default')
                flash("UserName or Password is Incorrect, Please Try Again")
                return render_template('index.html', CityName=CityName, show=show, venue=venue, user=user)
        
    return render_template('index.html')

# For adding a city by admin
@app.route('/city', methods=['GET','POST'])
def city():
    if request.method=='POST':
        StateName = request.form['statename']
        CityName = request.form['cityname']
        city = City(StateName = StateName, CityName = CityName)
        db.session.add(city)
        db.session.commit()
        allCity = City.query.all()
        user = Login.query.filter_by(UserName='admin').first()

        flash("City Added Successfully")
        return render_template('admin.html', allCity=allCity, user=user)
    
    allCity = City.query.all()
    user = Login.query.filter_by(UserName='admin').first()
    CityName='Gwalior'
    return render_template('admin.html', allCity=allCity, user=user, CityName=CityName)
    
# For adding a venue by admin
@app.route('/venue/<CityName>', methods=['GET','POST'])
def venue(CityName):
    if request.method=='POST':
        CityName = request.form['cityname']
        VenueID = request.form['venueid']
        VenueName = request.form['venuename']
        VenuePlace = request.form['venueplace']
        VenueCapacity = request.form['venuecapacity']
        venue = Venue(VenueID = VenueID, VenueName = VenueName, VenuePlace = VenuePlace, VenueCapacity = VenueCapacity , CityName=CityName)
        db.session.add(venue)
        db.session.commit()

        City = Venue.query.filter_by(CityName=CityName).first()
        CityName = City.CityName

        flash("Venue Added Successfully")
        return redirect(current_app.url_for('venue', CityName= CityName))
    
    CityName = CityName
    City= Venue.query.filter_by(CityName=CityName).first()
    CityVenue = Venue.query.filter_by(CityName=CityName).all()
    user = Login.query.filter_by(UserName='admin').first()
    return render_template('venue.html', CityVenue=CityVenue, City = City, CityName=CityName, user=user)

# For adding a show by admin    
@app.route('/show/<VenueID>', methods=['GET','POST'])
def show(VenueID):
    if request.method=='POST':
        VenueID = request.form['venueid']
        ShowID = request.form['showid']
        ShowName = request.form['showname']
        ShowRating = request.form['showrating']
        ShowTag = request.form['showtag']
        ShowLanguage = request.form['showlanguage']
        ShowTime = request.form['showtime']
        ShowPrice = request.form['showprice']
        show = Show(ShowID = ShowID, ShowName = ShowName, ShowRating = ShowRating, ShowTag = ShowTag, ShowLanguage = ShowLanguage, ShowTime = ShowTime, ShowPrice = ShowPrice, VenueID=VenueID)
        db.session.add(show)
        db.session.commit()

        seats(ShowID)
        
        Venue = Show.query.filter_by(VenueID=VenueID).first()
        VenueID = Venue.VenueID

        flash("Show Added Successfully")
        return redirect(current_app.url_for('show', VenueID=VenueID))
    
    VenueID= VenueID
    user = Login.query.filter_by(UserName='admin').first()
    Venue = Show.query.filter_by(VenueID=VenueID).first()
    allShow = Show.query.filter_by(VenueID=VenueID).all()
    return render_template('show.html', Venue=Venue, allShow = allShow, VenueID=VenueID, user=user)

# For deleting a city    
@app.route('/deletecity/<CityName>', methods= ["GET", "POST"])
def city_delete(CityName):
        city = City.query.filter_by(CityName=CityName).first()
        venue = Venue.query.filter_by(CityName= CityName).all()
        shows = Show.query.all()
        tickets = Ticket.query.all()
        show = []
        ticket =[]
        for v in venue:
            for s in shows:
                if v.VenueID == s.VenueID:
                    show.append(s)

        for i in venue:
            for t in tickets:
                if i.VenueID == t.VenueID:
                    ticket.append(t)

        for d3 in ticket:
            db.session.delete(d3) 
            db.session.commit()    

        for d2 in show:
            db.session.delete(d2)
            db.session.commit()  
            
        for d1 in venue:
            db.session.delete(d1)
            db.session.commit()  

        db.session.delete(city)
        db.session.commit()

        flash("City Deleted Successfully")
        return redirect(current_app.url_for('city'))

# For deleting a venue
@app.route('/deletevenue/<VenueID>', methods= ["GET", "POST"])
def venue_delete(VenueID):
        venue = Venue.query.filter_by(VenueID = VenueID).first()
        shows = Show.query.filter_by(VenueID = VenueID).all()
        ticket = Ticket.query.filter_by(VenueID = VenueID).all()
        CityName = venue.CityName
        City = Venue.query.filter_by(CityName = CityName).first()

        for d3 in ticket:
            db.session.delete(d3) 
            db.session.commit()    

        for d2 in shows:
            db.session.delete(d2)
            db.session.commit()  

        db.session.delete(venue)
        db.session.commit()
        
        flash("Venue Deleted Successfully")
        return redirect(current_app.url_for('venue', CityName = City.CityName))

# For deleting a show
@app.route('/deleteshow/<ShowID>', methods= ["GET", "POST"])
def show_delete(ShowID):
        show = Show.query.filter_by(ShowID = ShowID).first()
        ticket = Ticket.query.filter_by(ShowID = ShowID).all()
        VenueID = show.VenueID
        Venue = Show.query.filter_by(VenueID=VenueID).first()
        for d3 in ticket:
            db.session.delete(d3) 
            db.session.commit()      

        db.session.delete(show)
        db.session.commit()
        
        flash("Show Deleted Successfully")
        return redirect(current_app.url_for('show', VenueID=Venue.VenueID))

# For updating a venue
@app.route('/updatevenue/<VenueID>', methods=['GET', 'POST'])
def venue_update(VenueID):
    if request.method=='POST':
        venue = Venue.query.filter_by(VenueID = VenueID).first()
        shows = Show.query.filter_by(VenueID = VenueID).all()
        ticket = Ticket.query.filter_by(VenueID = VenueID).all()
        CityName = venue.CityName
        City = Venue.query.filter_by(CityName = CityName).first()

        for s in shows:
            a = Update(ShowID = s.ShowID, ShowName = s.ShowName, ShowRating = s.ShowRating, ShowTag = s.ShowTag, ShowLanguage = s.ShowLanguage, ShowTime = s.ShowTime, ShowPrice = s.ShowPrice, VenueID=s.VenueID)
            db.session.add(a)
            db.session.commit()

        for t in ticket:
            a = Update(sno= t.sno, tno = t.tno, Booked= t.Booked, ShowID=t.ShowID, UserName= t.UserName, VenueID=t.VenueID)
            db.session.add(a)
            db.session.commit()

        for d3 in ticket:
            db.session.delete(d3)    
             
        for d2 in shows:
            db.session.delete(d2)

        db.session.delete(venue)
        db.session.commit()

        VenueID = request.form['venueid']
        VenueName = request.form['venuename']
        VenuePlace = request.form['venueplace']
        VenueCapacity = request.form['venuecapacity']

        updatedvenue = Venue(VenueID = VenueID, VenueName = VenueName, VenuePlace = VenuePlace, VenueCapacity = VenueCapacity , CityName=CityName)
        db.session.add(updatedvenue)
        db.session.commit()
        
        updated = Update.query.all()
        for u in updated:
            if u.ShowID != None and u.ShowName != None:
                s = Show(ShowID = u.ShowID, ShowName = u.ShowName, ShowRating = u.ShowRating, ShowTag = u.ShowTag, ShowLanguage = u.ShowLanguage, ShowTime = u.ShowTime, ShowPrice = u.ShowPrice, VenueID= VenueID)
                db.session.add(s)
            
            elif u.sno != None:
                t= Ticket(sno= u.sno, tno = u.tno, Booked=u.Booked, ShowID=u.ShowID, UserName= u.UserName, VenueID= VenueID)
                db.session.add(t)

            for u in updated:
                db.session.delete(u)
                db.session.commit()
        
        flash("Venue Updated Successfully")
        return redirect(current_app.url_for('venue', CityName = City.CityName))

    venue = Venue.query.filter_by(VenueID=VenueID).first()
    user = Login.query.filter_by(UserName='admin').first()
    return render_template('updatevenue.html', venue=venue, user=user)

# For updating a city
@app.route('/updatecity/<CityName>', methods=['GET', 'POST'])
def city_update(CityName):
    if request.method=='POST':
        city = City.query.filter_by(CityName = CityName).first()
        venue = Venue.query.filter_by(CityName = CityName).all()
        shows = Show.query.all()
        tickets = Ticket.query.all()
        show = []
        ticket =[]
        for v in venue:
            for s in shows:
                if v.VenueID == s.VenueID:
                    show.append(s)

        for i in venue:
            for t in tickets:
                if i.VenueID == t.VenueID:
                    ticket.append(t)

        for v in venue:
            a = Update(CityName= v.CityName, VenueID = v.VenueID, VenueName = v.VenueName, VenuePlace = v.VenuePlace, VenueCapacity = v.VenueCapacity)
            db.session.add(a)
            db.session.commit()

        for s in show:
            a = Update(ShowID = s.ShowID, ShowName = s.ShowName, ShowRating = s.ShowRating, ShowTag = s.ShowTag, ShowLanguage = s.ShowLanguage, ShowTime = s.ShowTime, ShowPrice = s.ShowPrice, VenueID=s.VenueID)
            db.session.add(a)
            db.session.commit()

        for t in ticket:
            a = Update(sno= t.sno, tno = t.tno, Booked= t.Booked, ShowID=t.ShowID, UserName= t.UserName, VenueID=t.VenueID)
            db.session.add(a)
            db.session.commit()

        for d3 in ticket:
            db.session.delete(d3)    
             
        for d2 in show:
            db.session.delete(d2)
            
        for d1 in venue:
            db.session.delete(d1) 

        db.session.delete(city)
        db.session.commit()

        StateName = request.form['statename']
        CityName = request.form['cityname']

        city = City(StateName=StateName, CityName= CityName)
        db.session.add(city)
        db.session.commit()

        updated = Update.query.all()
        for u in updated:
            if u.CityName != None and u.VenueID != None and u.VenueName != None:
                u.CityName = CityName
                v= Venue(CityName=CityName, VenueID= u.VenueID, VenueName= u.VenueName, VenuePlace=u.VenuePlace, VenueCapacity= u.VenueCapacity)
                db.session.add(v)
                db.session.commit()
                
            elif u.ShowID != None and u.ShowName != None:
                s = Show(ShowID = u.ShowID, ShowName = u.ShowName, ShowRating = u.ShowRating, ShowTag = u.ShowTag, ShowLanguage = u.ShowLanguage, ShowTime = u.ShowTime, ShowPrice = u.ShowPrice, VenueID= u.VenueID)
                db.session.add(s)
            
            elif u.sno != None:
                t= Ticket(sno= u.sno, tno = u.tno, Booked=u.Booked, ShowID=u.ShowID, UserName= u.UserName, VenueID= u.VenueID)
                db.session.add(t)

            for u in updated:
                db.session.delete(u)
                db.session.commit()
        
        flash("City Updated Successfully")

        return redirect(current_app.url_for('city'))

    city = City.query.filter_by(CityName=CityName).first()
    user = Login.query.filter_by(UserName='admin').first()
    return render_template('updatecity.html', city=city, user=user)

# For updating a show
@app.route('/updateshow/<ShowID>', methods=['GET', 'POST'])
def show_update(ShowID):
    if request.method=='POST':
        show = Show.query.filter_by(ShowID = ShowID).first()
        ticket = Ticket.query.filter_by(ShowID = ShowID).all()
        VenueID = show.VenueID
        Venue = Show.query.filter_by(VenueID=VenueID).first()

        for t in ticket:
            a = Update(sno= t.sno, tno = t.tno, Booked= t.Booked, ShowID=t.ShowID, UserName= t.UserName, VenueID=t.VenueID)
            db.session.add(a)
            db.session.commit()

        for d3 in ticket:
            db.session.delete(d3) 
            db.session.commit()      

        db.session.delete(show)
        db.session.commit()

        ShowID = request.form['showid']
        ShowName = request.form['showname']
        ShowRating = request.form['showrating']
        ShowTag = request.form['showtag']
        ShowLanguage = request.form['showlanguage']
        ShowTime = request.form['showtime']
        ShowPrice = request.form['showprice']

        s = Show(ShowID = ShowID, ShowName = ShowName, ShowRating = ShowRating, ShowTag = ShowTag, ShowLanguage = ShowLanguage, ShowTime = ShowTime, ShowPrice = ShowPrice, VenueID=VenueID)

        db.session.add(s)
        db.session.commit()

        updated = Update.query.all()
        for u in updated:
            if u.sno != None:
                t= Ticket(sno= u.sno, tno = u.tno, Booked=u.Booked, ShowID=ShowID, UserName= u.UserName, VenueID= u.VenueID)
                db.session.add(t)

            for u in updated:
                db.session.delete(u)
                db.session.commit()
        
        flash("Show Updated Successfully")
        return redirect(current_app.url_for('show', VenueID=Venue.VenueID))
    
    show = Show.query.filter_by(ShowID=ShowID).first()
    user = Login.query.filter_by(UserName='admin').first()
    return render_template('updateshow.html', show=show, user=user)

# This route is made for adding seats in 'ticket' table when a show is added
@app.route('/seats', methods=['GET', 'POST'])
def seats(ShowID):
    show = Show.query.filter_by(ShowID=ShowID).first()
    VenueID = show.VenueID
    venue = Venue.query.filter_by(VenueID=VenueID).first()
    capacity = int(venue.VenueCapacity)

    for i in range(capacity):
        tno=i+1
        ShowID=ShowID
        VenueID=VenueID
        t= Ticket(tno=tno, ShowID= ShowID, VenueID=VenueID,  Booked = 0, UserName= None)
        db.session.add(t)
        db.session.commit()

# For rendering seating of a show only when a valid user is logged in
@app.route('/seating/<ShowID>/<UserName>', methods=['GET', 'POST'])
def seating(ShowID, UserName):
    show = Show.query.filter_by(ShowID=ShowID).first()
    VenueID = show.VenueID
    venue = Venue.query.filter_by(VenueID=VenueID).first()
    CityName=venue.CityName
    ticket = Ticket.query.filter_by(ShowID=ShowID).all()
    capacity = int(venue.VenueCapacity)
    user = Login.query.filter_by(UserName = UserName).first()

    if UserName == 'default':
        CityName = venue.CityName
        venues= Venue.query.filter_by(CityName=CityName).all()
        shows=[]
        for v in venues:
            s = Show.query.filter_by(VenueID=v.VenueID).all()
            for i in s:
                shows.append(i)
        flash("Please Login To Proceed")
        return render_template('index.html', CityName=CityName, venue=venues, show= shows, user=user)
    else:
        return render_template('seating.html', capacity = capacity, show=show, venue=venue, CityName=CityName, ticket=ticket, user=user)

# For searching a city
@app.route('/cityname/<CityName>/<UserName>', methods=['GET', 'POST'])
def cityname(CityName, UserName):
    if request.method == 'POST':
        CityName = request.form['cityname']
        city = City.query.filter_by(CityName=CityName).first()
        if city == None:
            return "City Not Found"
        else:
            CityName= city.CityName
            return redirect(current_app.url_for('cityname', CityName=CityName, UserName=UserName))
    
    CityName=CityName
    user = Login.query.filter_by(UserName=UserName).first()
    venue= Venue.query.filter_by(CityName=CityName).all()
    show=[]
    for v in venue:
        s = Show.query.filter_by(VenueID=v.VenueID).all()
        for i in s:
            show.append(i)
    return render_template('index.html', CityName=CityName, show=show, venue=venue, user=user)

# For rendring all the shows for a perticular venue
@app.route('/venueshow/<UserName>/<VenueID>', methods=['GET', 'POST'])
def venueshow(VenueID,UserName):
    venue= Venue.query.filter_by(VenueID=VenueID).first()
    CityName = venue.CityName
    show= Show.query.filter_by(VenueID=VenueID).all()
    user = Login.query.filter_by(UserName=UserName).first()
    return render_template('venue_show.html', venue=venue, show=show, CityName=CityName, user=user)

# For searching venue, show using show name, venue name, show time, show tag, venue place
@app.route('/search/<CityName>/<UserName>', methods=['GET','POST'])
def search(CityName,UserName):
    if request.method == 'POST':
        st = request.form['st']
        city = City.query.filter_by(CityName=CityName).first()
        CityName = city.CityName
        return redirect(current_app.url_for('search2', CityName=CityName, st=st, UserName=UserName))

# For rendering the filtered search of above route
@app.route('/search/<CityName>/<UserName>/<st>')
def search2(CityName, st, UserName):
    st=st
    user = Login.query.filter_by(UserName=UserName).first()
    city = City.query.filter_by(CityName=CityName).first()
    CityName = city.CityName
    venue = Venue.query.filter_by(CityName=CityName).all()
    shows = Show.query.all()
    show=[]
    search=[]
    for v in venue:
        for s in shows:
            if v.VenueID == s.VenueID:
                show.append(s)

    for j in venue:
        if st == j.VenueName or st == j.VenuePlace:
            a= Venue.query.filter_by(VenueID=j.VenueID).first()
            search.append(a)
        
    for s in show:
        if st == s.ShowName or st == s.ShowTag or st == s.ShowTime:
            a= Show.query.filter_by(ShowID = s.ShowID).first()
            search.append(a)
    if search==[]:
        flash("No Record Found !! Seach for another movie..")
        return render_template('index.html', CityName=CityName, venue=venue, show= show, user=user)
    else:
        return render_template('search.html', CityName=CityName, search=search, user=user)

# For booking single or multiple tickets by a user
@app.route('/bookticket/<ShowID>/<UserName>', methods=['GET', 'POST'])
def bookticket(ShowID, UserName):
    if request.method == "POST":
        list = request.form.getlist("seatno")
        show= Show.query.filter_by(ShowID=ShowID).first()
        ShowID=show.ShowID
        user = Login.query.filter_by(UserName=UserName).first()
        UserName = user.UserName
        
        return redirect(current_app.url_for('userticket', ShowID=ShowID, list=list, UserName=UserName))

# For rendering booked page with details, user's ticket
@app.route('/userticket/<ShowID>/<UserName>/<list>', methods=['GET', 'POST'])
def userticket(ShowID, UserName, list):
    show=Show.query.filter_by(ShowID=ShowID).first()
    Tickets = Ticket.query.filter_by(ShowID=ShowID).all()
    VenueID = show.VenueID
    venue = Venue.query.filter_by(VenueID=VenueID).first()
    CityName= venue.CityName
    a= str(list)
    b=''
    for i in a:
        if i=="'" or i=="[" or i=="]" or i == " ":
            pass
        else:
            b+=i
    d= b.split(',')

    for l in d:
        for t in Tickets:
            if t.tno == int(l):
                t.UserName = UserName
                t.Booked =1
                db.session.commit()
    user = Login.query.filter_by(UserName=UserName).first()
    flash("Ticket Booked Successfully")
    return render_template('booked.html', user=user, d=d, show=show, venue=venue,CityName=CityName)

# For rating a show when ticket is booked
@app.route('/rate/<ShowID>/<UserName>/<d>', methods=['GET','POST'])
def rate(ShowID, UserName, d):
    if request.method == "POST":
        rate = str(request.form.getlist("rate"))[2:3]
        show= Show.query.filter_by(ShowID=ShowID).first()
        ShowID=show.ShowID
        user = Login.query.filter_by(UserName=UserName).first()
        UserName = user.UserName
        Tickets = Ticket.query.filter_by(ShowID=ShowID).all()
        b=''
        d2 = str(d)
        for i in d2:
            if i=="'" or i=="[" or i=="]" or i == " ":
                pass
            else:
                b+=i

        list2 = b.split(',')

        for l in list2:
            for t in Tickets:
                if t.tno == int(l):
                    t.Rate = int(rate)
                    db.session.commit()

        count=0
        sum=0
        for i in Tickets:
            if i.Booked == 1 and i.Rate>0:
                sum+= int(i.Rate)
                count+= 1
        
        if count != 0:
            average = sum/count
            average = round(average,2)
            show.ShowRating = average
            db.session.commit()

        flash("You have rated Successfully")

    user = Login.query.filter_by(UserName=UserName).first()
    VenueID = show.VenueID
    venue = Venue.query.filter_by(VenueID=VenueID).first()
    CityName= venue.CityName
    return render_template('booked.html', user=user, d=d, show=show, venue=venue,CityName=CityName)


if __name__ == "__main__":
    app.run(debug=True)

   