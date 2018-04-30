# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A detailed example of how to create a flag definition function."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import flags

from official.utils.flags._conventions import help_wrap
from official.utils.flags._conventions import to_choices_str


def define_example(foo=True, bar=True):  # pylint: disable=blacklisted-name
  """Register a flag called `--foo`.

  Args:
    foo: Create an example flag.
    bar: Create another example flag.

  Returns:
    A list of key flags; these flags will show up in --help
  """

  key_flags = []

  if foo:
    choices = ["fizz", "bang"]

    # to_choices_str is a convenience function to make pretty (and consistent)
    # help strings.
    choices_str = to_choices_str(choices)
    flags.DEFINE_string(
        name="foo",
        short_name="f",  # define an abbreviation for the lazy.
        default="fizz",  # default is required, but may be None

        # help_wrap is a string function that allows enforcement of a shared
        # set of style conventions for all help messages.
        help=help_wrap(
            "A flag of no particular note\n{}".format(choices_str)
        ),
    )

    # By marking a flag as a key_flag, you indicate that it should appear in
    # --help. (All flags appear in --helpfull) Due to the way that absl handles
    # key flags, the declaration cannot take place in this file. Instead it is
    # returned to flags/core.py for declaration.
    key_flags.append("foo")

    # absl supports arbitrary validation of flags. Marking a function with
    # the flags.validator decorator registers it with absl which will run all
    # validator functions after flag parsing. Validator functions should return
    # True if the flag passes muster.
    val_msg = "--foo should be one of: {}".format(", ".join(choices))
    @flags.validator("foo", message=val_msg)
    def _foo_check(foo_flag):  # pylint: disable=unused-variable
      return foo_flag in choices

  if bar:
    assert foo, "bar depends on foo"
    choices = {
        "fizz": [1, 2, 3],
        "bang": [4, 5, 6],
    }
    # lets make a --bar flag which is related to foo
    flags.DEFINE_integer(
        name="bar",
        short_name="b",
        default=None,

        # absl's formatter (which under the hood uses Python's builtin textwrap)
        # respects newlines, but it tries to strip leading whitespace. If you
        # wish to indent for readability, prefix a line with a unicode
        # zero-width no-break space, which absl will respect. It's a slight
        # hassle, but it can make the help message much more readable.
        help=help_wrap(
            u"Specify a number to go along with -foo.\n"
            u"\ufeff  if --foo=fizz:\n\ufeff    {}\n"
            .format(to_choices_str(choices["fizz"])) +
            u"\ufeff  if --foo=bang:\n\ufeff    {}\n"
            .format(to_choices_str(choices["bang"]))
        ),
    )

    # absl supports required flags.
    flags.mark_flag_as_required("bar")

    # absl allows validation between arbitrary sets of flags. When using
    # multi_flags_validator, the flag names and parsed values are passed into
    # the validator function as a dict.
    @flags.multi_flags_validator(["foo", "bar"])
    def _check_bar(flag_dict):  # pylint: disable=unused-variable
      return flag_dict["bar"] in choices[flag_dict["foo"]]

    key_flags.append("bar")

  return key_flags
