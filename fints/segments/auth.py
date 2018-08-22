from fints.fields import CodeField, DataElementField, DataElementGroupField
from fints.formals import (
    BankIdentifier, Language2, SynchronisationMode, SystemIDStatus,
    TANMediaType2, TANMediaClass4, TANMedia5, TANMediaClass3, TANMedia4, TANUsageOption,
)
from fints.utils import fints_escape

from . import FinTS3Segment, FinTS3SegmentOLD


class HKIDN(FinTS3SegmentOLD):
    """
    HKIDN (Identifikation)
    Section C.3.1.2
    """
    type = 'HKIDN'
    version = 2

    def __init__(self, segmentno, blz, username, systemid=0, customerid=1):
        data = [
            '{}:{}'.format(self.country_code, blz),
            fints_escape(username),
            systemid,
            customerid
        ]
        super().__init__(segmentno, data)

class HKIDN2(FinTS3Segment):
    """Identifikation, version 2

    Source: FinTS Financial Transaction Services, Schnittstellenspezifikation, Formals"""
    bank_identifier = DataElementGroupField(type=BankIdentifier, _d="Kreditinstitutskennung")
    customer_id = DataElementField(type='id', _d="Kunden-ID")
    system_id = DataElementField(type='id', _d="Kundensystem-ID")
    system_id_status = CodeField(enum=SystemIDStatus, length=1, _d="Kundensystem-Status")


class HKVVB(FinTS3SegmentOLD):
    """
    HKVVB (Verarbeitungsvorbereitung)
    Section C.3.1.3
    """
    type = 'HKVVB'
    version = 3

    LANG_DE = 1
    LANG_EN = 2
    LANG_FR = 3

    PRODUCT_NAME = 'pyfints'
    PRODUCT_VERSION = '0.1'

    def __init__(self, segmentno, lang=LANG_DE):
        data = [
            0, 0, lang, fints_escape(self.PRODUCT_NAME), fints_escape(self.PRODUCT_VERSION)
        ]
        super().__init__(segmentno, data)

class HKVVB3(FinTS3Segment):
    """Verarbeitungsvorbereitung, version 3

    Source: FinTS Financial Transaction Services, Schnittstellenspezifikation, Formals"""
    bpd_version = DataElementField(type='num', max_length=3, _d="BPD-Version")
    upd_version = DataElementField(type='num', max_length=3, _d="UPD-Version")
    language = CodeField(enum=Language2, max_length=3, _d="Dialogsprache")
    product_name = DataElementField(type='an', max_length=25, _d="Produktbezeichnung")
    product_version = DataElementField(type='an', max_length=5, _d="Produktversion")

class HKSYN(FinTS3SegmentOLD):
    """
    HKSYN (Synchronisation)
    Section C.8.1.2
    """
    type = 'HKSYN'
    version = 3

    SYNC_MODE_NEW_CUSTOMER_ID = 0
    SYNC_MODE_LAST_MSG_NUMBER = 1
    SYNC_MODE_SIGNATURE_ID = 2

    def __init__(self, segmentno, mode=SYNC_MODE_NEW_CUSTOMER_ID):
        data = [
            mode
        ]
        super().__init__(segmentno, data)


class HKTAN(FinTS3SegmentOLD):
    """
    HKTAN (TAN-Verfahren festlegen)
    Section B.5.1
    """
    type = 'HKTAN'

    def __init__(self, segno, process, aref, medium, version):
        self.version = version

        if process not in ('2', '4'):
            raise NotImplementedError("HKTAN process {} currently not implemented.".format(process))
        if version not in (3, 4, 5, 6):
            raise NotImplementedError("HKTAN version {} currently not implemented.".format(version))

        if process == '4':
            if medium:
                if version == 3:
                    data = [process, '', '', '', '', '', '', '', medium]
                elif version == 4:
                    data = [process, '', '', '', '', '', '', '', '', medium]
                elif version == 5:
                    data = [process, '', '', '', '', '', '', '', '', '', '', medium]
                elif version == 6:
                    data = [process, '', '', '', '', '', '', '', '', '', medium]
            else:
                data = [process]
        elif process == '2':
            if version == 6:
                data = [process, '', '', '', aref, 'N']
            elif version == 5:
                data = [process, '', '', '', aref, '', 'N']
            elif version in (3, 4):
                data = [process, '', aref, '', 'N']
        super().__init__(segno, data)


class HKTAB(FinTS3SegmentOLD):
    """
    HKTAB (Verfügbarre TAN-Medien ermitteln)
    Section C.2.1.2
    """
    type = 'HKTAB'

    def __init__(self, segno):
        self.version = 5
        data = [
            '0', 'A'
        ]
        super().__init__(segno, data)

class HKTAB4(FinTS3Segment):
    """TAN-Generator/Liste anzeigen Bestand, version 4

    Source: FinTS Financial Transaction Services, Schnittstellenspezifikation, Sicherheitsverfahren PIN/TAN"""

    tan_media_type = CodeField(enum=TANMediaType2, _d="TAN-Medium-Art")
    tan_media_class = CodeField(enum=TANMediaClass3, _d="TAN-Medium-Klasse")

class HITAB4(FinTS3Segment):
    """TAN-Generator/Liste anzeigen Bestand Rückmeldung, version 4

    Source: FinTS Financial Transaction Services, Schnittstellenspezifikation, Sicherheitsverfahren PIN/TAN"""

    tan_usage_option = CodeField(enum=TANUsageOption, _d="TAN_Einsatzoption")
    tan_media_list = DataElementGroupField(type=TANMedia4, max_count=99, required=False, _d="TAN-Medium-Liste")

class HKTAB5(FinTS3Segment):
    """TAN-Generator/Liste anzeigen Bestand, version 5

    Source: FinTS Financial Transaction Services, Schnittstellenspezifikation, Sicherheitsverfahren PIN/TAN"""

    tan_media_type = CodeField(enum=TANMediaType2, _d="TAN-Medium-Art")
    tan_media_class = CodeField(enum=TANMediaClass4, _d="TAN-Medium-Klasse")

class HITAB5(FinTS3Segment):
    """TAN-Generator/Liste anzeigen Bestand Rückmeldung, version 5

    Source: FinTS Financial Transaction Services, Schnittstellenspezifikation, Sicherheitsverfahren PIN/TAN"""

    tan_usage_option = CodeField(enum=TANUsageOption, _d="TAN_Einsatzoption")
    tan_media_list = DataElementGroupField(type=TANMedia5, max_count=99, required=False, _d="TAN-Medium-Liste")
