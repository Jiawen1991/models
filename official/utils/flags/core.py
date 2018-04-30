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
"""Public interface for flag definition.

See _example.py for detailed instructions on defining flags.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import sys

from absl import flags

from official.utils.flags import _base
from official.utils.flags import _benchmark
from official.utils.flags import _conventions
from official.utils.flags import _example
from official.utils.flags import _misc
from official.utils.flags import _performance


def set_defaults(**kwargs):
  for key, value in kwargs.items():
    flags.FLAGS.set_default(name=key, value=value)


def call_only_once(f):
  """Prevent unittests from defining flags multiple times."""
  setattr(f, "already_called", False)

  @functools.wraps(f)
  def wrapped_fn(*args, **kwargs):
    print(f.already_called)
    if f.already_called:
      return

    f(*args, **kwargs)
    setattr(f, "already_called", True)
  return wrapped_fn


def parse_flags(argv=None):
  """Reset flags and reparse. Only used by utils.testing.integration."""
  flags.FLAGS.unparse_flags()
  try:
    flags.FLAGS(sys.argv if argv is None else argv)
  except flags.Error as error:
    sys.stderr.write("FATAL Flags parsing error: %s\n" % error)
    sys.stderr.write("Pass -h or --helpfull to see help on flags.\n")
    sys.exit(1)


def define_in_core(f):
  """Defines a function in core.py, and registers it's key flags.

  absl uses the location of a flags.declare_key_flag() to determine the context
  in which a flag is key. By making all declares in core, this allows model
  main functions to call flags.adopt_module_key_flags() on core and correctly
  chain key flags.

  Args:
    f:  The function to be wrapped

  Returns:
    The "core-defined" version of the input function.
  """

  def core_fn(*args, **kwargs):
    key_flags = f(*args, **kwargs)
    [flags.declare_key_flag(fl) for fl in key_flags]  # pylint: disable=expression-not-assigned
  return core_fn


define_base = define_in_core(_base.define_base)
define_benchmark = define_in_core(_benchmark.define_benchmark)
define_example = define_in_core(_example.define_example)
define_image = define_in_core(_misc.define_image)
define_performance = define_in_core(_performance.define_performance)


help_wrap = _conventions.help_wrap
to_choices_str = _conventions.to_choices_str


get_tf_dtype = _performance.get_tf_dtype
get_loss_scale = _performance.get_loss_scale
