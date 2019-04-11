#!/usr/bin/env python3

import unittest
from unittest.mock import patch,call
import os
import sys

import cartesian

_TEST_FILE1 = 'test1.txt'
_TEST_DATA1 = ('a','b','c')
_TEST_FILE2 = 'test2.txt'
_TEST_DATA2 = ('1','2')
_LINE_SEP = '\n'

def init_file(path,datas,sep):
    clean_file(path)
    with open(path,'w') as file:
        for data in datas:
            file.write(data)
            file.write(sep)

def clean_file(path):
    if os.path.isfile(path):
        os.remove(path)

class TestCartesian(unittest.TestCase):
    def setUp(self):
        init_file(_TEST_FILE1,_TEST_DATA1,_LINE_SEP)
        init_file(_TEST_FILE2,_TEST_DATA2,_LINE_SEP)

    def tearDown(self):
        clean_file(_TEST_FILE1)
        clean_file(_TEST_FILE2)

    unittest
    @patch('cartesian.print',return_value="no")
    def test_generate(self,mock_print):
        cartesian.generate(_TEST_FILE1,_TEST_FILE2)
        self.assertEqual(
            len(_TEST_DATA1) * len(_TEST_DATA2),
            mock_print.call_count
        )
        mock_print.assert_has_calls([
            call('a1'),call('b1'),call('c1'),
            call('a2'),call('b2'),call('c2')
        ], any_order=True)
