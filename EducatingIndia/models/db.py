from gluon.storage import Storage
settings = Storage()
settings.title = 'GyaanPushpa'
settings.subtitle = 'Ek saakaar Bharat ka sapna'
settings.database_uri = 'sqlite://storage.sqlite'
settings.email_server = 'smtp.gmail.com:587' #localhost
settings.email_sender = 'coniosam@gmail.com'
settings.email_login = 'coniosam:sanjeevsajjan12<>?'
settings.login_method = 'local'
settings.login_config = ''
#here i am making sample comment 
if  not request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('sqlite://storage.sqlite')    
else:                                         # else use a normal relational database
    db = DAL('google:datastore')                           # connect to Google BigTable
    session.connect(request, response, db = db)
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'coniosam@gmail.com'         # your email
mail.settings.login = 'coniosam:sanjeevsajjan12<>?'      # your credentials or None
auth.settings.hmac_key = 'sha512:d7c965e8-0685-477a-baae-087e7372943f'   # before define_tables()

db.define_table('auth_user',
    Field('id','id',
          represent=lambda id:SPAN(id,' ',A('view',_href=URL('auth_user_read',args=id)))),
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('phone',type='integer',default='',label=T('Contact Number')),      
    Field('language',type='string',default='',label=T('Language Preferred')),          
    Field('area',type='string',default='',label=T('Area')),      
    Field('city',type='string',default='',label=T('City')),              
    Field('state',type='string',default='',label=T('State')),          
    Field('zip',type='integer',default='',label=T('Zip')),          
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    format='%(username)s')

db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
auth.define_tables(migrate=settings.migrate)                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'http://www.gmail.com'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'coniosam@gmail.com'
mail.settings.login = 'coniosam:sanjeevsajjan12<>?'

db.define_table('t_schedule',
    Field('id','id',
          represent=lambda id:SPAN(id,' ',A('view',_href=URL('view_schedule',args=id)))),
    Field('schedule_date', type='datetime',notnull= True),
    Field('language', default='',label=T('Language Preferred')),
    Field('area', default='',label=T('Area')),
    Field('city', default='',label=T('City')),
    Field('state', default='',label=T('State')),
    Field('zip', default='',label=T('Zip code')),
    Field('active','boolean',default=True,
          label=T('Active'),writable=False,readable=False),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False))

db.define_table('t_inform',
    Field('name', type='string',
          label=T('Name')),
    Field('address',
          label=T('Address')),
    Field('contact', type='string',
          label=T('Contact number')),
    Field('informed_on','date',default=request.now,
          label=T('Informed On'),writable=False,readable=False))
db.t_inform.name.requires = IS_NOT_EMPTY()
db.t_inform.address.requires = IS_NOT_EMPTY()
db.t_inform.contact.requires = IS_NOT_EMPTY() 

db.define_table('donation',
    Field('donor_name',notnull=False,writable=False, readable=False),
    Field('donation_date',notnull=False,writable=False,readable=False),
    Field('donation_item',notnull=False),
    Field('donation_amount'),
    Field('donated_to',notnull=False),
    Field('donated_by',db.auth_user,default=auth.user_id,
          label=T('Donated By'),writable=False))

db.donation.donor_name.requires = IS_NOT_EMPTY()
db.donation.donation_item.requires = IS_NOT_EMPTY()

db.define_table('page',
    Field('title'),
    Field('experience','text'),
    Field('created_on','datetime',default=request.now,writable = False),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False))
    
db.define_table('comment',
    Field('page_id',db.page),
    Field('experience','text',label=T('')),
    Field('created_on', 'datetime', default=request.now,writable=False, readable=False),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False,readable=False))
    
db.page.title.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'page.title')]
db.page.experience.requires = IS_NOT_EMPTY()

db.comment.page_id.requires = IS_IN_DB(db, 'page.id','%(title)s')
db.comment.experience.requires = IS_NOT_EMPTY()
db.comment.page_id.readable = False
db.comment.page_id.writable = False
