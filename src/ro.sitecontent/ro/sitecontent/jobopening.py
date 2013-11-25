from five import grok

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from ro.sitecontent import MessageFactory as _


class IJobOpening(form.Schema, IImageScaleTraversable):
    """
    A single job opening
    """
    attachment = NamedBlobFile(
        title=_(u"Attachement"),
        description=_(u"Please upload additional attachment preferable as pdf"),
        required=False,
    )


class JobOpening(Container):
    grok.implements(IJobOpening)


class View(grok.View):
    grok.context(IJobOpening)
    grok.require('zope2.View')
    grok.name('view')
