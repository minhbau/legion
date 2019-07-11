#!/usr/bin/env python

# Copyright 2019 Stanford University
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
#

from __future__ import print_function

import legion
from legion import task, Reduce
import numpy

@task(privileges=[Reduce('+')])
def inc(R, step):
    numpy.add(R.x, step, out=R.x)
    numpy.add(R.y, step, out=R.y)

@task
def main():
    R = legion.Region.create([4, 4], {'x': legion.float64, 'y': legion.int32})
    legion.fill(R, 'x', 1.25)
    legion.fill(R, 'y', 2)
    inc(R, 20)
    print(R.x)
    print(R.y)
    assert R.x[0, 0] == 21.25
    assert R.y[0, 0] == 22

if __name__ == '__legion_main__':
    main()