from django.core.management.base import BaseCommand
from django.db.models import Model
from django.db.models.loading import get_model
from datetime import datetime


def attribute_to_str(obj, field):
    value = getattr(obj, field.name)
    if value is None:
        value = u'None'
    elif isinstance(value, datetime):
        value = repr(value)
    elif isinstance(value, Model):
        value = value.id
    elif isinstance(value, basestring):
        if '\n' in value:
            value = u'u\"\"\"%s\"\"\"' % value.replace('\'', '\\\'')\
                .replace('\"', '\\\"')
        else:
            value = u'u\'%s\'' % value.replace('\'', '\\\'') \
                .replace('\"', '\\\"')

    return u'%s=%s' % (field.name, value)


def print_object_as_code_fixture(obj):
    print u'%(model)s.objects.create(%(attributes)s)\n' % ({
        'model' : obj.__class__.__name__,
        'attributes' : u',\n'.join(
            attribute_to_str(obj, field) for field in obj._meta.fields)})


def print_object_dict(obj):
    print obj.__dict__


def get_object_model_attributes(obj, depth,
                                print_method=print_object_as_code_fixture):
    if not depth:
        return
    depth -= 1
    print_method(obj)
    related_models = obj._meta.get_all_related_objects()
    for self_reference in related_models:
        for related_object in self_reference.related_model.objects.filter(
                **{self_reference.field.name: obj}):
            get_object_model_attributes(related_object, depth,
                                        print_method=print_method)


class Command(BaseCommand):
    help = 'Produce test set up fixtures fast and dirty.'
    ARG_MODEL = 'model'
    IDS = 'ids'
    DEPTH = 'depth'
    AS_DICT = 'as_dict'

    def add_arguments(self, parser):
        parser.add_argument('--%s' % Command.ARG_MODEL, type=str,
                            help='A model reference with the app path to the '
                                 'model e.g. sportamor.logistics.models.SupplierOrderReference')
        parser.add_argument('--%s' % Command.IDS, nargs='+', type=int,
                            help='A space delimited string of primary keys '
                                 'for the model.')
        parser.add_argument('--%s' % Command.DEPTH, type=int,
                            help='An integer defining the depth to travel for '
                                 'foreign keys in the objects referenced by '
                                 'the supplied primary keys, applies to all '
                                 'types of foreign keys.')
        parser.add_argument('--%s' % Command.AS_DICT, action='store_true',
                            help='If called, dicts will be printed instead of'
                                 'python fixture code.')

    def handle(self, *args, **options):
        model_str = options[Command.ARG_MODEL]
        ids_list = options[Command.IDS]
        depth = options[Command.DEPTH]
        as_dict = options[Command.AS_DICT]
        Model = get_model(model_str)
        objects = Model.objects.filter(id__in=ids_list)
        if as_dict:
            for object in objects:
                get_object_model_attributes(object, depth,
                                            print_method=print_object_dict)
        else:
            for object in objects:
                get_object_model_attributes(object, depth)
