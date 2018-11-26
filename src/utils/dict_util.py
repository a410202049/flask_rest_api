#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys

import re

import logging

logger = logging.getLogger(__name__)


class CheckDictError(Exception):

    def __init__(self, msg, illegal_value_notice, *args, **kwargs):
        super(CheckDictError, self).__init__(msg, *args, **kwargs)

        self.illegal_value_notice = illegal_value_notice


class BaseInputType(object):
    DEFAULT_NULLABEL = False

    def __init__(self, nullable=DEFAULT_NULLABEL, accept_class=None, illegal_value_notice=None, sub_rules=None):
        self.nullable = nullable
        self.accept_class = accept_class
        self.illegal_value_notice = illegal_value_notice
        self.sub_rules = sub_rules

    def check(self, value):
        if self.value_is_null(value):
            return self.nullable, None

        if self.accept_class is not None and not isinstance(value, self.accept_class):
            return False, None

        try:
            value = self.convert(value)
        except ValueError:
            return False, None

        result = self.inner_check(value)
        return result, value if result else None

    def value_is_null(self, value):
        return value is None

    def convert(self, value):
        return value

    def inner_check(self, value):
        return True


class SimpleRule(BaseInputType):
    pass


class IntRule(BaseInputType):
    def __init__(self, min_val=-sys.maxint - 1, max_val=sys.maxint,
                 nullable=BaseInputType.DEFAULT_NULLABEL, accept_class=(int, long, basestring),
                 illegal_value_notice=None):
        super(IntRule, self).__init__(nullable, accept_class, illegal_value_notice)

        self.min_val = min_val
        self.max_val = max_val

    def inner_check(self, value):
        if self.nullable and value is None:
            return True

        return self.min_val <= value <= self.max_val

    def convert(self, value):
        return int(value) if value is not None else None


class BoolRule(BaseInputType):
    def __init__(self, nullable=BaseInputType.DEFAULT_NULLABEL, accept_class=(bool, basestring, int),
                 illegal_value_notice=None):
        super(BoolRule, self).__init__(nullable, accept_class, illegal_value_notice)

    def inner_check(self, value):
        return True

    def convert(self, value):
        if value is None:
            return None

        if isinstance(value, basestring):
            return value.lower() == 'true'

        return bool(value)


class StrRule(BaseInputType):
    def __init__(self, reg_exp=None, nullable=BaseInputType.DEFAULT_NULLABEL, accept_class=None,
                 illegal_value_notice=None):
        super(StrRule, self).__init__(nullable, accept_class, illegal_value_notice)

        self.reg_exp = re.compile(reg_exp) if reg_exp is not None else None

    def inner_check(self, value):
        if self.reg_exp is None or value is None:
            return True
        return self.reg_exp.match(value) is not None

    def value_is_null(self, value):
        return not value

    def convert(self, value):
        return value if value is None or isinstance(value, basestring) else str(value)


class FloatRule(BaseInputType):
    def __init__(self, min_val=sys.float_info.min, max_val=sys.float_info.max,
                 nullable=BaseInputType.DEFAULT_NULLABEL, accept_class=(float, int, basestring),
                 illegal_value_notice=None):
        super(FloatRule, self).__init__(nullable, accept_class, illegal_value_notice)

        self.min_val = min_val
        self.max_val = max_val

    def inner_check(self, value):
        return self.min_val <= value <= self.max_val

    def convert(self, value):
        if value is None:
            return None

        return float(value)


class EnumRule(BaseInputType):
    def __init__(self, enum_type, nullable=BaseInputType.DEFAULT_NULLABEL, accept_class=(int, basestring),
                 illegal_value_notice=None):
        super(EnumRule, self).__init__(nullable, accept_class, illegal_value_notice)
        self.enum_type = enum_type

    def inner_check(self, value):
        return value in self.enum_type.values()

    def convert(self, value):
        if value is None:
            return None

        return self.enum_type.value_of(value, None)


class DictRule(BaseInputType):
    def __init__(self, nullable=BaseInputType.DEFAULT_NULLABEL, illegal_value_notice=None, sub_rules=None):
        super(DictRule, self).__init__(nullable, dict, illegal_value_notice, sub_rules)


class ListRule(BaseInputType):
    def __init__(self, nullable=BaseInputType.DEFAULT_NULLABEL, illegal_value_notice=None, item_rule=None, sub_rules=None):
        super(ListRule, self).__init__(nullable, (list, tuple), illegal_value_notice, sub_rules)
        self.item_rule = item_rule

    def convert(self, value):
        if self.item_rule:
            return [self.item_rule.convert(item) for item in value]
        else:
            return super(ListRule, self).convert(value)

    def inner_check(self, value):
        if self.item_rule:
            for item in value:
                if not self.item_rule.inner_check(item):
                    return False

        return True


def _compile_rule(rules, parent=None):
    """
    convert rule map to rule tree
    rule node contains key, rule, children
    :param rules: rule map
    :return: rule tree
    """

    if not isinstance(rules, dict):
        raise RuntimeError('rule format error, except dict got %s' % type(rules))

    root_node = parent or {'children': {}, 'path': ''}

    for key in rules:
        current_node = root_node

        rule = rules[key]

        ks = key.split('.')
        for k in ks:
            if k not in current_node['children']:
                current_node['children'][k] = {'key': k, 'children': {}}

            current_node = current_node['children'][k]

        current_node['rule'] = rule
        current_node['path'] = '%s.%s' % (root_node['path'], key) if root_node['path'] else key

        if rule.sub_rules:
            _compile_rule(rule.sub_rules, current_node)

    return root_node


def _check_value(value, rule_node):
    key = rule_node.get('key', None)
    rule = rule_node.get('rule', None)
    path = rule_node.get('path', key)
    children = rule_node.get('children', {})

    if rule:
        result, value = rule.check(value)
        if not result:
            message = value or rule.illegal_value_notice or u'{0}取值不符合约定'.format(path)
            return False, message

    if len(children) > 0 and value is not None:
        for ck in children:
            child = children[ck]

            if isinstance(value, dict):
                result, cv = _check_value(value.get(ck, None), child)
                if not result:
                    return False, cv

                if cv is not None:
                    value[ck] = cv
            elif isinstance(value, (tuple, list)):
                for item in value:
                    result, cv = _check_value(item.get(ck, None), child)
                    if not result:
                        return False, cv

                    if cv is not None:
                        item[ck] = cv

    return True, value


def check_dict(req_dict, rules):
    rule_tree = _compile_rule(rules)
    return _check_value(req_dict, rule_tree)


def get_value(mapper, key_path, default_value=None):
    if not mapper:
        return default_value

    current_node = mapper
    keys = key_path.split('.')

    for k in keys[:-1]:
        if k in current_node:
            current_node = current_node[k]
        else:
            # element not exist, just return default value
            return default_value

    return current_node.get(keys[-1], default_value) if current_node else None


def set_value(mapper, key_path, value):
    current_node = mapper
    keys = key_path.split('.')

    for k in keys[:-1]:
        if k not in current_node:
            current_node[k] = {}

        current_node = current_node[k]

    current_node[keys[-1]] = value


# def to_str(mapper):
#     keys = mapper.keys()
#     for k in keys:
#         if isinstance(k, unicode):
#             uk = k
#             k = to_str


def pop_value(mapper, key_path, default_value=None):
    current_node = mapper
    keys = key_path.split('.')

    for k in keys[:-1]:
        if k in current_node:
            current_node = current_node[k]
        else:
            return default_value

    return current_node.pop(keys[-1], default_value)


if __name__ == '__main__':
    sample_rule = {
        'class': StrRule('.+', nullable=False),
        'grade': StrRule('.+', nullable=True),
        'students': SimpleRule(nullable=True, accept_class=(tuple, list)),
        'students.name': StrRule('.+', nullable=False),
        'students.age': IntRule(1, 99, nullable=True),
        'school': SimpleRule(nullable=False, accept_class=(dict,)),
        'school.name': StrRule('.+', nullable=True),
        'school.code': StrRule('.+', nullable=False),
        'amt': FloatRule(nullable=False),
        'binded': BoolRule(nullable=False),
        'names': StrRule('.+', nullable=False),
        'password': StrRule('^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,32}$', nullable=True,
                            illegal_value_notice=u'密码由6-32位字符或者数字组成')
    }

    sample_rule2 = {
        'class': StrRule('.+', nullable=False),
        'grade': StrRule('.+', nullable=True),
        'students': ListRule(nullable=True, sub_rules={
            'name': StrRule('.+', nullable=False),
            'age': IntRule(1, 99, nullable=True),
        }),
        'school': DictRule(nullable=False, sub_rules={
            'name': StrRule('.+', nullable=True),
            'code': StrRule('.+', nullable=False),
        }),
        'amt': FloatRule(nullable=False),
        'binded': BoolRule(nullable=False),
        'names': ListRule(nullable=False, item_rule=StrRule('.+', nullable=False)),
        'password': StrRule('^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,32}$', nullable=True,
                            illegal_value_notice=u'密码由6-32位字符或者数字组成')
    }

    sample_value = {
        'class': '一班',
        'grade': '一年',
        'students': [
            {
                'name': '学生1',
                'age': 12
            },
            {
                'name': '学生2',
                'age': 13
            },
            {
                'name': '学生3',
                'age': '14'
            },
        ],
        'school': {
            'name': '测试学校',
            'code': '123456'
        },
        'amt': 12.34,
        'binded': 'true',
        'names': ['a', 'b', 'c', 'd', 4],
        'password': ""
    }

    print check_dict(sample_value.copy(), sample_rule)
    print check_dict(sample_value.copy(), sample_rule2)
    print get_value(sample_value, 'class')
    print get_value(sample_value, 'school.name')
    print get_value(sample_value, 'school.code')
    print set_value(sample_value, 'school.code', '123')
    print get_value(sample_value, 'school.code')
