from cffi import FFI as _FFI

import numpy as _np

import glob as _glob
import os as _os


__all__ = ['BloscWrapper']



class BloscWrapper:
    
    def __init__(self, plugin_file=""):

        this_module_dir = _os.path.dirname(_os.path.realpath(__file__))

        # find the C library by climbing the directory tree
        while plugin_file == "":
            plugin_pattern = _os.path.join(this_module_dir, "*ags_blosc_wrapper.*")
            candidate_plugins = _glob.glob(plugin_pattern)
            # if found then break
            if candidate_plugins:
                plugin_file = candidate_plugins[0]
                break
            # not found and already at root.  We're not going to find it
            if this_module_dir == "/":
                raise ValueError("Cannot find plugin ags_blosc_wrapper")
            # go to parent directory and try again
            this_module_dir = _os.path.split(this_module_dir)[0] 
            

        # specify the C signatures of the foreign functions
        self._ffi = _FFI()
        self._ffi.cdef("typedef void* ags_BloscWrapper;")
        self._ffi.cdef("ags_BloscWrapper ags_BloscWrapper_new();")
        self._ffi.cdef("void ags_BloscWrapper_delete(ags_BloscWrapper);")
        self._ffi.cdef("size_t ags_BloscWrapper_reserveNeededToCompress(ags_BloscWrapper, size_t);")
        self._ffi.cdef("size_t ags_BloscWrapper_reserveNeededToDecompress(ags_BloscWrapper, void*);")
        self._ffi.cdef("size_t ags_BloscWrapper_compress(ags_BloscWrapper, void*, size_t, void*, size_t);")
        self._ffi.cdef("size_t ags_BloscWrapper_decompress(ags_BloscWrapper, void*, void*, size_t);")
        
        self._cmodule = self._ffi.dlopen(plugin_file)
        
        # allocate a new raw instance 
        self.blosc_wrapper = self._cmodule.ags_BloscWrapper_new()


    def __del__(self):

        # free the raw instance
        self._cmodule.ags_BloscWrapper_delete(self.blosc_wrapper)


    def reserve_needed_to_compress(self, srcsize):

        size = self._ffi.cast("size_t", srcsize)
        return self._cmodule.ags_BloscWrapper_reserveNeededToCompress(self.blosc_wrapper, size)


    def reserve_needed_to_decompress(self, src):

        # get raw buffers
        src_contiguous = _np.ascontiguousarray(src)
        src_raw = src_contiguous.__array_interface__['data'][0]
        src_cffi = self._ffi.cast("void*", src_raw)
        return self._cmodule.ags_BloscWrapper_reserveNeededToDecompress(self.blosc_wrapper, src_cffi)


    def compress(self, src):

        # get sizes
        srcsize = src.nbytes
        dstsize = self.reserve_needed_to_compress(srcsize) 
        srcsize_cffi = self._ffi.cast("size_t", srcsize)
        dstsize_cffi = self._ffi.cast("size_t", dstsize)

        # allocate destination
        dst = _np.empty(shape=(dstsize,), dtype=_np.uint8)

        # get raw buffers
        src_contiguous = _np.ascontiguousarray(src)
        src_raw = src_contiguous.__array_interface__['data'][0]
        src_cffi = self._ffi.cast("void*", src_raw)

        dst_contiguous = _np.ascontiguousarray(dst)
        dst_raw = dst_contiguous.__array_interface__['data'][0]
        dst_cffi = self._ffi.cast("void*", dst_raw)

        # perform compression and resize
        dstsize = self._cmodule.ags_BloscWrapper_compress(self.blosc_wrapper, src_cffi, srcsize_cffi, dst_cffi, dstsize_cffi)
        dst.resize((dstsize,))
        
        return dst


    def decompress(self, src):

        # get sizes
        dstsize = self.reserve_needed_to_decompress(src)
        dstsize_cffi = self._ffi.cast("size_t", dstsize)

        # allocate destination
        dst = _np.empty(shape=(dstsize,), dtype=_np.uint8)

        # get raw buffers
        src_contiguous = _np.ascontiguousarray(src)
        src_raw = src_contiguous.__array_interface__['data'][0]
        src_cffi = self._ffi.cast("void*", src_raw)

        dst_contiguous = _np.ascontiguousarray(dst)
        dst_raw = dst_contiguous.__array_interface__['data'][0]
        dst_cffi = self._ffi.cast("void*", dst_raw)

        # perform decompression and resize
        dstsize = self._cmodule.ags_BloscWrapper_decompress(self.blosc_wrapper, src_cffi, dst_cffi, dstsize_cffi)
        dst.resize((dstsize,))
        
        return dst
