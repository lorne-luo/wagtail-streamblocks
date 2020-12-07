import os

from django.utils.html import format_html
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.core.blocks import PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from wagtailmedia.blocks import AbstractMediaChooserBlock


class CustomStructBlock(blocks.StructBlock):
    """base custom block, add block_id,block_class,block_template for each"""

    template_path = 'includes/streamblocks'  # all templates for steam block under this path

    def get_template_path(self, filename):
        filename = os.path.basename(filename)
        return os.path.join(self.template_path, filename), filename

    def get_templates(self, kwargs):
        templates = kwargs.pop('templates', ())
        if isinstance(templates, str):
            filename = os.path.basename(templates)
            return [self.get_template_path(filename)]
        elif type(templates) in [list, tuple]:
            if not len(templates):
                raise Exception('Should provide at latest one templates')

            if isinstance(templates[0], str):
                return [self.get_template_path(t) for t in templates]
            return templates
        raise Exception('templates should be tuple, list or str.')

    def __init__(self, local_blocks=None, **kwargs):
        skip = kwargs.pop('skip', False)
        templates = self.get_templates(kwargs)
        if not skip:
            local_blocks = [('block_id', blocks.CharBlock(required=False, help_text='id attribute')),
                            ('block_class', blocks.CharBlock(required=False, help_text='class attribute')),
                            ('block_template', blocks.ChoiceBlock(choices=templates,
                                                                  default=templates[0][0],
                                                                  required=False,
                                                                  help_text='select template')),
                            ('block_background_color',
                             blocks.CharBlock(required=False, help_text='color code, eg #eeeeee')),
                            ] + local_blocks
        super(CustomStructBlock, self).__init__(local_blocks, **kwargs)


class ButterflyMediaBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
                <video autoplay loop muted>
                    <source src="{0}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            '''
        else:
            player_code = '''
                <audio controls>
                    <source src="{0}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            '''
        return format_html(player_code, value.file.url)


new_table_options = {
    'colHeaders': False,
}
SUPER_STREAM_BLOCK = [
    ('heading', blocks.StructBlock([
        ('heading_type', blocks.ChoiceBlock(choices=[
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
        ])),
        ('heading_text', blocks.CharBlock(required=True)),
    ], icon='title')),
    ('table', TableBlock(table_options=new_table_options)),
    ('html', blocks.RawHTMLBlock()),
    ('accordion', blocks.StructBlock([
        ('accordion_heading', blocks.CharBlock(required=True)),
        ('accordion_content', blocks.RichTextBlock()),
    ], icon='arrows-up-down')),
    ('quote', CustomStructBlock([
        ('quote', blocks.RichTextBlock(required=False)),
    ], icon='openquote',
        templates=['streamblock_blockquote.html']
    )),
    ('info_block', CustomStructBlock([
        ('info_block_heading', blocks.CharBlock(required=False)),
        ('info_block_text', blocks.RichTextBlock(required=False)),
        ('info_block_button_name', blocks.CharBlock(required=False)),
        ('info_block_button_url', blocks.CharBlock(required=False)),
        ('info_block_image', ImageChooserBlock(required=False)),
        ('info_block_image_position', blocks.ChoiceBlock(choices=[
            ('left', 'Image on the left'),
            ('right', 'Image on the right')
        ])),
    ], icon='plus',
        templates=['streamblock_info_block.html']
    )),
    ('multi_blocks', CustomStructBlock([
        ('block_heading', blocks.CharBlock(required=False)),
        ('block_description', blocks.RichTextBlock(required=False)),
        ('items_section', blocks.ListBlock(blocks.StructBlock([
            ('heading', blocks.CharBlock(required=False)),
            ('text', blocks.RichTextBlock(required=False)),
            ('image', ImageChooserBlock(required=True)),
            ('image_link', blocks.CharBlock(required=False)),
        ]))),
        ('block_url_text', blocks.CharBlock(required=False)),
        ('block_url', blocks.CharBlock(required=False)),
    ], icon='grip',
        templates=['streamblock_multi_blocks.html', 'streamblock_multi_list.html']
    )),
    ('checklist', CustomStructBlock([
        ('checklist_heading', blocks.CharBlock(required=False)),
        ('checklist_text', blocks.RichTextBlock(required=False)),
        ('checklist_tag_type', blocks.ChoiceBlock(required=True, choices=[
            ('ul', 'Unordered list'),
            ('ol', 'Ordered list'),
        ], default='li')),
        ('checklist_lists', blocks.ListBlock(blocks.StructBlock([
            ('checklist_list', blocks.CharBlock(required=False, label="Checklist")),
        ]))),
        ('checklist_layout', blocks.ChoiceBlock(choices=[
            ('col-1', 'Single Column'),
            ('col-2', 'Double Column'),
            ('col-4', 'Four Column'),
        ])),
        ('checklist_button_name', blocks.CharBlock(required=False)),
        ('checklist_button_url', blocks.CharBlock(required=False)),
    ], icon='list-ul',
        templates=['streamblock_checklist.html'])),
    ('responsive_image', CustomStructBlock([
        ('default_image', ImageChooserBlock(help_text="helper text to come")),
        ('tablet_image', ImageChooserBlock(required=False, help_text="helper text to come")),
        ('mobile_image', ImageChooserBlock(required=False, help_text="helper text to come")),
        ('image_caption', blocks.CharBlock(required=False)),
        ('image_position', blocks.ChoiceBlock(choices=[
            ('center', 'Center'),
            ('left', 'Left'),
            ('right', 'Right'),
        ])),
        ('image_size', blocks.ChoiceBlock(choices=[
            ('original', 'Original'),
            ('small', 'Small'),
            ('full-width', 'Full width')
        ])),
    ], icon='image',
        templates=['streamblock_responsive_image.html'])),
    ('call_to_action', CustomStructBlock([
        ('call_to_action_heading', blocks.CharBlock(required=False)),
        ('call_to_action_text', blocks.RichTextBlock(required=False)),
        ('call_to_action_button_label', blocks.CharBlock(required=False)),
        ('call_to_action_button_link', blocks.CharBlock(required=False)),
    ], icon='plus',
        templates=['streamblock_call_to_action.html'])),
    ('banner_block',
     CustomStructBlock([
         ('heading', blocks.CharBlock(required=False)),
         ('heading_type', blocks.ChoiceBlock(required=False, choices=[
             ('h1', 'H1'),
             ('h2', 'H2'),
             ('h3', 'H3'),
             ('h4', 'H4'),
             ('h5', 'H5'),
             ('h6', 'H6'),
         ])),
         ('paragraph', blocks.RichTextBlock(required=False)),
         ('paragraph_button_name', blocks.CharBlock(required=False)),
         ('paragraph_button_url', blocks.CharBlock(required=False)),
         ('default_bg', ImageChooserBlock(required=True, help_text="Default background image")),
         ('tablet_bg',
          ImageChooserBlock(required=False, help_text="tablet background image, if not provided desktop would be use")),
         ('mobile_bg',
          ImageChooserBlock(required=False, help_text="mobile background image, if not provided desktop would be use")),
     ], icon='placeholder', label="Banner",
         templates=['streamblock_hero_banner.html', 'streamblock_form_banner.html',
                    'streamblock_internal_banner.html'])),
    ('paragraph_block', CustomStructBlock([
        ('paragraph_heading', blocks.CharBlock(required=False)),
        ('paragraph_tag_type', blocks.ChoiceBlock(required=False, choices=[
            ('h1', 'H1'),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
            ('span', 'span'),
        ])),
        ('paragraph_text', blocks.RichTextBlock(required=False)),
        ('paragraph_button_name', blocks.CharBlock(required=False)),
        ('paragraph_button_url', blocks.CharBlock(required=False)),
    ], icon='edit',
        templates=['streamblock_paragraph_block.html']
    )),
    ('article_blocks', CustomStructBlock([
        ('block_heading', blocks.CharBlock(required=False)),
        ('block_tag_type', blocks.ChoiceBlock(required=False, choices=[
            ('h1', 'H1'),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
            ('span', 'span'),
        ])),
        ('block_description', blocks.RichTextBlock(required=False)),
        ('display_article', blocks.ListBlock(blocks.StructBlock([
            ('article_page', PageChooserBlock(required=True)),
        ]))),
        ('block_url_text', blocks.CharBlock(required=False)),
        ('block_url', blocks.CharBlock(required=False)),
    ], icon='grip',
        templates=['streamblock_article_blocks.html']
    )),
    ('button', blocks.StructBlock([
        ('button_name', blocks.CharBlock(required=True)),
        ('button_url', blocks.CharBlock(required=True)),
        ('button_type', blocks.ChoiceBlock(choices=[
            ('btn-primary', 'Primary'),
            ('btn-secondary', 'Secondary'),
            ('btn-tertiary', 'Tertiary')
        ], required=False)),
    ], icon='form')),
    ('subscription_block', CustomStructBlock([
        ('subscription_heading', blocks.CharBlock(required=False)),
        ('subscription_tag_type', blocks.ChoiceBlock(required=False, choices=[
            ('h1', 'H1'),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
            ('span', 'span'),
        ])),
        ('subscription_text', blocks.RichTextBlock(required=False)),
        ('subscription_form_name', blocks.CharBlock(required=False)),
        ('subscription_url', blocks.CharBlock(required=False)),
        ('subscription_form_bottom', blocks.CharBlock(required=False)),
    ], icon='edit',
        templates=['streamblock_subscription_block.html']
    )),
    ('media', ButterflyMediaBlock(icon='media')),
    ('slider_blocks', CustomStructBlock([
        ('block_heading', blocks.CharBlock(required=False)),
        ('block_description', blocks.RichTextBlock(required=False)),
        ('slide', blocks.ListBlock(blocks.StructBlock([
            ('heading', blocks.CharBlock(required=False)),
            ('text', blocks.RichTextBlock(required=False)),
            ('image', ImageChooserBlock(required=True)),
        ]))),
    ], icon='grip',
        templates=['streamblock_slider_blocks.html']
    )),
    ('static_block', CustomStructBlock([
    ], icon='plus',
        templates=['streamblock_static_blocks.html', 'streamblock_static_demo.html'])),
]
