class ReadOnlyAdminMixin(object):
    extra = 0
    max_num = 0
    can_delete = False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
