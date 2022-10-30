#!/usr/bin/python3
'''
Module: console.py
'''

import cmd
from models import storage
import re
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class HBNBCommand(cmd.Cmd):
    '''defines the entry point of the command interpreter'''
    prompt = "(hbnb)"
    model_classes = {
            'BaseModel': BaseModel, 'User': User,
            'Amenity': Amenity, 'City': City, 'State': State,
            'Place': Place, 'Review': Review
            }

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, arg):
        ''' close program and save program
        using CTRL + D
        '''
        print("")
        return True

    def do_help(self, arg):
        '''help center command '''
        return super().do_help(arg)

    def emptyline(self):
        """defines an empty function"""
        pass

    def do_create(self, arg):
        '''Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Ex: $ create BaseModel
        '''
        tokens = arg.split()
        if not HBNBCommand.validator(tokens, check_id=False):
            return
        obj = HBNBCommand.model_classes[tokens[0]]()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        '''
        Prints the string representation of an
        instance based on the class name and id.
        Ex: $ show BaseModel 1234-1234-1234.
        '''
        tokens = arg.split()
        if not HBNBCommand.validator(tokens, check_id=True):
            return
        storage.reload()
        objs = storage.all()
        key = "{}.{}".format(tokens[0], tokens[1])
        obj_instance = objs.get(key, None)
        if obj_instance is None:
            print("** no instance found **")
            return
        print(obj_instance)

    def do_destroy(self, arg):
        '''
        Deletes an instance based on the class name
        and id (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234
        '''
        tokens = arg.split()
        if not HBNBCommand.validator(tokens, check_id=True):
            return
        storage.reload()
        objs = storage.all()
        key = "{}.{}".format(tokens[0], tokens[1])
        obj_instance = objs.get(key, None)
        if obj_instance is None:
            print("** no instance found **")
            return
        del objs[key]
        storage.save()

    def do_all(self, arg):
        '''
        Prints all string representation of all instances
        based or not on the class name.
        Ex: $ all BaseModel or $ all
        '''
        tokens = arg.split()
        storage.reload()
        objs = storage.all()
        if len(tokens) < 1:
            print(["{}".format(str(v)) for _, v in objs.items()])
            return
        if tokens[0] not in HBNBCommand.model_classes.keys():
            print("** class doesn't exist **")
            return
        else:
            print(["{}".format(str(v))
                  for _, v in objs.items() if type(v).__name__ == tokens[0]])
            return

    def do_update(self, arg):
        tokens = arg.split()
        if not HBNBCommand.validator(tokens, check_id=True):
            return
        storage.reload()
        objs = storage.all()
        key = "{}.{}".format(tokens[0], tokens[1])
        obj_instance = objs.get(key, None)
        if obj_instance is None:
            print("** no instance found **")
            return

        matcher = re.findall(r"{.*}", arg)
        if matcher:
            payload = None
            try:
                payload: dict = json.loads(matcher[0])
            except Exception:
                print("** invalid syntax")
                return
            for k, v in payload.items():
                setattr(obj_instance, k, v)
            storage.save()
            return

        if not HBNBCommand.validate_attrs(tokens):
            return
        finder = re.findall(r"^[\"\'](.*?)[\"\']", tokens[3])
        if finder:
            setattr(obj_instance, tokens[2], finder[0])
        else:
            vals = tokens[3].split()
            setattr(obj_instance, tokens[2], HBNBCommand.parse_str(vals[0]))
        storage.save()

    def precmd(self, arg):
        """
        Instructions to execute before arguments are interpreted
        """
        if not arg:
            return '\n'

        pattern = re.compile(r"(\w+)\.(\w+)\((.*)\)")
        match_list = pattern.findall(arg)
        if not match_list:
            return super().precmd(arg)

        matcher = match_list[0]
        if not matcher[2]:
            if matcher[1] == "count":
                instance_objs = storage.all()
                print(len([
                    v for _, v in instance_objs.items()
                    if type(v).__name__ == matcher[0]]))
                return "\n"
            return "{} {}".format(matcher[1], matcher[0])
        else:
            args = matcher[2].split(", ")
            if len(args) == 1:
                return "{} {} {}".format(
                    matcher[1], matcher[0],
                    re.sub("[\"\']", "", matcher[2]))
            else:
                json_match = re.findall(r"{.*}", matcher[2])
                if (json_match):
                    return "{} {} {} {}".format(
                        matcher[1], matcher[0],
                        re.sub("[\"\']", "", args[0]),
                        re.sub("\'", "\"", json_match[0]))
                return "{} {} {} {} {}".format(
                    matcher[1], matcher[0],
                    re.sub("[\"\']", "", args[0]),
                    re.sub("[\"\']", "", args[1]), args[2])

    def validate_attrs(tokens):
        """ validate classname attributes and values."""
        if len(tokens) < 3:
            print("** attribute name missing **")
            return False
        if len(tokens) < 4:
            print("** value missing **")
            return False
        return True

    def validator(tokens, check_id=False):
        '''validate class entry'''
        if not tokens:
            print("* class name missing **")
            return False
        if tokens[0] not in HBNBCommand.model_classes.keys():
            print("** class doesn't exist **")
            return False
        if len(tokens) < 2 and check_id:
            print("** instance id missing **")
            return False
        return True

    def parse_str(token):
        """Parse token to str or int or float"""
        parsed = re.sub("\"", "", token)
        if HBNBCommand.is_int(parsed):
            return int(parsed)
        elif HBNBCommand.is_float(parsed):
            return float(parsed)
        else:
            return token

    def is_float(tok):
        """Checks tok is float"""
        try:
            x = float(tok)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def is_int(tok):
        """Check that tok is integer"""
        try:
            x = float(tok)
            y = int(x)
        except (TypeError, ValueError):
            return False
        else:
            return x == y


if __name__ == '__main__':
    HBNBCommand().cmdloop()
