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
"""Example of flag use."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from absl import app as absl_app
from absl import flags

from official.utils.flags import core as flags_core


@flags_core.call_only_once
def define_flags():
  flags_core.define_example()
  flags.adopt_module_key_flags(flags_core)


def main(_):
  print(flags.FLAGS.foo)
  print(flags.FLAGS.bar)


if __name__ == "__main__":
  define_flags()
  absl_app.run(main)
