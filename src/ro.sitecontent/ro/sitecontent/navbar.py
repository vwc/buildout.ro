from five import grok
from plone import api

from Products.CMFCore.interfaces import IContentish
from plone.app.layout.viewlets.interfaces import IPortalFooter


class NavbarViewlet(grok.Viewlet):
    grok.context(IContentish)
    grok.viewletmanager(IPortalFooter)
    grok.require('zope2.View')
    grok.name('ro.sitecontent.NavbarViewlet')

    def update(self):
        self.portal_url = api.portal.get().absolute_url()
