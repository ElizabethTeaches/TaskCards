"""Adds borders after the fact to task cards"""
import PIL
import PyPDF2
import pdf2image
import typing
import os


def _resize_to_keep_aspect(oldw, oldh, neww, newh):
    """Returns the new width and height to fit oldw x oldh into
    neww x newh without changing the aspect ratio"""
    newh_if_match_wid = int(neww * (oldh / oldw))
    if newh_if_match_wid < newh:
        return (neww, newh_if_match_wid)
    return (int(newh * (oldw / oldh)), newh)


def add_borders_to_img(img: PIL.Image, border_img='img/border_1.jpg',
                       margins: typing.Tuple[int, int] = (200, 200)):
    """Adds the specified border image to the background of the given
    image, by breaking the border image into 4ths, resizing in the appropriate
    aspect ratio for each 4th, and dumping onto the appropriate spot
    """

    border = PIL.Image.open(border_img)
    target_img = PIL.Image.new('RGB', img.size, 'white')

    bcs = (border.size[0] // 2, border.size[1] // 2)
    # bcs = border corner size
    new_border_size = _resize_to_keep_aspect(
        bcs[0], bcs[1],
        img.size[0] // 2, img.size[1] // 2
    )
    nbs = new_border_size

    bord = (border.crop((0, 0, bcs[0], bcs[1]))  # top-left
            .resize(new_border_size, PIL.Image.LANCZOS))
    target_img.paste(bord, (0, 0))
    bord = (border.crop((bcs[0], 0, bcs[0] * 2, bcs[1]))  # top-right
            .resize(new_border_size, PIL.Image.LANCZOS))
    target_img.paste(bord, (img.size[0] - nbs[0], 0))
    bord = (border.crop((0, bcs[1], bcs[0], bcs[1] * 2))  # bottom-left
            .resize(new_border_size, PIL.Image.LANCZOS))
    target_img.paste(bord, (0, img.size[1] - nbs[1]))
    bord = (border.crop((bcs[0], bcs[1], bcs[0] * 2, bcs[1] * 2))  # bot-right
            .resize(new_border_size, PIL.Image.LANCZOS))
    target_img.paste(bord, (img.size[0] - nbs[0], img.size[1] - nbs[1]))

    target_img.paste(
        img.resize((img.size[0] - margins[0] * 2,
                    img.size[1] - margins[1] * 2), PIL.Image.LANCZOS),
        margins
    )
    return target_img


def add_borders(pdf: str, final_pdf: str, num_pages: int):
    """Loads the PDF and exports to a PNG with pretty borders"""
    without_ext = os.path.splitext(pdf)[0]
    png = without_ext + '.png'
    pdfs = []
    for page in range(num_pages):
        out_pdf = f'{without_ext}_{page}.pdf'
        pdf2image.convert_from_path(
            pdf, dpi=300, first_page=page+1, last_page=page+1)[0].save(png)

        img = PIL.Image.open(png)
        width, height = img.size

        w_o_2 = width // 2
        h_o_2 = height // 2

        cards = [
            img.crop((0, 0, w_o_2, h_o_2)),
            img.crop((w_o_2, 0, width, h_o_2)),
            img.crop((0, h_o_2, w_o_2, height)),
            img.crop((w_o_2, h_o_2, width, height))
        ]

        for i in range(4):
            cards[i] = add_borders_to_img(cards[i])

        tar_img = PIL.Image.new('RGB', (width, height), 'white')
        tar_img.paste(cards[0], (0, 0))
        tar_img.paste(cards[1], (w_o_2, 0))
        tar_img.paste(cards[2], (0, h_o_2))
        tar_img.paste(cards[3], (w_o_2, h_o_2))
        tar_img.save(out_pdf)
        pdfs.append(out_pdf)

    merger = PyPDF2.PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(final_pdf)
    merger.close()
