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
from legion import task, RW, WD
import numpy as np

@task(privileges=[WD])
def init_field(R):
    points = np.array(
        [[([0, 0],), ([0, 0],), ([2, 1],), ([1, 2],)],
         [([1, 1],), ([1, 1],), ([3, 1],), ([1, 3],)],
         [([0, 1],), ([2, 0],), ([3, 0],), ([0, 0],)],
         [([1, 0],), ([2, 0],), ([3, 2],), ([0, 1],)]],
        dtype=R.point.dtype)
    np.copyto(R.point, points, casting='no')

@task
def main():
    R = legion.Region.create([4, 4], {'point': legion.int2d})
    init_field(R)

    P = legion.Partition.create_by_restriction(R, [2, 2], np.eye(2)*2, [2, 2])
    Q = legion.Partition.create_by_preimage(P, R, 'point', [2, 2])

    assert P.color_space.volume == 4
    assert P[0, 0].ispace.volume == 4
    assert P[0, 1].ispace.volume == 4
    assert P[1, 0].ispace.volume == 4
    assert P[1, 1].ispace.volume == 4

    assert Q[0, 0].ispace.volume == 8
    assert Q[0, 1].ispace.volume == 2
    assert Q[1, 0].ispace.volume == 5
    assert Q[1, 1].ispace.volume == 1

if __name__ == '__legion_main__':
    main()