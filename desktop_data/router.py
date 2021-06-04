class CheckerRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'desktop':
            return 'desktop'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'desktop':
            return 'desktop'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ['desktop', 'default']
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True