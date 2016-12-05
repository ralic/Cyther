
"""
This module holds utilities to search for items, whether they be files or
textual patterns, that cyther will use for compilation. This module is
designed to be relatively easy to use and make a very complex task much less so
"""

import os
import re
import shutil

MULTIPLE_FOUND = "More than one pattern found for regex pattern: '{}' " \
                 "for output:\n\t{}"
NONE_FOUND = "No matches for pattern '{}' could be found in output:\n\t{}"
ASSERT_ERROR = "The search result:\n\t{}\nIs not equivalent to the assert " \
               "test provided:\n\t{}"

RUNTIME_PATTERN = r"(?<=lib)(?P<content>.+?)(?=\.so|\.a)"
POUND_PATTERN = r"#\s*@\s?[Cc]yther +(?P<content>.+?)\s*?(\n|$)"
TRIPPLE_PATTERN = r"(?P<quote>'{3}|\"{3})(.|\n)+?@[Cc]yther\s+" \
                  r"(?P<content>(.|\n)+?)\s*(?P=quote)"
VERSION_PATTERN = r"[Vv]ersion:?\s+(?P<content>([0-9]+\.){1,}((dev)?[0-9]+))"


def where(cmd, path=None):
    """
    A function to wrap shutil.which for universal usage
    """
    raw_result = shutil.which(cmd, os.X_OK, path)
    if raw_result:
        return os.path.abspath(raw_result)
    else:
        raise ValueError("Could not find '{}' in the path".format(cmd))


def _get_content(pattern, string):
    output = []
    for match in re.finditer(pattern, string):
        output.append(match.group('content'))
    return output


def _process_no_output(pattern, output, error_if_none, none_message, default):
    if error_if_none:
        if not none_message:
            none_message = NONE_FOUND.format(pattern, output)
        raise LookupError(none_message)
    else:
        if default:
            output = default
        else:
            output = None
    return output


def _process_output(pattern, output, condense, default, multiple_message,
                    allow_only_one):
    if condense:
        output = list(set(output))

    if allow_only_one:
        if len(output) > 1:
            if default:
                output = default
            else:
                if not multiple_message:
                    multiple_message = MULTIPLE_FOUND.format(pattern,
                                                             output)
                raise ValueError(multiple_message)
        output = output[0]

    return output


def _assert_output(output, assert_equal, assert_message):
    sorted_output = sorted(output)
    sorted_assert = sorted(assert_equal)
    if sorted_output != sorted_assert:
        if not assert_message:
            assert_message = ASSERT_ERROR.format(sorted_output,
                                                 sorted_assert)
        raise ValueError(assert_message)


def extract(pattern, string, assert_equal=False,
            allow_only_one=False, condense=False,
            error_if_none=False, default=None,
            multiple_message=None,
            none_message=None,
            assert_message=None):
    """
    Used by extract to filter the entries in the searcher results
    """
    output = _get_content(pattern, string)

    if not output:
        output = _process_no_output(pattern, output, error_if_none,
                                    none_message, default)
    else:
        output = _process_output(pattern, output, condense, default,
                                 multiple_message, allow_only_one)

    if assert_equal:
        _assert_output(output, assert_equal, assert_message)
    else:
        return output


def extractRuntime(runtime_dirs):
    """
    Used to find the correct static lib name to pass to gcc
    """
    names = [str(item) for name in runtime_dirs for item in os.listdir(name)]
    string = '\n'.join(names)
    result = extract(RUNTIME_PATTERN, string,
                     condense=True, error_if_none=True)
    return result


def extractAtCyther(path):
    """
    Extracts the '@cyther' code to be run as a script after compilation
    """
    with open(path) as file:
        string = file.read()

    found_pound = extract(POUND_PATTERN, string)
    found_tripple = extract(TRIPPLE_PATTERN, string)
    all_found = found_pound + found_tripple
    code = '\n'.join([item for item in all_found])

    return code


def extractVersion(string, default='?'):
    """
    Extracts a three digit standard format version number
    """
    error_if_none = not bool(default)
    return extract(VERSION_PATTERN, string, condense=True, default=default,
                   error_if_none=error_if_none, allow_only_one=True)
