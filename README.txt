Overview
========

Plone support for z3c.relationfield. If this package is installed, you
should be able to use z3c.relationfield as per its documentation for
Dexterity and Archetypes content.

Note that this package does not depend on Dexterity or Archetypes directly.
However, if plone.dexterity is installed, the DexterityContent base class
will be marked with z3c.relationfield's IHasRelations. Similarly, if
Products.Archetypes is installed, its BaseObject class will be marked with
IHasIncomingRelations, thus allowing relationships to Archetypes objects from
Dexterity content.

Other types of content can be supported by appropriate use of these marker
interfaces. See z3c.relationfield for more details.

