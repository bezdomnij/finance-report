import logging

from .tf24symbols import tfsymbols
from .amazon import amz_read
from .audible import audible
from .bibliotheca import bibliotheca
from .bn import bn
from .baker import baker
from .bookmate import bookmate
from .bookmate_audio import bookmate_audio
from .ciando import ciando
from .cnpiec import cnpiec
from .dangdang import dangdang
from .dibook import dibook
from .dreame import dreame_month
from .ekonyv import ekonyv
from .eletoltes import eletoltes
from .empik import empik
from .esentral import esentral
from .findaway import findaway
from .gardners import gardners
from .google import google
from .google_audio import google_audio
from .hoopla import hoopla
from .ireader import ireader
from .jd import jd
from .libreka import libreka
from .mackin import mackin
from .odilo import odilo
from .perlego import perlego
from .scribd import scribd
from .voxa import voxa
from .overdrive import overdrive
from .storytel import storytel
from .multimediaplaza import multimediaplaza

logging.basicConfig(level=logging.INFO, filename='logs/datacamp.log', filemode='a', format='%(asctime)s %(message)s')
