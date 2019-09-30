from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        # handle key in frontend logic
        context['activate_url'] = f"{ settings.URL_FRONT }/auth/v/?key={ context['key'] }"
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
