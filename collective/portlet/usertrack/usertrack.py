from time import time
from Acquisition import aq_inner, aq_chain
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.component import getUtility
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from collective.portlet.usertrack import UsertrackMessageFactory as _
from collective.portlet.usertrack.events import GetUsersForPath

class IUsertrack(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    timeout = schema.Int(
            title=_(u"label_timeout", default=u"Inactivity timeout"),
            description=_(u"help_timeout",
                default=u"Select how long (in minutes) it takes for a user "
                        u"to be considered inactive."),
            required=True,
            default=5,
            min=1)

    roles = schema.Set(
            title=_(u"label_roles", default=u"Roles"),
            description=_(u"help_roles",
                default=u"Select roles users must have for them to appear in "
                        u"in the portlet. Users must have at least one of "
                        u"these roles to appear in the portlet."),
            value_type=schema.Choice(vocabulary="plone.app.vocabularies.Roles"))


    folder_type = schema.Set(
            title=_(u"label_folder_type", default=u"Folder type"),
            description=_(u"help_folder_type",
                          default=u"Select the content type where roles will "
                                  u"be checked. The system will look for the "
                                  u"first item of this type in the breadcrumbs "
                                  u"and check roles there."),
            required=False,
            value_type=schema.Choice(vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"))



class Assignment(base.Assignment):
    """Portlet assignment.
    """

    implements(IUsertrack)

    roles = ()
    folder_type = None
    timeout = 5

    def __init__(self, timeout=5, roles=(), folder_type=None):
        self.timeout=timeout
        self.roles=roles
        self.folder_type=folder_type

    title = _(u"portlet_title", default=u"Active Users")


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('usertrack.pt')

    def _morph(self, member):
        info=dict(userid=member.getId(),
                  fullname=member.getProperty("fullname"),
                  )
        if info is None:
            info={}

        portrait=self.mt.getPersonalPortrait(member.getId())
        if portrait is not None:
            info["portrait"]=portrait.tag(alt="", title=info["fullname"])

        return info


    def update(self):
        self.mt=getToolByName(self.context, "portal_membership")
        site=getUtility(ISiteRoot)
        rootpath="/".join(site.getPhysicalPath())

        users=GetUsersForPath(rootpath, after=(time()-(self.data.timeout*60)))
        users=[self.mt.getMemberById(user["userid"]) for user in users]
        users=filter(None, users)

        if self.data.roles and users:
            context=aq_inner(self.context)
            if self.data.folder_type:
                for entry in aq_chain(context):
                    if getattr(entry, "portal_type", None)==self.data.folder_type:
                        context=entry
                        break
                else:
                    context=None

            def check(member):
                if context is None:
                    roles=member.getRoles()
                else:
                    roles=member.getRolesInContext(context)
                for role in roles:
                    if role in self.data.roles:
                        return True
                return False

            users=filter(check, users)


        self.users=[self._morph(member) for member in users]



class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(IUsertrack)
    label = _(u"Add a user track portlet")
    description = _(u"help_portlet",
            default=u"The user track portlet shows the current active users.")
    form_name = _(u"Portlet configuration")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IUsertrack)
    label = _(u"Edit the user track portlet")
    description = _(u"help_portlet",
            default=u"The user track portlet shows the current active users.")
    form_name = _(u"Portlet configuration")

