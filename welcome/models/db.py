db = DAL('sqlite://storage.sqlite')

from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('object',
		Field('obj_name'),
		Field('body','text'),
		Field('image','upload'),
		Field('created_on','datetime',default=request.now),
		Field('created_by','reference auth_user', default=auth.user_id),
		format='%(title)s')
db.define_table('comment',
		Field('page_id','reference page'),
		Field('body','text'),
		Field('created_on','datetime',default=request.now),
		Field('created_by','reference auth_user',default=auth.user_id)
		)

