import os
import json
import base64
import subprocess
import configparser
import io
import re
import cv2
import numpy
from PIL import Image, ImageFilter
import PySimpleGUI as sg
import easygui
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, A3, legal

sw, sh = sg.Window.get_screen_size()
sg.theme("DarkTeal2")


def popup(middle_text):
    return sg.Window(
        middle_text,
        [
            [sg.Sizer(v_pixels=20)],
            [sg.Sizer(h_pixels=20), sg.Text(middle_text), sg.Sizer(h_pixels=20)],
            [sg.Sizer(v_pixels=20)],
        ],
        no_titlebar=True,
        finalize=True,
    )


fallback_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00Z\x00\x00\x00u\x08\x02\x00\x00\x00A0a\xb6\x00\x00\x0c\xd4IDATx\x01\xed\xc1}L\x95u\xff\x07\xf0\xf7\xe7\xfb\xfd\\(bh\xc1\x94Z\xca=]\xa9EJ*N4&\x8aJ\xa8d>l\x8aY\xd9z\xd8\x9a\xd9\xf3*]M\xca:\xd7\xf7\x80\x9es\xbc\x15B\xb4\x9cm\xb1\xd9\xa3\xa6\xe2\x7f\x94i3gaS\xd3(5\x9f\xa60:\xe2@ \xce\xf5t\xdf\xf9\x9b\xbfr\xe9\x9d\xd7\x81s\x0e\x7f\x9c\xd7\x8b\x02\xff^k[&\xa2\xc8q\x1c\\\x8b\xe38p\xc3q\x008\x00\x88\x00\x10\xdcpp\x85\xe3\xe0\n\x87\x04\xad\\\xb9\x12qW\x90\xcf\x1f\xb0-\x13q\xffE\x82|\xfe\x80m\x99\x88\x03\x88$\xf9\xfc\x01\xdb2\x11\x07\x90\x90\xe4\xf3\x07l\xcbD\x1c \xa4$\x9f?`[&\xe2\x00\xc9L>\x7f\xc0\xb6L\xc4\x01B2\xf9\xfc\x01\xdb2\x11\x07\x08\xc9\xe4\xf3\x07l\xcbD\x1c $\x93\xcf\x1f\xb0-\x13q\x80\x90L>\x7f\xc0\xb6L\xc4\x01B2\xf9\xfc\x01\xdb2\x11\x07\x08\xc9\xe4\xf3\x07l\xcbD\x1c $\x93\xcf\x1f\xb0-\x13\x91\xf7\xfb\xef\xbf744466\xfevY\xf0\xb2\xb6\xb66\\\x91\x9c\x9c\xdc\xbbw\xef\xd4\xd4\xd4\xbe}\xfb\xa6\xa4\xa4\xf4\xeb\xd7/%%\xe5\xe6\x9bo&"D\x85\x90L>\x7f\xc0\xb6LDLCC\xc3\xb1c\xc7\x0e\x1f>\xfc\xcb/\xbf\xc0\xbd>}\xfa\x8c\x181\xe2\x8e;\xee\x184hP\x8f\x1e=\x10IB2\xf9\xfc\x01\xdb2\xd1\xd5:::\x8e\x1c9\xb2{\xf7\xee\xd3\xa7O\xa3+H)\xb3\xb3\xb3G\x8d\x1a5`\xc0\x00D\x86\x90L>\x7f\xc0\xb6Lt\x9d\x8e\x8e\x8e\xda\xda\xda\xea\xea\xea\xf6\xf6vD\xc0\x90!C&M\x9a4x\xf0`t5!\x99|\xfe\x80m\x99\xe8\n\x86a|\xff\xfd\xf7;v\xechooG\x84eff\x16\x14\x14\xa4\xa4\xa4\xa0\xeb\x08\xc9\xe4\xf3\x07l\xcbD\xa7\x1d;v\xec\xf3\xcf?ohh@\xb4H)\xe7\xcd\x9bw\xef\xbd\xf7\x12\x11\xba\x82\x90L>\x7f\xc0\xb6LtBkk\xeb\xb6m\xdb\xbe\xfb\xee;\xdc\x981c\xc6\x0c\x1f>\xbc_\xbf~IIIDd\x18\xc6\xc5\x8b\x17O\x9f>\xfd\xcd7\xdf\xd4\xd7\xd7\xc3\xa5\xf1\xe3\xc7\x17\x16\x1623:MH&\x9f?`[&\xc2u\xec\xd8\xb1\xaa\xaa\xaa\xe6\xe6f\xdc\x80\xc1\x83\x07\xcf\x9e=\xbb\x7f\xff\xfe\xb8\x16\xdb\xb6\x0f\x1c8\xf0\xd1G\x1fY\x96\x057222\x8a\x8a\x8az\xf4\xe8\x81\xce\x11\x92\xc9\xe7\x0f\xd8\x96\t\xf7\x1c\xc7\xd9\xb5k\xd7\xf6\xed\xdbqc\xb2\xb2\xb2f\xcf\x9e\xadi\x1a\xfe\xa7s\xe7\xce\x95\x95\x95utt\xc0\x8d\xcc\xcc\xcc\xf9\xf3\xe733:AH&\x9f?`[&\\\n\x85B[\xb7n\xdd\xb7o\x1fnLFF\xc6\xc2\x85\x0b\x99\x197\xe0\xf8\xf1\xe3\xef\xbe\xfb.\\\x9a0aBaa!:AH&\x9f?`[&\\jkk[\xb3fMcc#n\x80\xa6iK\x97.MNN\xc6\r\xdb\xb1c\xc7\x97_~\t\x97\x1e{\xec\xb1\xbb\xef\xbe\x1b\xe1\x12\x92\xc9\xe7\x0f\xd8\x96\t\xf7\xce\x9f?\xef\xf7\xfbm\xdb\xc6?\x993gNvv6\xdchnn^\xb1b\x85\xe38p\xa3g\xcf\x9e\xcb\x96-\xeb\xd5\xab\x17\xc2"$\x93\xcf\x1f\xb0-\x13a9x\xf0\xe0\x07\x1f|\x80\xff\x89\x99\x8b\x8b\x8b{\xf6\xec\t\x97\xbe\xf8\xe2\x8b\xaf\xbf\xfe\x1a.M\xbd\x0ca\x11\x92\xc9\xe7\x0f\xd8\x96\x89pUWW\xd7\xd4\xd4\xe0\xfa&M\x9a4m\xda4\xb8\xf7\xeb\xaf\xbf\x96\x95\x95\xc1%"Z\xbe|y\xef\xde\xbd\xe1\x9e\x90L>\x7f\xc0\xb6L\x84\xcb4\xcd\x8d\x1b7\xd6\xd5\xd5\xe1:\x9e~\xfa\xe9\xc1\x83\x07\xc3=\xd34_\x7f\xfdu\xd34\xe1\xd2\xacY\xb3\xc6\x8f\x1f\x0f\xf7\x84d\xf2\xf9\x03\xb6e\xa2\x13\x9a\x9b\x9b\xfd~\x7fKK\x0b\xae\xe5\xcd7\xdfLJJBX\xaa\xaa\xaajkk\xe1RZZ\xda\xcb/\xbf\x0c\xf7H2\xf9\xfc\x01\xdb2\xd19\xa7N\x9dZ\xb3f\r\xfe&55\xf5\xb5\xd7^C\xb8\xf6\xec\xd9\xb3e\xcb\x16\xb8\xb7l\xd9\xb2[n\xb9\x05.\x91d\xf2\xf9\x03\xb6e\xa2\xd3\xf6\xed\xdb\xf7\xf1\xc7\x1f\xe3j#G\x8e\\\xb0`\x01\xc2u\xe4\xc8\x91\xf7\xdf\x7f\x1f\xee=\xfa\xe8\xa3\xf7\xdcs\x0f\\\x12\x92\xc9\xe7\x0f\xd8\x96\x89Ns\x1c\xe7\xb3\xcf>\xdb\xbbw/\xfe\xe2\xbe\xfb\xee{\xf0\xc1\x07\x11\xae\xb3g\xcf\x06\x02\x01\xb87}\xfa\xf4\x89\x13\'\xc2%!\x99|\xfe\x80m\x99\xe8\n\x1d\x1d\x1d\x15\x15\x15g\xce\x9c\xc1\x15S/C\xb8\x1a\x1a\x1aJKK\xe1^VV\xd6\xbcy\xf3\xe0\x92\x90L>\x7f\xc0\xb6Lt\x91`0\xb8j\xd5\xaaP(\x84\xcb\xf2\xf2\xf2\n\n\n\x10\xae\x0b\x17.x<\x1e\xb87l\xd8\xb0\xc7\x1f\x7f\x1c.\t\xc9\xe4\xf3\x07l\xcbD\xd7\xf9\xf9\xe7\x9f+++qYNN\xce\xcc\x993\x11\xaeK\x97.\x15\x17\x17\xc3\xbd\x81\x03\x07>\xfb\xec\xb3pIH&\x7f\xe0\xdf\x96\x19B\x97\xda\xb5k\xd7\xb6m\xdb\x00dff.\\\xb8\x10\xe1\xbat\xe9Rqq1\xdc\x1b0`\xc0s\xcf=\x07\x97\x84d*)])\x08]\xcb\xb6\xed\xaa\xaa\xaa\x1f~\xf8!==}\xc9\x92%\x08\xd7\xc5\x8b\x17\xdf~\xfbm\xb87d\xc8\x90\'\x9f|\x12.\t\xc9\xa4\xeb\xba\xa6i\xe8jmmmk\xd7\xaemllTJI)\x11\x96\x0b\x17.x<\x1e\xb87|\xf8\xf0G\x1ey\x04.\t\xc9\xa4\x94bfD@}}\xbd\xcf\xe7{\xe5\x95WRSS\x11\x96\x86\x86\x86\xd2\xd2R\xb8\x97\x9b\x9b;c\xc6\x0c\xb8$$\x93R\x8a\x99\x11\x19\x07\x0f\x1e\x0c\x85B\xa3G\x8fFXN\x9c8Q^^\x0e\xf7f\xcd\x9a5~\xfcx\xb8$$\x93R^f\x89\x88iooOLLDX\x0e\x1d:\xb4i\xd3&\xb8\xf7\xd4SO\xddy\xe7\x9dpIH&\xa5\xbc\xcc\x12\xdd\xd2\xde\xbd{?\xfd\xf4S\xb8\xf7\xc6\x1bo\xf4\xe9\xd3\x07.\t\xc9\xa4\x94\x97Y\xa2[\xda\xbe}\xfbW_}\x05\x97RSS_}\xf5U"\x82KB2)\xa5\x98\x19\xdd\xd2\xda\xb5kO\x9e<\t\x97\n\n\n\xf2\xf2\xf2\xe0\x9ed\x8d\x94\xf22Kt?\xad\xad\xad\xcb\x97/\x87{\xcf?\xff\xfc\xed\xb7\xdf\x0e\xf7\x985R\xca\xcb,\xd1\xfd\x1c=z\xf4\xbd\xf7\xde\x83K\xe9\xe9\xe9\xcf<\xf3\x0c\x11\xc1=\xc9\x1a)\xa5\x98\x19\xddOUUUmm-\\z\xf8\xe1\x87G\x8c\x18\x81\xb0\x08f\xd2\x95\xd2\x98\xd1\xcd455\xbd\xf3\xce;p\xa9\x7f\xff\xfe/\xbe\xf8\xa2\x94\x12a\x11\xac\x91R\x8a\x99\xd1\xcdTWW\xd7\xd4\xd4\xc0\xa5\'\x9exb\xe8\xd0\xa1\x08\x97`&\xa5\x143\xa3;ill\xf4z\xbdp)++k\xde\xbcy\xe8\x04!\x99\x94\xf22Kt\x1b\xb6mo\xda\xb4\xe9\xc7\x1f\x7f\x84\x1bIII/\xbd\xf4Rrr2:\x81\x84$\xa5\xbc\xcc\x12\xdd\xc6\x9e={\xb6l\xd9\x02\x97\x96,Y\x92\x9e\x9e\x8e\xce!!I)/\xb3D\xf7PWW\xb7~\xfdz\xb8TTT4j\xd4(t\x1a\x91 \xa5\xbc\xcc\x12\xdd\xc0\xe9\xd3\xa7\xcb\xca\xca,\xcb\x82\x1b3g\xce\xcc\xc9\xc9AW \x12\xa4\x94\x97Y"\xd6N\x9c8\xb1n\xdd:\xcb\xb2\xe0Faa\xe1\x84\t\x13\xd0UH\x90\xae\x94\xc6\x8c\x98\xda\xbf\x7f\xff\xe6\xcd\x9b\xe1\xd2\xdc\xb9s\xc7\x8e\x1d\x8b.DD\xbaR\x1a3b\xa4\xb5\xb5u\xe7\xce\x9d\xdf~\xfb-\xdc\x90R.Z\xb4h\xd8\xb0a\xe8Z$HWJcF\xd4\xd9\xb6}\xf8\xf0\xe1O>\xf9\xa4\xad\xad\rn\xa4\xa5\xa5=\xf4\xd0C\xb7\xdez+\xba\x1c\tRJ13\xa2\xc8q\x9c\xe3\xc7\x8f\xef\xdc\xb9\xf3\xd4\xa9Sp);;{\xfa\xf4\xe9={\xf6D\x04\x10\t\xd2u\xa5i\x8c\xa8\xb0,\xeb\xc8\x91#555g\xce\x9c\x81KIIIEEEC\x87\x0eE\xc4\x08!I\xd7\x95\xa61\xa2\xc2\xb6\xedU\xabV544\xc0\xa5I\x93&\xe5\xe6\xe6\xf6\xea\xd5\x0b\x11EDJ)fF\xb4\xd4\xd6\xd6VUU\xe1\x86edd\xdc\x7f\xff\xfdiii\x88<\xdbq\xc8\xeb\xf5J)\x11-\xa1Ph\xc5\x8a\x15\xed\xed\xed\xf8\'w\xdduW^^^zz:\xa2\xc5\xb6\x1d\xf2z\x95\x94\x8c(\xda\xbd{\xf7\xd6\xad[q}c\xc6\x8c\xc9\xce\xce\x1e0`\x00\xa2\xcb\xb2m\xf2z\x95\x94\x8c(\xbat\xe9\xd2[o\xbde\xdb6\xaee\xee\xdc\xb9c\xc7\x8eE,\xd8\xb6MJ)fFtUWW\xd7\xd4\xd4\xe0o\xa4\x94\xc5\xc5\xc5\x89\x89\x89\x88\x05\xcb\xb6\xc9\xeb\xf5J)\x11]\xbf\xfd\xf6\x9bR\n\x7f3\xf52\xc4\x88eY\xa4\x94bfD\xdd\xe6\xcd\x9b\xf7\xef\xdf\x8f\xab-]\xba4%%\x051b\xdb\x16)\xa5\x98\x19Qw\xe6\xcc\x99\xd5\xabW\xe3/F\x8f\x1e=\x7f\xfe|\xc4\x8ei\x9a\xe4\xf5*)\x19\xb1\xb0~\xfd\xfa\xba\xba:\\\xb1d\xc9\x92\xf4\xf4t\xc4\x8eeY\xa4\x94bf\xc4B]]\xdd\xfa\xf5\xebq\xd9\xbf\xfe\xf5\xaf\xc5\x8b\x17\x13\x11b\xc74MRJ13b\xc1\xb6m\x9f\xcfW__\x0f`\xd1\xa2E\x19\x19\x19\x88)\xcb\xb2H)\xc5\xcc\x88\x91\x03\x07\x0e|\xf8\xe1\x87\xc9\xc9\xc9\xcb\x96-cf\xc4\x94m\xdb\xa4\x94bf\xc4H(\x14Z\xb1bEAA\xc1\xb8q\xe3\x10k\xa6i\x92R\x8a\x99\x11;G\x8f\x1e\x1d8p`RR\x12b\xcd\xb2,\xf2z\xbdRJ\xc4\x01\xb6m\x93\xd7\xab\xa4d\xc4\x01\x96e\x91\xae\xeb\x9a\xa6!vN\x9e<\xd9\xbf\x7f\xff\xc4\xc4D\xc4\x9ae\x99\xa4\xeb\x1eMK@\x8c\xb4\xb5\xb5y<\x9eI\x97!\xd6\x0c\xc3 ]\xd75MC\x8cl\xd9\xb2e\xcf\x9e=D\xf4\xc2\x0b/\xdcv\xdbm\x88)\xc30H\xd7uM\xd3\x10\x0b\x87\x0e\x1d\xda\xb4i\x13.KKK[\xbcxqbb"b\xc70\x0c\xd2u]\xd34D\xdd\xd9\xb3gW\xaf^\xed8\x0e\xae\xc8\xcc\xcc,**\x92R"F\x0c\xc3 ]\xd75MCt\x05\x83\xc1\xb5k\xd7\xb6\xb4\xb4\xe0j\x13\'N\x9c6m\x1a\x11!\x16L\xd3 ]\xd75MC\x14555UTT\x04\x83A\\\xcb\xe4\xc9\x93\xf3\xf3\xf3\x89\x08Qg\x9a&\xe9\xba\xaei\x1a\xa2%\x18\x0cVVV\x06\x83A\\_^^^~~\xbe\x10\x02\xd1e\x9a&\xe9\xba\xaei\x1a\xa2\xe2\xfc\xf9\xf3\x95\x95\x95---\xf8\'\xe3\xc6\x8d{\xe0\x81\x07\x98\x19Qd\x18!\xd2u]\xd34D\xdeO?\xfd\xb4q\xe3F\xcb\xb2pc\x86\x0c\x192\x7f\xfe\xfc\x9bn\xba\t\xd1b\x18!RJg\xd6\x10I\xa6i\xee\xde\xbd{\xc7\x8e\x1dp\xa9o\xdf\xbe\x0b\x16,\x184h\x10\xa2\xc20B\xa4\x94\xce\xac!2\x1c\xc79q\xe2\xc4\xce\x9d;O\x9e<\x89pM\x980!\'\'\xa7o\xdf\xbe\x880\xc30H\xd7uM\xd3\x10\x19\xad\xad\xad\x1e\x8f\xa7\xa3\xa3\x03\x9d3e\xca\x94\xfc\xfc|DX\xc8\x08\x91\xae\xeb\x9a\xa6!b\xce\x9d;WVV\xd6\xd1\xd1\x81peee\xcd\x993\x87\x99\x11a\x86\x11"]\xd75MC$\xd5\xd7\xd7\xaf[\xb7\xae\xa5\xa5\x05\xeeeee\xcd\x993\x87\x99\x11y\x86a\x90R\x8a\x99\x11a\x8d\x8d\x8d\xe5\xe5\xe5---p#;;{\xe6\xcc\x99\xcc\x8c\xa80\x8c\x10)\xa5\x98\x19\x91\xd7\xd8\xd8X^^\xde\xd2\xd2\x82\x1b\x93\x93\x93SXX(\x84@\xb4\x84B!\xd2u]\xd34DEcccyyyKK\x0b\xfeINNNaa\xa1\x10\x02Q\x14\n\x85\xc8\xe3\xf1$$$ Z\x82\xc1`eee0\x18\xc4\xf5\xe5\xe6\xe6N\x9b6M\x08\x81\xe8\n\x85B\xe4\xf1x\x12\x12\x12\x10EMMM\x15\x15\x15\xc1`\x10\xd72y\xf2\xe4\xfc\xfc|"B\xd4\x19F\x88t\xdd\xa3i\t\x88\xae\xa6\xa6\xa6\x8a\x8a\x8a`0\x88\xabM\x9e<9??\x9f\x88\x10\x0b\x86a\x90\xee\xf1h\t\t\x88\xba\xa6\xa6\xa6\x8a\x8a\x8a`0\x88+\xa6N\x9d:e\xca\x14"B\x8c\x18\x86A\x1e\x8f\'!!\x01\xb1\xd0\xdc\xdc\xbca\xc3\x86s\xe7\xce\x01\x981cFnn.b\xca0\x0c\xd2u]\xd34\xc4Hss\xf3\x86\r\x1bF\x8e\x1c\x99\x9b\x9b\x8bX3\x0c\x83\x94R\xcc\x8c8\xc04\rRJ13\xe2\x00\xd34H)\xc5\xcc\x88\x03\x0c\xc3 \xa5\x143#\x0e0\x0c\x83\x94R\xcc\x8c8\xc00\x0c*)-\x15D\x88\x03\x0c\xc3\xa0\x92\x92\x12!\x04\xe2\x00\xc30Hy\xbd,%\xe2\x00\xc30\xa8\xa4\xa4D\x08\x818\xc04\r*--%"\xc4\x01\xa6iPIi\xa9 B\x1c`\x9a&\x95\x94\x94\x08!\x10\x07\x98\xa6I%%%B\x08\xc4\x01\x86a\xd0\xca\x95+\x11w\x05\xe9JI!\x1c\x00\x8e\x03\x80H\xe0\xff\x10\xfe\xe0\xfc\x01\x7fA$\xf0\x07\x07 \x10\xe0\xfc\x01\xff\x8f\x88\xf0_\x84kpp\x85\x83\xab\x10\xfe\xe4\xe0*\x84\xeb!\x10\xfe\x8a@\xf8\x93\xe3\x00pp\x85\x03\x10\xfe\xe4\xe0o\x1c\xc71\x0c\xe3?X\xdaD\xe2\xdc\x81\xdb\xf4\x00\x00\x00\x00IEND\xaeB`\x82'
fallback_size = (90, 117)

loading_window = popup("Loading...")
loading_window.refresh()

cwd = os.path.dirname(__file__)
image_dir = os.path.join(cwd, "images")
crop_dir = os.path.join(image_dir, "crop")
print_json = os.path.join(cwd, "print.json")
img_cache = os.path.join(cwd, "img.cache")
for folder in [image_dir, crop_dir]:
    if not os.path.exists(folder):
        os.mkdir(folder)

config = configparser.ConfigParser()
config.read(os.path.join(cwd, "config.ini"))
cfg = config["DEFAULT"]

card_size_with_bleed_inch = (2.72, 3.7)
card_size_without_bleed_inch = (2.48, 3.46)


def load_vibrance_cube():
    with open(os.path.join(cwd, "vibrance.CUBE")) as f:
        lut_raw = f.read().splitlines()[11:]
    lsize = round(len(lut_raw) ** (1 / 3))
    row2val = lambda row: tuple([float(val) for val in row.split(" ")])
    lut_table = [row2val(row) for row in lut_raw]
    lut = ImageFilter.Color3DLUT(lsize, lut_table)
    return lut


vibrance_cube = load_vibrance_cube()
del load_vibrance_cube


def list_files(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]


def mm_to_inch(mm):
    return mm * 0.0393701


def inch_to_mm(inch):
    return inch / 0.0393701


def is_number_string(str):
    return str.replace(".", "", 1).isdigit()


def cap_bleed_edge_str(bleed_edge):
    if is_number_string(bleed_edge):
        bleed_edge_num = float(bleed_edge)
        max_bleed_edge = inch_to_mm(0.12)
        if bleed_edge_num > max_bleed_edge:
            bleed_edge_num = min(bleed_edge_num, max_bleed_edge)
            bleed_edge = "{:.2f}".format(bleed_edge_num)
    return bleed_edge


def grey_out(main_window):
    the_grey = sg.Window(
        title="",
        layout=[[]],
        alpha_channel=0.6,
        titlebar_background_color="#888888",
        background_color="#888888",
        size=main_window.size,
        disable_close=True,
        location=main_window.current_location(more_accurate=True),
        finalize=True,
    )
    the_grey.disable()
    the_grey.refresh()
    return the_grey


def read_image(path):
    with open(path, "rb") as f:
        bytes = bytearray(f.read())
        numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
        image = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        return image


def write_image(path, image):
    with open(path, "wb") as f:
        _, bytes = cv2.imencode(".png", image)
        bytes.tofile(f)


# Draws black-white dashed cross at `x`, `y`
def draw_cross(can, x, y, c=6, s=1):
    dash = [s, s]
    can.setLineWidth(s)

    # First layer
    can.setDash(dash)
    can.setStrokeColorRGB(255, 255, 255)
    can.line(x, y - c, x, y + c)
    can.setStrokeColorRGB(0, 0, 0)
    can.line(x - c, y, x + c, y)

    # Second layer with phase offset
    can.setDash(dash, s)
    can.setStrokeColorRGB(0, 0, 0)
    can.line(x, y - c, x, y + c)
    can.setStrokeColorRGB(255, 255, 255)
    can.line(x - c, y, x + c, y)


def pdf_gen(p_dict, size):
    rgx = re.compile(r"\W")
    img_dict = p_dict["cards"]
    has_backside = print_dict["backside_enabled"]
    bleed_edge = float(p_dict["bleed_edge"])
    has_bleed_edge = bleed_edge > 0
    if has_bleed_edge:
        b = mm_to_inch(bleed_edge)
        img_dir = os.path.join(crop_dir, str(bleed_edge).replace(".", "p"))
    else:
        b = 0
        img_dir = crop_dir
    (w, h) = card_size_without_bleed_inch
    w, h = (w + 2 * b) * 72, (h + 2 * b) * 72
    b = b * 72
    rotate = bool(p_dict["orient"] == "Landscape")
    size = tuple(size[::-1]) if rotate else size
    pw, ph = size
    pdf_fp = os.path.join(
        cwd,
        (
            f"{re.sub(rgx, '', p_dict['filename'])}.pdf"
            if len(p_dict["filename"]) > 0
            else "_printme.pdf"
        ),
    )
    pages = canvas.Canvas(pdf_fp, pagesize=size)
    cols, rows = int(pw // w), int(ph // h)
    rx, ry = round((pw - (w * cols)) / 2), round((ph - (h * rows)) / 2)
    ry = ph - ry - h
    total_cards = sum(img_dict.values())
    images_per_page = cols * rows
    i = 0

    images = []
    for img in img_dict.keys():
        images.extend([img] * img_dict[img])
    images = [
        images[i : i + images_per_page] for i in range(0, len(images), images_per_page)
    ]

    for page_images in images:

        def get_ith_image_coords(i):
            _, j = divmod(i, images_per_page)
            y, x = divmod(j, cols)
            return x, y

        def draw_image(img, x, y):
            img_path = os.path.join(img_dir, img)
            if os.path.exists(img_path):
                pages.drawImage(
                    img_path,
                    x * w + rx,
                    ry - y * h,
                    w,
                    h,
                )

        # Draw front-sides
        for i, img in enumerate(page_images):
            x, y = get_ith_image_coords(i)
            draw_image(img, x, y)

            # Draw lines per image
            if has_bleed_edge:
                draw_cross(pages, (x + 0) * w + b + rx, ry - (y + 0) * h + b)
                draw_cross(pages, (x + 1) * w - b + rx, ry - (y + 0) * h + b)
                draw_cross(pages, (x + 1) * w - b + rx, ry - (y - 1) * h - b)
                draw_cross(pages, (x + 0) * w + b + rx, ry - (y - 1) * h - b)

        # Next page
        pages.showPage()

        # Draw lines for whole page
        if not has_bleed_edge:
            for cy in range(rows + 1):
                for cx in range(cols + 1):
                    draw_cross(pages, rx + w * cx, ry - h * cy)

        # Draw back-sides if requested
        if has_backside:
            for i, img in enumerate(page_images):
                backside = (
                    print_dict["backsides"][img]
                    if img in print_dict["backsides"]
                    else print_dict["backside_default"]
                )
                x, y = get_ith_image_coords(i)
                draw_image(backside, x, y)

            # Next page
            pages.showPage()

    saving_window = popup("Saving...")
    saving_window.refresh()
    pages.save()
    saving_window.close()
    try:
        subprocess.Popen([pdf_fp], shell=True)
    except Exception as e:
        print(e)


def need_run_cropper(folder, bleed_edge):
    has_bleed_edge = bleed_edge is not None and bleed_edge > 0

    output_dir = crop_dir
    if has_bleed_edge:
        output_dir = os.path.join(output_dir, str(bleed_edge).replace(".", "p"))

    if not os.path.exists(output_dir):
        return True

    for img_file in list_files(folder):
        if os.path.splitext(img_file)[1] in [
            ".gif",
            ".jpg",
            ".jpeg",
            ".png",
        ] and not os.path.exists(os.path.join(output_dir, img_file)):
            return True

    return False


def cropper(folder, img_dict, bleed_edge):
    has_bleed_edge = bleed_edge is not None and bleed_edge > 0
    if has_bleed_edge:
        img_dict = cropper(folder, img_dict, None)

    i = 0
    output_dir = crop_dir
    if has_bleed_edge:
        output_dir = os.path.join(output_dir, str(bleed_edge).replace(".", "p"))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for img_file in list_files(folder):
        if os.path.splitext(img_file)[1] not in [
            ".gif",
            ".jpg",
            ".jpeg",
            ".png",
        ] or os.path.exists(os.path.join(output_dir, img_file)):
            continue
        im = read_image(os.path.join(folder, img_file))
        i += 1
        (h, w, _) = im.shape
        (bw, bh) = card_size_with_bleed_inch
        c = round(0.12 * min(w / bw, h / bh))
        dpi = c * (1 / 0.12)
        if has_bleed_edge:
            bleed_edge_inch = mm_to_inch(bleed_edge)
            bleed_edge_pixel = dpi * bleed_edge_inch
            c = round(0.12 * min(w / bw, h / bh) - bleed_edge_pixel)
            print(
                f"{img_file} - DPI calculated: {dpi}, cropping {c} pixels around frame (adjusted for bleed edge)"
            )
        else:
            print(
                f"{img_file} - DPI calculated: {dpi}, cropping {c} pixels around frame"
            )
        crop_im = im[c : h - c, c : w - c]
        (h, w, _) = crop_im.shape
        max_dpi = cfg.getint("Max.DPI")
        if dpi > max_dpi:
            new_size = (
                int(round(w * cfg.getint("Max.DPI") / dpi)),
                int(round(h * cfg.getint("Max.DPI") / dpi)),
            )
            print(
                f"{img_file} - Exceeds maximum DPI {max_dpi}, resizing to {new_size[0]}x{new_size[1]}"
            )
            crop_im = cv2.resize(crop_im, new_size, interpolation=cv2.INTER_CUBIC)
            crop_im = numpy.array(
                Image.fromarray(crop_im).filter(ImageFilter.UnsharpMask(1, 20, 8))
            )
        if cfg.getboolean("Vibrance.Bump"):
            crop_im = numpy.array(Image.fromarray(crop_im).filter(vibrance_cube))
        write_image(os.path.join(output_dir, img_file), crop_im)

    if i > 0 and not has_bleed_edge:
        return cache_previews(img_cache, output_dir)
    else:
        return img_dict


def to_bytes(file_or_bytes, resize=None):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :param resize:  optional new size
    :return: (bytes) a byte-string object
    """
    if isinstance(file_or_bytes, str):
        img = read_image(file_or_bytes)
    else:
        try:
            dataBytesIO = io.BytesIO(base64.b64decode(file_or_bytes))
            buffer = dataBytesIO.getbuffer()
            img = cv2.imdecode(numpy.frombuffer(buffer, numpy.uint8), -1)
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            buffer = dataBytesIO.getbuffer()
            img = cv2.imdecode(numpy.frombuffer(buffer, numpy.uint8), -1)

    (cur_height, cur_width, _) = img.shape
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = cv2.resize(
            img,
            (int(cur_width * scale), int(cur_height * scale)),
            interpolation=cv2.INTER_AREA,
        )
        cur_height, cur_width = new_height, new_width
    _, buffer = cv2.imencode(".png", img)
    bio = io.BytesIO(buffer)
    del img
    return bio.getvalue(), (cur_width, cur_height)


def cache_previews(file, folder, data={}):
    for f in list_files(folder):
        if f in data.keys():
            continue

        fn = os.path.join(folder, f)
        im = read_image(fn)
        (h, w, _) = im.shape
        del im
        r = 248 / w
        image_data, image_size = to_bytes(fn, (round(w * r), round(h * r)))
        data[f] = {
            "data": str(image_data),
            "size": image_size,
        }
        preview_data, preview_size = to_bytes(
            fn, (image_size[0] * 0.45, image_size[1] * 0.45)
        )
        data[f + "_preview"] = {
            "data": str(preview_data),
            "size": preview_size,
        }

    with open(file, "w") as fp:
        json.dump(data, fp, ensure_ascii=False)
    return data


def img_frames_refresh(max_cols):
    frame_list = []
    for card_name, number in print_dict["cards"].items():
        if not os.path.exists(os.path.join(crop_dir, card_name)):
            print(f"{card_name} not found.")
            continue

        img_size = img_dict[card_name]["size"]
        backside_padding = 40
        padded_size = tuple(s + backside_padding for s in img_size)

        img_layout = [
            sg.Push(),
            sg.Graph(
                canvas_size=padded_size,
                graph_bottom_left=(0, 0),
                graph_top_right=padded_size,
                key=f"GPH:{card_name}",
                enable_events=True,
                drag_submits=True,
                motion_events=True,
            ),
            sg.Push(),
        ]
        button_layout = [
            sg.Push(),
            sg.Button(
                "-",
                key=f"SUB:{card_name}",
                target=f"NUM:{card_name}",
                size=(5, 1),
                enable_events=True,
            ),
            sg.Input(number, key=f"NUM:{card_name}", size=(5, 1)),
            sg.Button(
                "+",
                key=f"ADD:{card_name}",
                target=f"NUM:{card_name}",
                size=(5, 1),
                enable_events=True,
            ),
            sg.Push(),
        ]
        frame_layout = [[sg.Sizer(v_pixels=5)], img_layout, button_layout]
        title = (
            card_name
            if len(card_name) < 35
            else card_name[:28] + "..." + card_name[card_name.rfind(".") - 1 :]
        )
        frame_list += [
            sg.Frame(
                title=f" {title} ",
                layout=frame_layout,
                title_location=sg.TITLE_LOCATION_BOTTOM,
                vertical_alignment="center",
            ),
        ]
    new_frames = [
        frame_list[i : i + max_cols] for i in range(0, len(frame_list), max_cols)
    ]
    if len(new_frames) == 0:
        return sg.Push()
    return sg.Column(
        layout=new_frames, scrollable=True, vertical_scroll_only=True, expand_y=True
    )


def img_draw_single_graph(window, card_name, has_backside):
    graph = window["GPH:" + card_name]

    img_data = eval(img_dict[card_name]["data"])
    img_size = img_dict[card_name]["size"]

    backside_padding = 40

    graph.erase()
    graph.metadata = {}
    if has_backside:
        backside = (
            print_dict["backsides"][card_name]
            if card_name in print_dict["backsides"]
            else print_dict["backside_default"]
        )
        if backside in img_dict:
            backside = backside + "_preview"
            backside_data = eval(img_dict[backside]["data"])
            backside_size = img_dict[backside]["size"]
        else:
            backside_data = fallback_data
            backside_size = fallback_size

        padded_size = tuple(s + backside_padding for s in img_size)
        graph.set_size(padded_size)
        graph.change_coordinates(graph_bottom_left=(0, 0), graph_top_right=padded_size)

        graph.metadata["back_id"] = graph.draw_image(
            data=backside_data, location=(0, backside_size[1])
        )
        graph.metadata["front_id"] = graph.draw_image(
            data=img_data, location=(backside_padding, backside_padding + img_size[1])
        )
    else:
        padded_size = (img_size[0] + backside_padding, img_size[1])
        graph.set_size(padded_size)
        graph.change_coordinates(graph_bottom_left=(0, 0), graph_top_right=padded_size)

        graph.metadata["back_id"] = 0
        graph.metadata["front_id"] = graph.draw_image(
            data=img_data, location=(backside_padding / 2, padded_size[1])
        )


def img_draw_graphs(window):
    has_backside = print_dict["backside_enabled"]

    for card_name, number in print_dict["cards"].items():
        if not os.path.exists(os.path.join(crop_dir, card_name)):
            print(f"{card_name} not found.")
            continue

        img_draw_single_graph(window, card_name, has_backside)


def window_setup(cols):
    column_layout = [
        [
            sg.Button(button_text=" Config ", size=(10, 1), key="CONFIG"),
            sg.Text("Paper Size:"),
            sg.Combo(
                print_dict["page_sizes"],
                default_value=print_dict["pagesize"],
                readonly=True,
                key="PAPER",
            ),
            sg.VerticalSeparator(),
            sg.Text("Orientation:"),
            sg.Combo(
                ["Portrait", "Landscape"],
                default_value=print_dict["orient"],
                readonly=True,
                key="ORIENT",
            ),
            sg.VerticalSeparator(),
            sg.Text("Bleed Edge (mm):"),
            sg.Input(
                print_dict["bleed_edge"], size=(6, 1), key="BLEED", enable_events=True
            ),
            sg.VerticalSeparator(),
            sg.Button(button_text=" Select All ", size=(10, 1), key="SELECT"),
            sg.Button(button_text=" Unselect All ", size=(10, 1), key="UNSELECT"),
            sg.VerticalSeparator(),
            sg.Text("PDF Filename:"),
            sg.Input(
                print_dict["filename"], size=(20, 1), key="FILENAME", enable_events=True
            ),
            sg.Push(),
            sg.Button(button_text=" Run Cropper ", size=(10, 1), key="CROP"),
            sg.Button(button_text=" Save Project ", size=(10, 1), key="SAVE"),
            sg.Button(button_text=" Render PDF ", size=(10, 1), key="RENDER"),
        ],
        [
            sg.Checkbox(
                "Backside",
                key="ENABLE_BACKSIDE",
                default=print_dict["backside_enabled"],
            ),
            sg.Button(
                button_text=" Default ",
                size=(10, 1),
                key="DEFAULT_BACKSIDE",
                disabled=not print_dict["backside_enabled"],
            ),
            sg.Push(),
        ],
        [
            sg.Frame(
                title="Card Images",
                layout=[[img_frames_refresh(cols)]],
                expand_y=True,
                expand_x=True,
            ),
        ],
    ]
    layout = [
        [
            sg.Column(layout=column_layout, expand_y=True),
        ],
    ]
    window = sg.Window(
        "PDF Proxy Printer",
        layout,
        resizable=True,
        finalize=True,
        element_justification="center",
        enable_close_attempted_event=True,
        size=print_dict["size"],
    )
    img_draw_graphs(window)

    for card_name in print_dict["cards"].keys():

        def make_number_callback(key):
            def number_callback(var, index, mode):
                window.write_event_value(key, window[key].TKStringVar.get())

            return number_callback

        window[f"NUM:{card_name}"].TKStringVar.trace(
            "w", make_number_callback(f"NUM:{card_name}")
        )

    def make_combo_callback(key):
        def combo_callback(var, index, mode):
            window.write_event_value(key, window[key].TKStringVar.get())

        return combo_callback

    window["PAPER"].TKStringVar.trace("w", make_combo_callback("PAPER"))
    window["ORIENT"].TKStringVar.trace("w", make_combo_callback("ORIENT"))

    def reset_button(button):
        button.set_tooltip(None)
        button.update(disabled=False)

    def crop_callback(var, index, mode):
        reset_button(window["RENDER"])

    window["CROP"].TKStringVar.trace("w", crop_callback)

    def bleed_callback(var, index, mode):
        bleed_input = window["BLEED"]
        bleed_edge = bleed_input.TKStringVar.get()
        bleed_edge = cap_bleed_edge_str(bleed_edge)
        if bleed_edge != bleed_input.TKStringVar.get():
            bleed_input.update(bleed_edge)

        if is_number_string(bleed_edge):
            reset_button(window["RENDER"])
            reset_button(window["CROP"])

            bleed_edge_num = float(bleed_edge)
            if bleed_edge != print_dict["bleed_edge"] and need_run_cropper(
                image_dir, bleed_edge_num
            ):
                render_button = window["RENDER"]
                render_button.set_tooltip("Bleed edge changed, re-run cropper first...")
                render_button.update(disabled=True)
        else:

            def set_invalid_bleed_edge_tooltip(button):
                button.set_tooltip("Bleed edge not a valid number...")
                button.update(disabled=True)

            set_invalid_bleed_edge_tooltip(window["RENDER"])
            set_invalid_bleed_edge_tooltip(window["CROP"])

    window["BLEED"].TKStringVar.trace("w", bleed_callback)

    def enable_backside_callback(var, index, mode):
        default_backside_button = window["DEFAULT_BACKSIDE"]
        backside_enabled = window["ENABLE_BACKSIDE"].TKIntVar.get() != 0
        print_dict["backside_enabled"] = backside_enabled
        if backside_enabled:
            reset_button(default_backside_button)
        else:
            default_backside_button.update(disabled=True)
        img_draw_graphs(window)

    window["ENABLE_BACKSIDE"].TKIntVar.trace("w", enable_backside_callback)

    window.bind("<Configure>", "Event")

    for card_name, _ in print_dict["cards"].items():
        if not os.path.exists(os.path.join(crop_dir, card_name)):
            print(f"{card_name} not found.")
            continue
        window["GPH:" + card_name].bind("<Leave>", f"-Leave")

    return window


crop_list = list_files(crop_dir)
img_dict = {}
if os.path.exists(img_cache):
    with open(img_cache, "r") as fp:
        img_dict = json.load(fp)
if len(img_dict.keys()) < len(crop_list):
    img_dict = cache_previews(img_cache, crop_dir, img_dict)
img_dict = cropper(image_dir, img_dict, None)

if os.path.exists(print_json):
    with open(print_json, "r") as fp:
        print_dict = json.load(fp)
    # Check that we have all our cards accounted for
    if len(print_dict["cards"].items()) < len(list_files(crop_dir)):
        for img in list_files(crop_dir):
            if img not in print_dict["cards"].keys():
                print_dict["cards"][img] = 1
    # Make sure we have a sensible bleed edge
    bleed_edge = print_dict["bleed_edge"]
    bleed_edge = cap_bleed_edge_str(bleed_edge)
    if not is_number_string(bleed_edge):
        bleed_edge = "0"
    print_dict["bleed_edge"] = bleed_edge
else:
    # Initialize our values
    print_dict = {
        "cards": {},
        # program window settings
        "size": (1480, 920),
        "columns": 5,
        # backside options
        "backside_enabled": False,
        "backside_default": "__barck.png",
        "backsides": {},
        # pdf generation options
        "pagesize": "Letter",
        "page_sizes": ["Letter", "A4", "A3", "Legal"],
        "orient": "Portrait",
        "bleed_edge": "0",
        "filename": "_printme",
    }
    for img in list_files(crop_dir):
        print_dict["cards"][img] = 1

bleed_edge = float(print_dict["bleed_edge"])
if need_run_cropper(image_dir, bleed_edge):
    cropper(image_dir, img_dict, bleed_edge)

window = window_setup(print_dict["columns"])
old_size = window.size
for k in window.key_dict.keys():
    if "CRD:" in str(k):
        window[k].bind("<Button-1>", "-LEFT")
        window[k].bind("<Button-3>", "-RIGHT")
loading_window.close()
hover_backside = False

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        break

    def get_card_name_from_event(event):
        name = event[4:]
        name = name.replace("+MOVE", "")
        name = name.replace("+UP", "")
        if "-RIGHT" in name:
            name = name.replace("-RIGHT", "")
            e = "SUB:"
        elif "-LEFT" in name:
            name = name.replace("-LEFT", "")
            e = "ADD:"
        else:
            e = event[:4]
        return name, e

    if "GPH:" in event:
        if "-Leave" in event:
            key = event[:-6]
            graph = window[key]
            graph.bring_figure_to_front(graph.metadata["front_id"])

        elif "+MOVE" in event:
            name, e = get_card_name_from_event(event)
            key = "GPH:" + name
            pos = values[key]

            graph = window[key]
            if graph.metadata:
                figures = graph.get_figures_at_location(pos)
                if graph.metadata["back_id"] in figures:
                    hover_backside = True
                    graph.bring_figure_to_front(graph.metadata["back_id"])
                else:
                    hover_backside = False
                    graph.bring_figure_to_front(graph.metadata["front_id"])

        elif hover_backside:
            if path := easygui.fileopenbox(default="images/*"):
                path = os.path.relpath(path, os.path.abspath("images"))
                name, e = get_card_name_from_event(event)
                print_dict["backsides"][name] = path

                has_backside = print_dict["backside_enabled"]
                img_draw_single_graph(window, name, has_backside)

    if event[:4] in ("ADD:", "SUB:"):
        name, e = get_card_name_from_event(event)
        key = "NUM:" + name
        num = int(values[key])
        num += 1 if "ADD" in e else 0 if num <= 0 else -1
        print_dict["cards"][name] = num
        window[key].update(str(num))

    if "NUM:" in event:
        name, e = get_card_name_from_event(event)
        if is_number_string(values[event]):
            print_dict["cards"][name] = int(values[event])

    if "ORIENT" in event:
        print_dict["orient"] = values[event]

    if "PAPER" in event:
        print_dict["pagesize"] = values[event]

    if "BLEED" in event:
        print_dict["bleed_edge"] = window["BLEED"].get()

    if "FILENAME" in event:
        print_dict["filename"] = window["FILENAME"].get()

    if "CONFIG" in event:
        subprocess.Popen(["config.ini"], shell=True)

    if "SAVE" in event:
        with open(print_json, "w") as fp:
            json.dump(print_dict, fp)

    if event in ["CROP", "RENDER"]:
        config.read(os.path.join(cwd, "config.ini"))
        cfg = config["DEFAULT"]

    if "CROP" in event:
        oldwindow = window
        oldwindow.disable()
        grey_window = grey_out(window)

        bleed_edge = float(print_dict["bleed_edge"])
        img_dict = cropper(image_dir, img_dict, bleed_edge)
        for img in list_files(crop_dir):
            if img not in print_dict["cards"].keys():
                print(f"{img} found and added to list.")
                print_dict["cards"][img] = 1

        window = window_setup(print_dict["columns"])
        window.enable()
        window.bring_to_front()
        oldwindow.close()
        grey_window.close()
        window.refresh()
        for k in window.key_dict.keys():
            if "CRD:" in str(k):
                window[k].bind("<Button-1>", "-LEFT")
                window[k].bind("<Button-3>", "-RIGHT")

    if "RENDER" in event:
        window.disable()
        grey_window = grey_out(window)
        render_window = popup("Rendering...")
        render_window.refresh()
        lookup = {"Letter": letter, "A4": A4, "A3": A3, "Legal": legal}
        pdf_gen(print_dict, lookup[print_dict["pagesize"]])
        render_window.close()
        grey_window.close()
        window.enable()
        window.bring_to_front()
        window.refresh()

    if "SELECT" in event:
        for card_name in print_dict["cards"].keys():
            print_dict["cards"][card_name] = 1
            window[f"NUM:{card_name}"].update("1")

    if "UNSELECT" in event:
        for card_name in print_dict["cards"].keys():
            print_dict["cards"][card_name] = 0
            window[f"NUM:{card_name}"].update("0")

    if event in ["DEFAULT_BACKSIDE"]:
        if path := easygui.fileopenbox(default="images/*"):
            print_dict["backside_default"] = os.path.relpath(
                path, os.path.abspath("images")
            )
            img_draw_graphs(window)

    if event and print_dict["size"] != window.size:
        print_dict["size"] = window.size

with open(print_json, "w") as fp:
    json.dump(print_dict, fp)
window.close()
