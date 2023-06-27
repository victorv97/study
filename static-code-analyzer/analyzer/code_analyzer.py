import pathlib
import sys
import ast
import re
from collections import defaultdict


# -------------------------------------------------------
#  Simple checks
# -------------------------------------------------------

SNAKE_CASE_PATTERN = r'[a-z_]*_*[a-z_0-9]*$'
CAMEL_CASE_PATTERN = r'[A-Z][A-Za-z0-9]*$'


def check_length(line):
    return len(line) > 79


def check_indentation(line):
    indentation = re.sub(r'\S.*', '', line)
    return indentation.count(' ') % 4 != 0


def check_semicolon(line):
    semicol_idx = line.find(';')
    return semicol_idx != -1 and '#' not in line[0:semicol_idx] and line[0:semicol_idx].count("'") % 2 != 1


def check_inline_comment(line):
    if not line.startswith('#') and '#' in line:
        comment_idx = line.find('#')
        return line[comment_idx - 2:comment_idx].count(' ') < 2


def check_todo(line):
    if '#' in line:
        comment_idx = line.find('#')
        return 'todo' in line[comment_idx:].lower()


def check_first_blank_lines(prev_lines):
    assert len(prev_lines) <= 3
    if prev_lines and all([line == '' for line in prev_lines]):
        return True
    # return prev_lines and all([line == '' for line in prev_lines])


def check_spaces_after_statement(line):
    m = re.match(r'.*(class|def)', line)
    if m:
        if not re.match(r'\s*(class|def)\s\S', line):
            return m.group(0)


def check_camel_case(name):
    return name and (re.match(CAMEL_CASE_PATTERN, name) is None)


def check_snake_case(name):
    return name and (re.match(SNAKE_CASE_PATTERN, name) is None)


def check_mutable_arg(default_arg_node):
    return isinstance(default_arg_node, (ast.List, ast.Dict, ast.Set))


# -------------------------------------------------------
#  Analyzer class
# -------------------------------------------------------

class CodeAnalyzer:

    def __init__(self, code: str):
        self._tree = ast.parse(code)
        self._code_lines = code.splitlines()
        self._messages = {
            'S001': {'msg': "Too long"},
            'S002': {'msg': "Indentation is not a multiple of four"},
            'S003': {'msg': "Unnecessary semicolon after a statement"},
            'S004': {'msg': "Less than two spaces before inline comments"},
            'S005': {'msg': "TODO found"},
            'S006': {'msg': "More than two blank lines preceding a code line"},
            'S007': {'msg': "Too many spaces after '{}'"},
            'S008': {'msg': "Class name '{class_name}' should be written in CamelCase"},
            'S009': {'msg': "Function name '{fun_name}' should be written in snake_case"},
            'S010': {'msg': "Argument name '{arg_name}' should be written in snake_case"},
            'S011': {'msg': "Variable '{var_name}' should be written in snake_case"},
            'S012': {'msg': "The default argument value is mutable"},
        }
        self._line_checks = {
            'S001': check_length,
            'S002': check_indentation,
            'S003': check_semicolon,
            'S004': check_inline_comment,
            'S005': check_todo,
            'S007': check_spaces_after_statement,
        }
        self._lines_msgs_map = defaultdict(set)

    def _check_line(self, line_num, line):
        # do line checks
        for key, check in self._line_checks.items():
            res = check(line)
            if res:
                self._lines_msgs_map[line_num].add(key + ' ' + self._messages[key]['msg'].format(res))

        # do blank lines check
        if check_first_blank_lines(self._code_lines[line_num - 4:line_num - 1]):
            self._lines_msgs_map[line_num].add('S006' + ' ' + self._messages['S006']['msg'])

    def _go_through_lines(self):
        for line_num, line in enumerate(self._code_lines, start=1):
            self._check_line(line_num, line)

    def _go_through_tree(self):
        for node in ast.walk(self._tree):
            # check function
            if isinstance(node, ast.FunctionDef):
                fun_name = node.name
                # check function name
                if check_snake_case(fun_name):
                    self._lines_msgs_map[node.lineno].add(
                        'S009' + ' ' + self._messages['S009']['msg'].format(fun_name=fun_name))

                # check arguments name
                for argument in node.args.args:
                    arg_name = argument.arg
                    if check_snake_case(arg_name):
                        self._lines_msgs_map[node.lineno].add(
                            'S010' + ' ' + self._messages['S010']['msg'].format(arg_name=arg_name))

                # check if default arguments are mutable
                for default in node.args.defaults:
                    if check_mutable_arg(default):
                        self._lines_msgs_map[node.lineno].add('S012' + ' ' + self._messages['S012']['msg'])

                # check variables names in function
                for item in node.body:
                    if not isinstance(item, ast.Assign):
                        continue

                    for target in item.targets:
                        if not isinstance(target, ast.Name):
                            continue

                        var_name = target.id
                        if check_snake_case(var_name):
                            self._lines_msgs_map[target.lineno].add(
                                'S011' + ' ' + self._messages['S011']['msg'].format(var_name=var_name))

            # check class name
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                if check_camel_case(class_name):
                    self._lines_msgs_map[node.lineno].add(
                        'S008' + ' ' + self._messages['S008']['msg'].format(class_name=class_name))

    def report(self):
        return self._lines_msgs_map

    def analyze(self):
        self._go_through_lines()
        self._go_through_tree()


# -------------------------------------------------------
#  Process files
# -------------------------------------------------------

def print_messages(file_path, messages):
    for line_num, msg_set in sorted(messages.items()):
        for msg in sorted(msg_set):
            print(f'{file_path}: Line {line_num}: {msg}')


def get_all_files(path):
    root = pathlib.Path(path)
    files_list = [str(p) for p in root.rglob('*.py')]
    return files_list


def get_input():
    file_path = sys.argv[1]
    if pathlib.Path(file_path).is_dir():
        files = get_all_files(file_path)
    else:
        files = [file_path]
    return sorted(files)


def process_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    analyzer = CodeAnalyzer(code)
    analyzer.analyze()
    msgs = analyzer.report()
    print_messages(file_path, msgs)


def main():
    files = get_input()

    for file in files:
        process_file(file)


if __name__ == '__main__':
    main()
