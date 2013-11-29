from Acquisition import aq_inner
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

    def active_marker(self, item_id):
        context = aq_inner(self.context)
        wfm = ('work-fm',
               'kaufmaennisches-facility-management',
               'infrastrukturelles-facility-management',
               'technisches-facility-management',
               'branchennahe-jobangebote')
        active = False
        if context.getId() == item_id:
            active = True
        if item_id == 'work-fm' and context.getId() in wfm:
            active = True
        return active
