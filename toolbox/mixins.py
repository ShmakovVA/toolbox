# coding: utf-8
import operator
from django.contrib.admin.utils import lookup_needs_distinct
from django.db import models

import logging
log = logging.getLogger(__name__)

class DjangoAdminSearchAndFilterMixin():
    """
        Overriding ModelAdmin.get_search_results to not split query, avoiding
        resulting amounts of joins with related models in search_fields.

        It still joins but it will only look for the complete string and not do
        the joins per split, only joins per searched related model.
    """
    def get_search_results(self, request, queryset, search_term):
        """
        Overrides ModelAdmin.get_search_results
        """
        log.debug('DjangoAdminSearchAndFilterMixin.get_search_results override '
                  'search_term=%s', search_term)
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        use_distinct = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            or_queries = []
            searches = []
            for search_field in search_fields:
                search = construct_search(str(search_field))
                or_queries.append(models.Q(**{search: search_term}))
                searches.append(search)

            queryset = queryset.filter(reduce(operator.or_, or_queries))
            if not use_distinct:
                for search_spec in searches:
                    if lookup_needs_distinct(self.opts, search_spec):
                        use_distinct = True
                        break

        return queryset, use_distinct