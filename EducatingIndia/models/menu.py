response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
    (T('Home'),URL('index')==URL(),URL('index'),[]),
    (T('Inform Us'),URL('inform_us')==URL(),URL('inform_us'),[]),
    (T('Feedback'),URL('s_exp')==URL(),URL('s_exp'),[]), 
    (T('Search schedule'),URL('schedule_search')==URL(),URL('schedule_search'),[]),
    (T('About Us'),URL('about_us')==URL(),URL('about_us'),[])   

]
