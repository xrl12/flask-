import logging

from uuid import uuid1
from flask import url_for, redirect, request, flash, current_app
from flask_login.utils import current_user
from jinja2 import Markup
from flask_admin.babel import gettext
from sqlalchemy.orm.base import instance_state
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from app.admin.views import login
import os.path as op

file_path = op.join(op.dirname(__file__), '../static')  # 文件上传路径

log = logging.getLogger("flask-admin.sqla")


class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        print('-----------------------------fadsfasdfadsfasd')
        # return redirect(url_for('admin.login', next=request.url))
        return redirect(url_for('admin.index',next=request.url))
        # return redirect('http://127.0.0.1:5000/admin/login')


class UModelview(MyModelView):
    column_labels = {
        'id': '序号',
        'email': '邮件',
        'username': '用户名',
        'role': '角色',
        'password_hash': '密码',
        'head_img': '头像',
        'create_time': '创建时间',
        'update_time': '更新时间'
    }
    column_exclude_list = ['password_hash', ]

    def _list_thumbnail(view, context, model, name):
        if not model.head_img:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.head_img)))

    column_formatters = {
        'head_img': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'head_img': form.ImageUploadField('Image',
                                          base_path=file_path,
                                          relative_path="uploadfile/",
                                          thumbnail_size=(100, 100, True))
    }


class FModelview(MyModelView):
    column_labels = {
        'id': '序号',
        'summary': '描述',
        'stock': '库存量',
        'category': '分类',
    }

    def get_img(view, context, model, name):
        if not model.main_image:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=model.main_image))

    column_formatters = {
        'main_image': get_img
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'main_image': form.ImageUploadField('Image',
                                            base_path=file_path,
                                            relative_path="uploadfile/")
    }

    # 重写创建方法
    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            model = self._manager.new_instance()
            # TODO: We need a better way to create model instances and stay compatible with
            # SQLAlchemy __init__() behavior
            state = instance_state(model)
            self._manager.dispatch.init(state, [], {})
            try:
                image = form.main_image.data.filename
                img_format = image[image.rfind('.') + 1:]
                if img_format not in current_app.config['IMG_FORMAT']:
                    flash(gettext('图片不合法', error=str('图片不合法')), 'error')
                    self.session.rollback()
                    return False
                form.main_image.data.filename = str(uuid1()) + '.' + img_format
            except Exception as e:
                pass
            form.populate_obj(model)
            self.session.add(model)

            self._on_model_change(form, model, True)
            self.session.commit()

        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def on_model_change(self, form, model, is_created):
        print(form.main_image.data.filename)

    # 重写更新方法
    def update_model(self, form, model):
        """
            Update model from form.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        try:
            img = form.main_image.data.filename.split('.')[-1]
            form.main_image.data.filename = str(uuid1()) + '.' + img
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to update record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to update record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True
