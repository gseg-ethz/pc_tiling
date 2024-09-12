from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import sysconfig
import os
import shutil


class CMakeBuildExt(build_ext):
    def run(self):
        # First, run CMake to build the shared library
        self.build_cmake()

        # Then, proceed with the rest of the build process
        super().run()

    def build_cmake(self):
        # Define the build directory for CMake
        cmake_build_dir = os.path.join(self.build_temp, 'cmake_build')

        # Create the build directory if it doesn't exist
        if not os.path.exists(cmake_build_dir):
            os.makedirs(cmake_build_dir)

        # Run CMake to configure and build the shared library
        cmake_source_dir = os.path.join('./cpp')
        cmake_args = [cmake_source_dir, '-B', cmake_build_dir]

        subprocess.check_call(['cmake', *cmake_args])
        subprocess.check_call(['cmake', '--build', cmake_build_dir])

        # Copy the built library to the expected location
        built_lib_path = os.path.join(cmake_build_dir, 'lib', 'libpc_tiling.so')
        if not os.path.exists(built_lib_path):
            raise RuntimeError(f"Failed to build the shared library: {built_lib_path} not found")

        target_lib_dir = os.path.join('.', 'lib')
        if not os.path.exists(target_lib_dir):
            os.makedirs(target_lib_dir)

        target_lib_path = os.path.join(target_lib_dir, 'libpc_tiling.so')
        self.copy_file(built_lib_path, target_lib_path)

        # Optionally, you could delete the CMake build directory after copying
        # shutil.rmtree(cmake_build_dir)

    def build_extensions(self):
        # Ensure the build directory exists
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Update the sources for the extension to include the generated wrapper
        for ext in self.extensions:
            if ext.name == 'pc_tiling._pc_tiling':
                _name = 'pc_tiling'
                ext.sources = [os.path.join(self.build_temp, 'pc_tiling_wrap.cxx')]

            # Generate the SWIG wrapper coded
            swig_cmd = ['swig', '-python', '-c++',
                        '-o', ext.sources[0],
                        '-outdir', os.path.join(self.build_lib, 'pc_tiling'),
                        *list(map(lambda incl_dir: f"-I{incl_dir}", ext.include_dirs)),
                        '-I./include',
                        './swig/pc_tiling.i']
            subprocess.check_call(swig_cmd)

        # Now proceed with the regular build process
        super().build_extensions()


# Define the extension module
pc_tiling_module = Extension(
    name='pc_tiling._pc_tiling',
    sources=[],  # This will be populated by SWIGBuildExt
    include_dirs=[
        sysconfig.get_path('include'),  # Python headers
        './include'  # Your custom headers
    ],
    libraries=['pc_tiling'],  # The original shared library (libpc_tiling.so)
    library_dirs=['./lib'],  # Directory where libpc_tiling.so is located
    extra_compile_args=['-fPIC'],  # Ensure position-independent code
    extra_link_args=[f"-Wl,-rpath,{os.path.join(sysconfig.get_config_var('LIBDIR'),'pc_tiling')}"],  # Add the library directory to the runtime path
)


# Setup script
setup(
    ext_modules=[pc_tiling_module],
    cmdclass={'build_ext': CMakeBuildExt},  # Use the custom build_ext command
    data_files=[
        ('lib/pc_tiling', ['./lib/libpc_tiling.so'])
    ]
)
