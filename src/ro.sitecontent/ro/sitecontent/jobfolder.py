from Acquisition import aq_inner
from five import grok
from plone import api

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.app.contentlisting.interfaces import IContentListing

from ro.sitecontent import MessageFactory as _


class IJobFolder(form.Schema, IImageScaleTraversable):
    """
    A folder holding job openings
    """


class JobFolder(Container):
    grok.implements(IJobFolder)


class View(grok.View):
    grok.context(IJobFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_folders = len(self.job_folders()) > 0

    def job_folders(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(object_provides=IJobFolder.__identifier__,
                          review_state='published',
                          sort_on='getObjPositionInParent')
        items = IContentListing(results)
        return items
