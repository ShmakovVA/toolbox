# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from monkey_contrib.options import MonkeyModelAdmin

try:
    from sportamor.user.models import User

    TEMPLATE = 'permission_handler.html'
except ImportError:
    from django.contrib.auth.models import User

    TEMPLATE = 'permission_handler_swms.html'


class PermissionAdmin(MonkeyModelAdmin):
    model = Permission
    search_fields = ('name', 'content_type__model', 'content_type__app_label')

    def search_perms(self, request, search_term):
        searched_perms = self.get_search_results(
            request, self.model.objects.all(), search_term
        )
        return searched_perms[0]


class UserWithPermissionManagerAdmin(MonkeyModelAdmin):
    def get_urls(self):
        urls = super(UserWithPermissionManagerAdmin, self).get_urls()
        my_urls = [
            url(r'permissonhandler/$',
                self.admin_site.admin_view(self.permissionhandler),
                name='permission_handler'
                ),
            url(r'remove_permission/$',
                self.admin_site.admin_view(self.remove_permission),
                name='remove_permission'
                )
        ]
        return my_urls + urls

    def permissionhandler(self, request):
        """
        One stop shop, for viewing the eco-system of perms, users and groups.
        takes  four different args to base the view on;
            user, group, permission-search and permission-id

        Primarily used to get an overview rather than interacting, apart from
        the possibility to remove duplicated perms per user.
        :param request:
        :return:
        """
        if not request.user.has_perm('core.can_change_adminuser'):
            return HttpResponseForbidden()
        user_id = request.GET.get('user', None)
        group_id = request.GET.get('group', None)
        perm_id = request.GET.get('permission', None)
        perm_search = request.GET.get('perm_search', "")

        all_perms = Permission.objects.all()
        groups = Group.objects.exclude(pk=2).order_by('name')

        selected_user = selected_perm_users = selected_perm_group_users = \
            User.objects.none()
        selected_group = selected_perm_groups = selected_user_groups = \
            Group.objects.none()
        no_perms = Permission.objects.none()
        selected_perm = group_perms = searched_perms = no_perms
        group_users = None
        user_perms = []
        user_group_perms = None
        perm_users = []
        perm_group_user_ids = []

        if user_id:
            selected_user = User.objects.get(pk=user_id)
            all_user_perms = selected_user.user_permissions.all()
            user_group_perms = selected_user.get_group_permissions_as_objects()
            user_group_perm_ids = selected_user.get_group_permissions_as_ids()
            selected_user_groups = selected_user.groups.all().order_by('name')

            if all_user_perms:
                for perm in all_user_perms:
                    if perm.pk in user_group_perm_ids:
                        user_perms.append((perm, True))
                    else:
                        user_perms.append((perm, False))
        if group_id:
            selected_group = Group.objects.get(pk=group_id)
            group_users = selected_group.user_set.filter(
                is_active=True,
            ).order_by('first_name')
            group_perms = selected_group.permissions.all().order_by(
                'content_type__app_label', 'content_type__model'
            )

        if perm_search:
            try:
                if Permission.objects.get(pk=perm_search):
                    perm_id = perm_search
                    perm_search = ""
            except (Permission.DoesNotExist, ValueError):
                pass

            pa = PermissionAdmin(Permission, admin.site)
            searched_perms = pa.search_perms(request, perm_search)

        if perm_id:
            selected_perm = Permission.objects.get(pk=perm_id)
            selected_perm_groups = selected_perm.group_set.all().order_by(
                'name'
            )
            selected_perm_users = selected_perm.user_set.filter(is_active=True)

            if selected_perm_groups:
                for group in selected_perm_groups:
                    for user in group.user_set.filter(is_active=True):
                        perm_group_user_ids.append(user.pk)
            selected_perm_group_users = User.objects.filter(
                pk__in=perm_group_user_ids
            ).order_by('first_name')

            if selected_perm_users:
                for user in selected_perm_users:
                    if selected_perm in user.user_permissions.all():
                        if selected_perm.pk in \
                                user.get_group_permissions_as_ids():
                            perm_users.append((user, True))
                        else:
                            perm_users.append((user, False))

        staff_users = User.objects.filter(
            is_staff=True, is_active=True
        ).order_by('first_name')
        apps = all_perms.values_list('content_type__app_label', flat=True)
        app_names = list(set(apps))
        context = {
            'selected_user': selected_user,
            'selected_user_groups': selected_user_groups,
            'selected_group': selected_group,
            'selected_perm': selected_perm,
            'selected_perm_groups': selected_perm_groups,
            'selected_perm_group_users': selected_perm_group_users,
            'selected_perm_users': selected_perm_users,
            'perm_users': perm_users,
            'searched_perms': searched_perms,
            'perm_search': perm_search,
            'perm_id': perm_id,
            'group_users': group_users,
            'group_perms': group_perms,
            'user_perms': user_perms,
            'user_group_perms': user_group_perms,
            'all_perms': all_perms.order_by('content_type__app_label'),
            'users': staff_users,
            'groups': groups,
            'apps': app_names
        }

        return render(request, TEMPLATE, context)

    def remove_permission(self, request):
        user_id = request.POST.get('user_id', None)
        perm_id = request.POST.get('perm_id', None)
        user = User.objects.get(pk=user_id)
        permission = Permission.objects.get(pk=perm_id)

        user.user_permissions.remove(permission)
        return HttpResponse(status=200)
