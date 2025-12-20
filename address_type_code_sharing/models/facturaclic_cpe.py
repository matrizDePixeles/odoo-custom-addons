# -*- coding: utf-8 -*-
from odoo import models
from base64 import b64encode, b64decode
from lxml import etree

class PeruSunatCpe(models.Model):
    _inherit = 'facturaclic.cpe'

    def _prepare_cpe(self):
        # Ejecutar primero la lógica original del módulo
        res = super()._prepare_cpe()

        # Normalizar la fuente del XML a bytes
        xml_bytes = None
        if self.xml_document:
            xml_bytes = self.xml_document if isinstance(self.xml_document, (bytes, bytearray)) else self.xml_document.encode('utf-8')
        elif self.datas:
            xml_bytes = b64decode(self.datas)

        if not xml_bytes:
            return res  # No hay XML para modificar

        try:
            # Namespaces UBL
            ns = {
                'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            }

            # Parsear el XML
            doc = etree.fromstring(xml_bytes)

            # Tomar la factura asociada
            move = self.invoice_ids and self.invoice_ids[0] or False
            new_code = False
            if move and move.associated_warehouse_id:
                new_code = move.associated_warehouse_id.l10n_pe_edi_address_type_code

            if new_code:
                # XPath específico del emisor
                nodes = doc.xpath(
                    './/cac:AccountingSupplierParty//cac:PartyLegalEntity//cac:RegistrationAddress/cbc:AddressTypeCode',
                    namespaces=ns
                )

                # Variante opcional: si no se encontró el nodo esperado, reemplazar todos los AddressTypeCode
                if not nodes:
                    nodes = doc.xpath('.//cbc:AddressTypeCode', namespaces=ns)

                for node in nodes:
                    node.text = str(new_code)

                # Serializar y actualizar coherentemente
                xml_out = etree.tostring(doc, encoding='UTF-8', xml_declaration=True)
                self.xml_document = xml_out.decode('utf-8')
                self.datas = b64encode(xml_out)

        except Exception:
            # Defensivo: no romper el flujo original
            pass

        return res

