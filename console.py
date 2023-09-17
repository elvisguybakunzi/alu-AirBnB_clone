#!/usr/bin/python3
"""Module for the console application
"""
from cmd import Cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(Cmd):
    """Console-based interpreter for different commands"""
    prompt = "(hbnb) "
    classes = ["BaseModel"]

    def __create_key(self, class_name, instance_id):
        """Helper function to construct key
        args: class_name, instance_id
        returns: string
        """
        return '{}.{}'.format(class_name, instance_id)

    def __get_args(self, line):
        """Helper function to parse line into args
        args are delimited by spaces and double quotes
        returns a list of args
        args: line
        returns: list of args
        """
        args = []
        open_quote = False
        curr_arg = ""

        for char in line:
            if char == '"':
                if open_quote:
                    # End of quoted string
                    args.append(curr_arg)
                    curr_arg = ""
                    open_quote = False
                else:
                    # Beginning of quoted string
                    open_quote = True
            elif char == " ":
                if open_quote:
                    # Quoted string so we add the space to curr_arg
                    curr_arg += char
                else:
                    # Separate argument
                    if curr_arg != "":
                        # We only append the string if there's a value
                        args.append(curr_arg)
                        curr_arg = ""
            else:
                # It's a normal character, which we simply add to the current string
                curr_arg += char

        # If curr_arg still has text
        # And quote is not open
        # Add curr_arg to the result
        if len(curr_arg) and not open_quote:
            args.append(curr_arg)

        return args

    def __validate_class_name(self, class_name):
        """Used to validate the class name
        Returns True if valid
        Returns False if invalid and prints the error message
        """
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return False
        else:
            return True

    def __validate_instance_id(self, valid_class_name, instance_id):
        """Used to validate the instance id for a given valid class name
        Returns True if valid
        Returns False if invalid and prints the error message
        """
        key = self.__create_key(valid_class_name, instance_id)
        models = storage.all()
        model = models.get(key)

        if model is None:
            print("** no instance found **")
            return False
        else:
            return True

    def __get_objects(self, class_name):
        if class_name == "":
            # If no class name has been supplied we return everything
            return storage.all()
        else:
            # If a class name has been supplied we validate it
            if self.__validate_class_name(class_name):

                # All objects
                objects = storage.all()

                # Filtered objects
                filtered_objects = {}

                # We filter to get only the objects with the class we want
                for key, value in objects.items():
                    if value.__class__.__name__ == class_name:
                        filtered_objects[key] = value

                return filtered_objects
            else:
                return {}

    def do_create(self, line):
        """Creates an instance
        args: class_name
        e.g.: create City
        """
        args = self.__get_args(line)

        if len(args) == 1:
            class_name = args[0]
            if self.__validate_class_name(class_name):
                bm = BaseModel()
                bm.save()
                print(bm.id)
        else:
            print("** class name missing **")

    def do_show(self, line):
        """Shows an instance
        args: class_name, instance_id
        e.g.: show City 1212
        """
        args = self.__get_args(line)
        print(args)

        if len(args) == 2:
            class_name, instance_id = args
            if self.__validate_class_name(class_name):
                if self.__validate_instance_id(class_name, instance_id):
                    key = self.__create_key(class_name, instance_id)
                    instance = storage.all().get(key)
                    print(instance)
        elif len(args) == 1:
            print('** instance id missing **')
        else:
            print('** class name missing **')

    def do_destroy(self, line):
        """Destroys an instance
        args: class_name, instance_id
        e.g.: destroy City 1212
        """
        args = self.__get_args(line)

        if len(args) == 2:
            class_name, instance_id = args
            if self.__validate_class_name(class_name):
                if self.__validate_instance_id(class_name, instance_id):
                    key = self.__create_key(class_name, instance_id)
                    del storage.all()[key]
                    storage.save()
        elif len(args) == 1:
            print('** instance id missing **')
        else:
            print('** class name missing **')

    def do_all(self, line):
        args = self.__get_args(line)
        class_name = args[0] if len(args) == 1 else ""
        models = self.__get_objects(class_name).values()
        models_str = list(map(lambda m: str(m), models))
        print(models_str)

    def do_update(self, line):
        """Updates an attribute on a specified instance
        args: class_name, instance_id, attribute_name, attribute_value
        e.g.: update City 1212 name "Denver"
        """
        args = self.__get_args(line)
        if len(args) >= 4:
            # Extract args
            class_name, instance_id, attr_name, attr_val, *rest = args

            # Validate class
            if self.__validate_class_name(class_name):

                # Validate id
                if self.__validate_instance_id(class_name, instance_id):

                    # Construct key and get instance
                    key = self.__create_key(class_name, instance_id)
                    instance = storage.all().get(key)

                    # Get attribute data type from instance and cast value to that type
                    attr_type = type(getattr(instance, attr_name))
                    cast_attr_val = eval(attr_type)(attr_val)

                    # Set the attribute to cast value
                    setattr(instance, attr_name, cast_attr_val)
        elif len(args) == 3:
            print('** value missing **')
        elif len(args) == 2:
            print('** attribute name missing **')
        elif len(args) == 1:
            print('** instance id missing **')
        else:
            print('** class name missing **')

    def do_quit(self, arg):
        """Quit the program"""
        return True

    def do_EOF(self, arg):
        """Quit the program"""
        return True

    def emptyline(self):
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
