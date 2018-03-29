#-*-coding:utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.test import TestCase
from django.core.exceptions import ValidationError

from tests.core.data_init import create_student_and_get_queryset
from export_csv import utils


class CleanFilenameTests(TestCase):
    def _assertCleanedFilenameEquals(self, filename, expected_filename):
        cleaned_filename = utils.clean_filename(filename)
        self.assertEqual(cleaned_filename, expected_filename)

    def test_filename_without_dots(self):
        self._assertCleanedFilenameEquals('testfile', 'testfile.csv')

    def test_filename_without_dots_cn(self):
        self._assertCleanedFilenameEquals('测试文件', '测试文件.csv')

    def test_filename_no_csv(self):
        self.assertRaises(ValidationError, utils.clean_filename, 'test.file')

    def test_filename_no_csv_cn(self):
        self.assertRaises(ValidationError, utils.clean_filename, '测试.file')

    def test_filename_not_end_of_csv(self):
        self.assertRaises(ValidationError, utils.clean_filename, 'test.csv.file')

    def test_filename_not_end_of_csv_cn(self):
        self.assertRaises(ValidationError, utils.clean_filename, '测试.csv.file')

    def test_csv_filename(self):
        self._assertCleanedFilenameEquals('testfile.csv', 'testfile.csv')

    def test_csv_filename_cn(self):
        self._assertCleanedFilenameEquals('测试文件.csv', '测试文件.csv')


class AttachDatestampTests(TestCase):
    def test_filename_should_be_cleaned_first(self):
        self.assertRaises(ValidationError, utils.attach_datestamp, 'testfile')
        self.assertRaises(ValidationError, utils.attach_datestamp, 'test.file')

    def test_filename_should_be_cleaned_first_cn(self):
        self.assertRaises(ValidationError, utils.attach_datestamp, '测试文件')
        self.assertRaises(ValidationError, utils.attach_datestamp, '测试.file')

    def test_attach_datestamp(self):
        filename = utils.attach_datestamp('testfile.csv')
        self.assertRegexpMatches(filename, r'testfile_[0-9]{8}.csv')

    def test_attach_datestamp_cn(self):
        filename = utils.attach_datestamp('测试文件.csv')
        self.assertRegexpMatches(filename, r'测试文件_[0-9]{8}.csv')


class GenerateFileTests(TestCase):
    def test_can_generate_filename_from_model(self):
        queryset = create_student_and_get_queryset()
        self.assertEqual(utils.generate_filename(queryset), 'student.csv')
        self.assertRegexpMatches(utils.generate_filename(queryset, True), r'student_[0-9]{8}.csv')
