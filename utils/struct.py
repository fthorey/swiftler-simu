#!/usr/bin/python
# coding: utf-8

class Struct:
    """This class describes structures with arbitrary fields.
       It is used, e.g. for the communication between the supervisor and the UI.

       Example::

            p = Struct()
            p.goal = Struct()
            p.goal.x = 0.0
            p.goal.y = 0.5
            p.velocity = Struct()
            p.velocity.v = 0.2
            p.gains = Struct()
            p.gains.kp = 10.0
            p.gains.ki = 2.0
            p.gains.kd = 0.0

    """
    def __str__(self):
        def str_field(key,value):
            indent = " "*(len(str(key)) + 3)
            str_value = str(value)
            if isinstance(value,Struct):
                # create indent
                str_value = str_value.replace('\n','\n'+indent)
            return "{}: {}".format(key,str_value)


        return "Struct\n {}".format("\n ".join((str_field(k,v) for k,v in self.__dict__.items())))
