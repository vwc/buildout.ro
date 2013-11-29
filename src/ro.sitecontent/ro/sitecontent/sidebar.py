from Acquisition import aq_inner
from five import grok
from plone import api

from Products.CMFCore.interfaces import IContentish
from plone.app.layout.viewlets.interfaces import IPortalFooter
from plone.app.contentlisting.interfaces import IContentListing

from ro.sitecontent.contentpage import IContentPage
from ro.sitecontent.jobopening import IJobOpening


class SidebarViewlet(grok.Viewlet):
    grok.context(IContentish)
    grok.viewletmanager(IPortalFooter)
    grok.require('zope2.View')
    grok.name('ro.sitecontent.SidebarViewlet')

    def update(self):
        self.portal_url = api.portal.get().absolute_url()

    def display_parent_pointer(self, item):
        context = aq_inner(self.context)
        unwanted = ('work-fm', 'kontakt', 'impressum', context.getId())
        display = True
        if item.getId() in unwanted:
            display = False
        return display

    def job_openings(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        results = catalog(object_provides=IJobOpening.__identifier__,
                          review_state='published',
                          sort_on='modified',
                          sort_order='reverse',
                          sort_limit=3)[:3]
        items = IContentListing(results)
        return items

    def content_pages(self):
        portal = api.portal.get()
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(object_provides=IContentPage.__identifier__,
                          path=dict(query='/'.join(portal.getPhysicalPath()),
                                    depth=1),
                          review_state='published',
                          sort_on='getObjPositionInParent')
        items = IContentListing(results)
        return items
