Introduction
============

This repo is part of the tutorial found in
https://github.com/ActivisionGameScience/ags_conda_recipes.git

It contains a single python module, ``ags_py_blosc_wrapper``, that
is a wrapper around the C++ library ``ags_blosc_wrapper``.  This, in
turn, is a dumb wrapper around the popular ``c-blosc`` compression library.  See
https://github.com/ActivisionGameScience/ags_example_cpp_lib.git for
more details. 

The purpose of this module is to demonstrate several techniques:

- How to manage external dependencies using ``conda``

- How to call a C binary from python using ``cffi``

We purposefully exposed both a C and C++ API in ``ags_blosc_wrapper``
to ease binding to other languages.  In our
opinion it is *always* best to wrap C++ code in a C API.  We recommend
*against* trying to bind to C++ directly.

Either ``cffi`` or ``cython`` can be used for the C binding (we
prefer ``cffi`` slightly).


How to build
============

The ``conda`` build recipe is located in 
https://github.com/ActivisionGameScience/ags_conda_recipes.git.
You can use it to build, publish, and install 
the ``conda`` way.

However, you can also build and install this module by hand.
Assuming that ``ags_blosc_wrapper`` is installed in the following location::

    /some/path/include/activision_game_science/*.h
    /some/path/lib/libags_blosc_wrapper.so

and PYTHONPATH points to the same directory tree::

    /some/path/lib/python2.7/site-packages

you can build and install with the following commands::

    git clone https://github.com/ActivisionGameScience/ags_example_py_wrapper.git
    cd ags_example_py_wrapper
    python setup.py install

Here is an example of how to import and use the module::

    from ags_py_blosc_wrapper import BloscWrapper
    b = BloscWrapper()

    # initialize data however you want
    data = np.array(..., dtype=float32) # can be an arbitrary numpy array, not just floats

    # compress data
    data_compressed = b.compress(data)
    del data
    
    # do stuff
    
    # decompress
    data = b.decompress(data_compressed).view(np.float32)
    del data_compressed

    print(data)  # should be the same as it was originally


License
=======

All files are licensed under the BSD 3-Clause License as follows:
 
| Copyright (c) 2015, Activision Publishing, Inc.  
| All rights reserved.
| 
| Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
| 
| 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
|  
| 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
|  
| 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
|  
| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

