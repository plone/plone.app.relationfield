# -*- coding: utf-8 -*-
from plone.z3cform import layout
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import IFormLayer
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


class ITestForm(IFormLayer):
    multiple = RelationList(
        title=u'Multiple (Relations field)',
        required=False,
        value_type=RelationChoice(
            title=u'Multiple', vocabulary='plone.app.vocabularies.Catalog'
        ),
    )
    single = RelationChoice(
        title=u'Single',
        required=False,
        vocabulary='plone.app.vocabularies.Catalog',
    )


class TestForm(form.EditForm):
    fields = field.Fields(ITestForm)


TestView = layout.wrap_form(TestForm)
