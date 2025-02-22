class EcommerceRouter:
    """
    Điều hướng cơ sở dữ liệu cho dự án Django sử dụng nhiều database.
    """
    route_app_labels = {
        'customers': 'mysql_db',
        'items': 'mongo_db',
        'orders': 'default'
    }

    def db_for_read(self, model, **hints):
        """Xác định database sử dụng để đọc dữ liệu"""
        return self.route_app_labels.get(model._meta.app_label, 'default')

    def db_for_write(self, model, **hints):
        """Xác định database sử dụng để ghi dữ liệu"""
        return self.route_app_labels.get(model._meta.app_label, 'default')

    def allow_relation(self, obj1, obj2, **hints):
        """Cho phép quan hệ giữa các model trong cùng một database"""
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Xác định database nào sẽ nhận migrations"""
        if app_label in self.route_app_labels:
            return db == self.route_app_labels[app_label]
        return db == 'default'