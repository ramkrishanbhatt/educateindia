def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    #my second comment
    session.forget()
    return service()
### end requires
def index():
    rows=db(db.t_schedule).select()
    return dict(rows=rows)

def error():
    return dict()

@auth.requires_login()
def create_schedule():
    form=crud.create(db.t_schedule,
                     next='view_schedule/[id]')
    return dict(form=form)

#@auth.requires_login()
def view_schedule():
    record = db.t_schedule(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_schedule,record)
    return dict(form=form)

@auth.requires_login()
def schedule_search():
    form, rows=crud.search(db.t_schedule,query=db.t_schedule.active==True)
    return dict(form=form, rows=rows)

def inform_us():
    form=crud.create(db.t_inform)
    if form.accepts(request,session):
        response.flash='Submitted Successfully'
    return dict(form=form)

def about_us():
    return dict()

def s_exp():
    pages = db().select(db.page.id, db.page.title, orderby=db.page.title)
    return dict(pages=pages)
    
@auth.requires_login()
def create():
    "Give your view"
    form = crud.create(db.page, next = URL(r=request, f='index'))
    return dict(form=form)
    
def show():
    "shows a page"
    thispage = db.page[request.args(0)]
    if not thispage:
        redirect(URL(r=request, f='index'))
    db.comment.page_id.default = thispage.id
    if auth.user_id:
        form = crud.create(db.comment)
    else:
        form = 'To post comments please login'
    pagecomments = db(db.comment.page_id==thispage.id).select()
    return dict(page=thispage, comments=pagecomments, form=form)
    
@auth.requires_login()
def donate():
    for row in db(db.auth_user.email==auth.user.email).select(db.auth_user.first_name):
       loginname=row.first_name 
    form=crud.create(db.donation)
    form.vars.donor_name = loginname
    form.vars.donation_date = request.now.date()
    if form.accepts(request.vars, session):response.flash="Thank You For Your Help"
    return dict(form=form)

def informer():
        sc = request.now.date()
        informs = db(db.t_inform.informed_on==sc).select(db.t_inform.id, db.t_inform.name, db.t_inform.address, db.t_inform.contact, orderby=db.t_inform.name)
        return dict(informs=informs)

@auth.requires_login()        
def attend():
    for row in db(db.auth_user.email==auth.user.email).select(db.auth_user.area, db.auth_user.language, db.auth_user.city, db.auth_user.state):
       area = row.area
       city = row.city
       state = row.state
       language = row.language    
       sc = request.now.date()
       informs = db(((db.t_schedule.area==area) & (db.t_schedule.city==city) & (db.t_schedule.state==state)) | (db.t_schedule.schedule_date==sc)).select(db.t_schedule.id, db.t_schedule.area, db.t_schedule.city, db.t_schedule.language, orderby=db.t_schedule.area)
    return dict(informs=informs)
