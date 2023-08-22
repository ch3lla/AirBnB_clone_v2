"""
Contains tests for Base class
"""

import unittest
import inspect
import pep8
import json
import console
import sys
import os
from os import getenv
from models.base_model import BaseModel
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from models.engine.file_storage import FileStorage
from io import StringIO
from unittest.mock import patch
HBNBCommand = console.HBNBCommand


class TestBaseDocs(unittest.TestCase):
    """Tests to check the documentation and style of COnsole module"""

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_base(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        res = pep8style.check_files(['tests/test_console.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Tests for the module docstring"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_class_docstring(self):
        """Tests for the Base Class docstring"""
        self.assertTrue(len(HBNBCommand.__doc__) >= 1)


class TestHBNBCommand_global(unittest.TestCase):
    """Unittests for testing HBNB console"""

    def setUp(self):
        """SetUp to avoid overwriting file.json"""
        if os.path.isfile('file.json'):
            os.rename("file.json", "file.jsonSAVE")

    def tearDown(self):
        """TearDown to avoid overwriting file.json"""
        if os.path.isfile('file.json'):
            os.remove("file.json")
        if os.path.isfile('file.jsonSAVE'):
            os.rename("file.jsonSAVE", "file.json")

    def test_empty_line(self):
        """Tests empty line"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", f.getvalue().strip())

    def test_help_quit(self):
        """Tests help quit"""
        h = "Exits the program with formatting"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h, f.getvalue().strip())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not supported in db mode")
    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(f.getvalue().strip()))
            testKey = "User.{}".format(f.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(f.getvalue().strip()))
            testKey = "State.{}".format(f.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(f.getvalue().strip()))
            testKey = "City.{}".format(f.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(f.getvalue().strip()))
            testKey = "Amenity.{}".format(f.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(f.getvalue().strip()))
            testKey = "Place.{}".format(f.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(f.getvalue().strip()))
            testKey = "Review.{}".format(f.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_show1(self):
        """Tests show function"""
        h = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(h, f.getvalue().strip())

    def test_show2(self):
        """Tests show function"""
        h = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Matt"))
            self.assertEqual(h, f.getvalue().strip())

    def test_show3(self):
        """Tests show function"""
        h = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(h, f.getvalue().strip())

    def test_show4(self):
        """Tests show function"""
        h = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(h, f.getvalue().strip())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not supported in db mode")
    def test_show5(self):
        """Tests show function"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "show BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), f.getvalue().strip())

    def test_destroy1(self):
        """Tests destroy function"""
        h = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(h, f.getvalue().strip())

    def test_destroy2(self):
        """Tests destroy function"""
        h = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Matt"))
            self.assertEqual(h, f.getvalue().strip())

    def test_destroy3(self):
        """Tests destroy function"""
        h = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(h, f.getvalue().strip())

    def test_destroy4(self):
        """Tests destroy function"""
        h = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(h, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(h, f.getvalue().strip())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not supported in db mode")
    def test_update_with_all_classes(self):
        """ Test with all classes """
        c = {
            'User': User, 'City': City, 'State': State, 'Amenity': Amenity,
            'Place': Place, 'Review': Review,
            'BaseModel': BaseModel
        }
        for i in c.keys():
            o = c[i]()
            storage.new(o)
            storage.save()
            with patch('sys.stdout', new=StringIO()) as x:
                s = "Matt"
                HBNBCommand().onecmd("update {} {} xd {}".format(i, o.id, s))
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("show {} {}".format(i, o.id))
            self.assertTrue("Matt" in f.getvalue())

    def test_del_with_all_classes(self):
        """ Test with all classes """
        c = {
            'User': User, 'City': City, 'State': State, 'Amenity': Amenity,
            'Place': Place, 'Review': Review,
            'BaseModel': BaseModel
        }
        for i in c.keys():
            o = c[i]()
            with patch('sys.stdout', new=StringIO()) as x:
                s = "Matt"
                uo = o.id
            with patch('sys.stdout', new=StringIO()) as z:
                HBNBCommand().onecmd("destroy {} {}".format(i, o.id))
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("show {} {}".format(i, uo))
            self.assertEqual("** no instance found **\n",  f.getvalue())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not supported in db mode")
    def test_all_with_all_classes(self):
        """ Test with all classes """
        c = {
            'User': User, 'City': City, 'State': State, 'Amenity': Amenity,
            'Place': Place, 'Review': Review,
            'BaseModel': BaseModel
        }
        if os.path.exists("file.json"):
            os.remove("file.json")
        for i in c.keys():
            o = c[i]()
            storage.new(o)
            storage.save()
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("all {}".format(i))
            self.assertTrue(str(o) in f.getvalue())

    def test_all_class_doesnt_exist_missing_err_msg(self):
        """ Test that all return a msg error """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all udzhdz")
        self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_update_name_class_missing_err_msg(self):
        """ Test that update return a msg error """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        self.assertEqual("** class name missing **", f.getvalue().strip())

    def test_update_wrong_name_class_err_msg(self):
        """ Test that update return a msg error """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update ijd")
        self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_update_no_id_given_err_msg(self):
        """ Test that update return a msg error """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
        self.assertEqual("** instance id missing **", f.getvalue().strip())

    def test_update_instance_doesnt_exist_err_msg(self):
        """ Test that update return a msg error """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 654448")
        self.assertEqual("** no instance found **", f.getvalue().strip())

    def test_dot_del_with_all_classes(self):
        """ Test with all classes """
        c = {
            'User': User, 'City': City, 'State': State, 'Amenity': Amenity,
            'Place': Place, 'Review': Review,
            'BaseModel': BaseModel
        }
        for i in c.keys():
            o = c[i]()
            with patch('sys.stdout', new=StringIO()) as x:
                s = "Matt"
                uo = o.id
            with patch('sys.stdout', new=StringIO()) as z:
                HBNBCommand().onecmd("{}.destroy(\"{}\")".format(i, o.id))
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("show {} {}".format(i, uo))
            self.assertEqual("** no instance found **\n",  f.getvalue())
