# Support for editing RelationChoice and RelationList fields
# via plone.schemaeditor.
#
# Goal, provide a schemaeditor interface that makes it easy
# to do the most common thing: browse for relations by
# portal type -- while having it still be possible to spec
# custom sources by editing XML.
#
# Support for supermodel ex/im in exportimport.py
#
# XXX: prevent edit if field is not the editable use case.

from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.fields import FieldFactory
from plone.schemaeditor.fields import IFieldFactory
from plone.schemaeditor.interfaces import IFieldEditFormSchema
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.schema import RelationChoice
from zope.app.intid.interfaces import IIntIds
from zope.component import adapter
from zope.component import adapts
from zope.component import queryUtility
from zope.interface import implementer
from zope.interface import implements
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder

import plone.formwidget.contenttree
import zope.component
import zope.interface
import zope.schema


# In order to appear in schemaeditor's list of addable/
# editable fields, we need to supply a FieldFactory
# as a utility.
#
# This requires a custom FieldFactory class so that we
# can override the available method so that we don't
# show the option when it doesn't make sense.
class RelationFieldFactory(FieldFactory):
    implements(IFieldFactory)

    def available(self):
        return queryUtility(IIntIds) is not None


# Our RelationFieldFactory will need to supply a
# default 'source' attribute for the field it returns.
# TODO: parameterize
@provider(zope.schema.interfaces.IContextSourceBinder)
def opsb(context):
    # provide a callable with a __name__attribute
    return plone.formwidget.contenttree.obj_path_src_binder(context)

# directlyProvides(opsb, zope.schema.interfaces.IContextSourceBinder)


RelationChoiceFactory = RelationFieldFactory(
    RelationChoice,
    _(u'label_relationchoice_field', default=u'Relation Choice'),
    source=opsb,
)


# Specify an editing interface and an adapter that will return it.

class IEditableRelationChoice(zope.schema.interfaces.IField):
    """XXX
    """

    source = zope.schema.DottedName(
        title=_("Source providing values"),
        description=_("The IContextSourceBinder "
                      "object that provides values for this field."),
        required=True,
        default=None,
        readonly=True,
        )

    portal_types = zope.schema.Set(
        title=_(u"Target types to allow for relations"),
        value_type=zope.schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
            ),
        )


@implementer(IFieldEditFormSchema)
@adapter(IRelationChoice)
def getRelationChoiceFieldSchema(field):
    return IEditableRelationChoice


class EditableRelationChoiceField(object):
    implements(IEditableRelationChoice)
    adapts(RelationChoice)

    def __init__(self, field):
        self.__dict__['field'] = field

    def __getattr__(self, name):
        # if name == 'source':
        #     source = getattr(self.field, name)
        #     return "%s.%s" % (source.__module__, source.__name__)
        if name == 'portal_types':
            source = self.field.source
            if IContextSourceBinder.providedBy(source):
                filter = getattr(source, 'selectable_filter', None)
                if filter is not None:
                    criteria = filter.criteria
                    portal_types = criteria.get('portal_type')
                    if len(criteria.keys()) == 1 and \
                       portal_types is not None:
                        return portal_types
            return []
        return getattr(self.field, name)

    def __setattr__(self, name, value):
        if name == 'portal_types':
            return setattr(
                self.field,
                'vocabulary',
                ObjPathSourceBinder(portal_type=value)
                )
        return setattr(self.field, name, value)

    def __delattr__(self, name):
        # import pdb; pdb.set_trace()
        return delattr(self.field, name)





# RelationListFactory = RelationFieldFactory(
#     RelationList,
#     _(u'label_relationlist_field', default=u'Relation List')
# )

