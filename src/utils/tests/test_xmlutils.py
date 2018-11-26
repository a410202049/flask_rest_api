#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from test.unit.base import BaseTestCase
from utils.xmlutils import XMLUtils


class XMLUtilsTestCase(BaseTestCase):
    """
    XMLUtilsTestCase
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_xml2json(self):
        xml_str = """
        <BOSFXII xmlns="http://www.bankofshanghai.com/BOSFX/2010/08" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.bankofshanghai.com/BOSFX/2010/08 BOSFX2.0.xsd">
          <XXXRq>
            <CommonRqHdr>
              <SPName>CBIB</SPName>
              <RqUID>20150324800148246569</RqUID>
              <ClearDate>20160331</ClearDate>
              <TranDate>20160331</TranDate>
              <TranTime>094338</TranTime>
              <ChannelId/>
            </CommonRqHdr>
            <SubAcctNo>11022133</SubAcctNo>
            <ProductCd>zzzzzz</ProductCd>
            <Amount>11.02</Amount>
            <Currency>156</Currency>
            <TheirRef>AAA子账户转第三方（带赎回）</TheirRef>
            <Purpose>AAA赎回</Purpose>
            <Attach/>
            <MemoInfo/>
            <KoalB64Cert/>
            <Signature/>
          </XXXRq>
        </BOSFXII>
        """
        result = XMLUtils.xml2json(xml_str, need_dict=True)
        self.assertEquals(result['BOSFXII']['XXXRq']['CommonRqHdr']['SPName'], 'CBIB')

    def test_json2xml(self):
        """
        json 字典必须有根元素
        :return:
        """
        json_data = {
            "planets": {
                "planet": [
                    {
                        "name": "Earth",
                        "radius": "6,371km"
                    },
                    {
                        "name": "Jupiter",
                        "radius": "69,911km"
                    },
                    {
                        "name": "Mars",
                        "radius": "3,390km"
                    }
                ],
                "@xmlns": "http://www.bankofshanghai.com/BOSFX/2010/08"
            },

        }
        result = XMLUtils.json2xml(json_data)
        print result
