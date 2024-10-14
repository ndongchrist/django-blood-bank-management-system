from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


class BlogPage(Page):
    intro = RichTextField(max_length=250)
    body = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
