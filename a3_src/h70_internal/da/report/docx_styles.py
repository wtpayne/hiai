# -*- coding: utf-8 -*-
"""
Module for defining docx styles.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2016 High Integrity Artificial Intelligence Systems"

license:
    "Licensed under the Apache License, Version 2.0 (the License);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."
...
"""


import docx


T_STYLE_CHAR = docx.enum.style.WD_STYLE_TYPE.CHARACTER   # pylint:disable=E1101
T_STYLE_PARA = docx.enum.style.WD_STYLE_TYPE.PARAGRAPH   # pylint:disable=E1101

ALIGN_LEFT   = docx.enum.text.WD_ALIGN_PARAGRAPH.LEFT    # pylint:disable=E1101

RGB_FONT_WEAK           = docx.shared.RGBColor(0x88, 0x88, 0x88)
RGB_FONT_MEDIUM         = docx.shared.RGBColor(0x44, 0x44, 0x44)
RGB_FONT_STRONG         = docx.shared.RGBColor(0x22, 0x22, 0x22)
RGB_FONT_PASS           = docx.shared.RGBColor(0x00, 0x55, 0x00)
RGB_FONT_FAIL           = docx.shared.RGBColor(0x55, 0x00, 0x00)
RGB_FONT_INSTRUCTIONS   = docx.shared.RGBColor(0x1a, 0x75, 0xff)

FONT_PARA_TEXT          = 'Roboto Thin'
FONT_HEADINGS           = 'Roboto Black'


# -----------------------------------------------------------------------------
def set_default_margins(sec):
    """
    Set default margins to the specified section.

    """
    sec.header_distance = docx.shared.Cm(2.0)
    sec.footer_distance = docx.shared.Cm(2.0)
    sec.top_margin      = docx.shared.Cm(2.5)
    sec.bottom_margin   = docx.shared.Cm(2.0)
    sec.left_margin     = docx.shared.Cm(2.0)
    sec.right_margin    = docx.shared.Cm(2.0)


# -----------------------------------------------------------------------------
def set_styles(document):
    """
    Set the document styles.

    """
    styles = document.styles

    # Body text
    _style_body(styles, 'Normal',       6.0)
    _style_body(styles, 'Body Text',   10.0)
    _style_body(styles, 'Body Text 2',  9.0)
    _style_body(styles, 'Body Text 3',  8.0)

    _style_body(styles, 'Instructions', 10.0)
    styles['Instructions'].font.italic    = True
    styles['Instructions'].font.color.rgb = RGB_FONT_INSTRUCTIONS

    # Line numbers
    _style_char(styles, 'Line Numbering', 5.0)
    styles['Line Numbering'].font.color.rgb = RGB_FONT_WEAK

    # Metadata at bottom of front page.
    _style_body(styles, 'Metadata', 8.0)

    # Document title and headings.
    _style_head(styles, 'Title',      22.0)
    styles['Title'].font.color.rgb = RGB_FONT_WEAK

    _style_head(styles, 'Heading 1',  14.0)
    _style_head(styles, 'Heading 2',  13.0)
    _style_head(styles, 'Heading 3',  12.0)
    _style_head(styles, 'Heading 4',  11.0)
    _style_head(styles, 'Heading 5',  10.0)
    _style_head(styles, 'Heading 6',  10.0)
    _style_head(styles, 'Heading 7',  10.0)
    _style_head(styles, 'Heading 8',  10.0)
    _style_head(styles, 'Heading 9',  10.0)
    _style_head(styles, 'Heading 10', 10.0)

    # Table Of Contents.
    _style_body(styles, 'TOC Heading', 10.0)
    _style_body(styles, 'Contents 1',  10.0)
    _style_body(styles, 'Contents 2',  10.0)
    _style_body(styles, 'Contents 3',  10.0)
    _style_body(styles, 'Contents 4',  10.0)
    _style_body(styles, 'Contents 5',  10.0)
    _style_body(styles, 'Contents 6',  10.0)
    _style_body(styles, 'Contents 7',  10.0)
    _style_body(styles, 'Contents 8',  10.0)
    _style_body(styles, 'Contents 9',  10.0)
    _style_body(styles, 'Contents 10', 10.0)
    styles['Contents 1'].font.name = FONT_HEADINGS

    # Lists
    _style_body(styles, 'List Paragraph', 10.0)
    _style_body(styles, 'List',           10.0)
    _style_body(styles, 'List 2',          9.0)
    _style_body(styles, 'List 3',          8.0)

    _style_body(styles, 'List Bullet',   10.0)
    _style_body(styles, 'List Bullet 2',  9.0)
    _style_body(styles, 'List Bullet 3',  8.0)

    _style_body(styles, 'List Number',   10.0)
    _style_body(styles, 'List Number 2',  9.0)
    _style_body(styles, 'List Number 3',  8.0)

    _style_body(styles, 'List Continue',   10.0)
    _style_body(styles, 'List Continue 2',  9.0)
    _style_body(styles, 'List Continue 3',  8.0)

    return styles


# -----------------------------------------------------------------------------
def _style_head(styles, name, font_size):
    """
    Create or modify a "Heading" type of paragraph style.

    """
    try:
        style = styles[name]
    except KeyError:
        style     = styles.add_style(name, T_STYLE_PARA)

    style.base_style    = styles['Normal']

    font                = style.font
    font.name           = FONT_HEADINGS
    font.color.rgb      = RGB_FONT_MEDIUM
    font.italic         = False
    font.size           = docx.shared.Pt(font_size)

    para                = style.paragraph_format
    para.alignment      = ALIGN_LEFT
    para.keep_together  = True
    para.keep_with_next = True
    para.space_after    = docx.shared.Pt(6)
    para.space_before   = docx.shared.Pt(3)
    para.tab_stops.add_tab_stop(docx.shared.Cm(1.7))

    # The Title paragraph file in the default python-docx template has
    # a blue bottom border set. We don't want that so we remove it here.
    # I feel that this approach is more explicit than making our own
    # customised template document).
    style.element.pPr.remove_all('w:pBdr')

    return style


# -----------------------------------------------------------------------------
def _style_body(styles, name, font_size):
    """
    Create or modify a "Body Text" type of paragraph style.

    """
    try:
        style = styles[name]
    except KeyError:
        style = styles.add_style(name, T_STYLE_PARA)

    style.base_style    = styles['Normal']

    font                = style.font
    font.name           = FONT_PARA_TEXT
    font.color.rgb      = RGB_FONT_MEDIUM
    font.size           = docx.shared.Pt(font_size)

    para                = style.paragraph_format
    para.alignment      = ALIGN_LEFT
    para.keep_together  = True
    para.keep_with_next = False
    para.space_after    = docx.shared.Pt(0)
    para.space_before   = docx.shared.Pt(0)

    return style


# -----------------------------------------------------------------------------
def _style_char(styles, name, font_size):
    """
    Create or modify a "character" style.

    """
    try:
        style = styles[name]
    except KeyError:
        style = styles.add_style(name, T_STYLE_CHAR)

    style.base_style    = styles['Default Paragraph Font']

    font                = style.font
    font.name           = FONT_PARA_TEXT
    font.color.rgb      = RGB_FONT_MEDIUM
    font.size           = docx.shared.Pt(font_size)

    return style
