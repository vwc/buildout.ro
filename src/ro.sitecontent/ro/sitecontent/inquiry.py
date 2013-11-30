from Acquisition import aq_inner
from AccessControl import Unauthorized
from five import grok
from plone import api
from zope.component import getMultiAdapter

from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.interfaces import IContentish

from ro.sitecontent import MessageFactory as _


class InquiryForm(grok.View):
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.name('inquiry-form')

    def update(self):
        context = aq_inner(self.context)
        self.errors = {}
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('subject', 'email')
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error['active'] = True
                        error['msg'] = _(u"This field is required")
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self.process_form(form_data)

    def process_form(self, data):
        context = aq_inner(self.context)
        options = data
        context_url = context.absolute_url()
        mto = 'anfrage@roconsulting.de'
        envelope_from = '%s' % data['email']
        subject = data['subject']
        options = dict(
            company=data['company'],
            position=data['position'],
            name=data['name'],
            firstname=data['firstname'],
            phone=data['phone'],
            message=data['message'],
            url=context_url,
            subject=subject
        )
        msg = ViewPageTemplateFile("inquirymail.pt")(self, **options)
        api.portal.send_email(
            recipient=mto,
            sender=envelope_from,
            subject=subject,
            body=msg
        )
        portal_url = api.portal.get().absolute_url()
        next_url = portal_url + '/kontakt/@@inquiry-processed'
        return self.request.response.redirect(next_url)

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value


class InquiryProcessed(grok.View):
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.name('inquiry-processed')

    def update(self):
        self.portal_url = api.portal.get().absolute_url()
