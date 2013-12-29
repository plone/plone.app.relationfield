from plone.app.relationfield import RelationChoice
from plone.app.relationfield import RelationList
from plone.schemaeditor import SchemaEditorMessageFactory as _
from plone.schemaeditor.fields import FieldFactory
from plone.schemaeditor.fields import IFieldFactory
from zope.app.intid.interfaces import IIntIds
from zope.component import queryUtility
from zope.interface import implements
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder

import plone.formwidget.contenttree


class RelationFieldFactory(FieldFactory):
    implements(IFieldFactory)

    def available(self):
        return queryUtility(IIntIds) is not None


def opsb(context):
    # provide a callable with a __name__attribute
    return plone.formwidget.contenttree.obj_path_src_binder(context)

directlyProvides(opsb, IContextSourceBinder)


RelationChoiceFactory = RelationFieldFactory(
    RelationChoice,
    _(u'label_relationchoice_field', default=u'Relation Choice'),
    source=opsb,
)


RelationListFactory = RelationFieldFactory(
    RelationList,
    _(u'label_relationlist_field', default=u'Relation List')
)
