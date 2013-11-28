import urllib2
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

from ro.sitecontent.jobopening import IJobOpening

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
        self.has_openings = len(self.job_openings()) > 0

    def job_folders(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(object_provides=IJobFolder.__identifier__,
                          review_state='published',
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          sort_on='getObjPositionInParent')
        items = IContentListing(results)
        return items

    def job_openings(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(object_provides=IJobOpening.__identifier__,
                          review_state='published',
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          sort_on='getObjPositionInParent')
        items = IContentListing(results)
        return items

    def has_subcontent(self, item):
        return len(self.get_subcontents(item)) > 0

    def get_subcontents(self, item):
        context = aq_inner(item.getObject())
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(object_provides=IJobOpening.__identifier__,
                          review_state='published',
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=2),
                          sort_on='modified',
                          sort_order='reverse')
        items = IContentListing(results)
        return items

    def inquiry_url(self, item):
        base_url = item.getURL()
        title = self._url_quote(item.Title())
        params = '/@@inquiry-form?subject={0}'.format(title)
        url = base_url + params
        return url

    def _url_quote(self, value):
        if value:
            try:
                encoded_value = urllib2.quote(value.encode('utf-8'))
            except:
                encoded_value = urllib2.quote(value)
            return encoded_value
        else:
            return ''
