from z3c.relationfield.interfaces import IHasRelations
from zope.schema.interfaces import IContextSourceBinder


class IDexterityHasRelations(IHasRelations):
    """ """


class IRelationChoiceSourceBinder(IContextSourceBinder):
    """ a simple, editable source usable as an object path source binder """

    def portal_types():
        """ portal types eligible to be targets """
