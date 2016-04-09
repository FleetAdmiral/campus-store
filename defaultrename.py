@auth.requires_login()
def index():
    if db().select(orderby=~db.page.id).first() is not None:
        start=db().select(orderby=~db.page.id).first().id
        newa=request.args(0) or (start+1)
        lol=db(db.page.id<newa).select(orderby=~db.page.id)
	return dict(lol=lol)

@auth.requires_login()
def create():
	form = SQLFORM(db.page).process(next=URL('index'))
	return dict(form=form)

@auth.requires_login()
def show():
    this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
    db.post.page_id.default = this_page.id
    form = SQLFORM(db.post).process() if auth.user else None
    pagecomments = db(db.post.page_id==this_page.id).select()
    return dict(page=this_page, comments=pagecomments, form=form)

@auth.requires_login()
def edit():
	this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
	form = SQLFORM(db.page, this_page).process(
	    next = URL('show',args=request.args))
	return dict(form=form)

@auth.requires_login()
def documents():
	page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
	db.document.page_id.default = page.id
	db.document.page_id.writable = False
	grid = SQLFORM.grid(db.document.page_id==page.id,args=[page.id])
	return dict(page=page, grid=grid)
@auth.requires_login()
def like():
    vart=db.page(request.args(0,cast=int)) or redirect(URL('index'))
    db.count.insert(name_id=auth.user.id,page_id=vart.id)
    redirect(URL('show',args=vart.id))
@auth.requires_login()
def unlike():
    vart=db.page(request.args(0,cast=int)) or redirect(URL('index'))
    db(db.count.name_id==auth.user.id and db.count.page_id==vart.id).delete()
    redirect(URL('show',args=vart.id))
@auth.requires_login()
def myrecipe():
        form=db(db.page.created_by==auth.user_id).select()
        return dict(form=form)
def user():
	return dict(form=auth())

def download():
	return response.download(request, db)

def search():
	return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
	_onkeyup="ajax('callback', ['keyword'], 'target');")),
	target_div=DIV(_id='target'))

def callback():
	query = db.page.title.contains(request.vars.keyword)
	pages = db(query).select(orderby=db.page.title)
	links = [A(p.title, _href=URL('show',args=p.id)) for p in pages]
	return UL(*links)
