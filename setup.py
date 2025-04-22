from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.dist import Distribution
import subprocess
import sysconfig
import os
import shutil

PACKAGE_NAME = "pc_tiling"
SRC_DIR = os.path.abspath("src")
PKG_DIR = os.path.join(SRC_DIR, PACKAGE_NAME)

class CMakeBuildExt(build_ext):
    def run(self):
        # First, run CMake to build the shared library
        self.build_cmake()

        # Then, proceed with the rest of the build process
        super().run()

    def build_cmake(self):
        build_temp = os.path.abspath(self.build_temp)
        cmake_build_dir = os.path.join(build_temp, "cmake_build")
        os.makedirs(cmake_build_dir, exist_ok=True)

        cmake_args = [
            os.path.abspath("cpp"),
            "-B", cmake_build_dir,
        ]

        subprocess.check_call(["cmake", *cmake_args])
        subprocess.check_call(["cmake", "--build", cmake_build_dir])

        built_lib_path = os.path.join(cmake_build_dir, "lib", "libpc_tiling.so")
        if not os.path.exists(built_lib_path):
            raise RuntimeError(f"Missing compiled shared lib: {built_lib_path}")

        target_path = os.path.join(PKG_DIR, "libpc_tiling.so")
        os.makedirs(PKG_DIR, exist_ok=True)
        self.copy_file(built_lib_path, target_path)

    def build_extensions(self):
        os.makedirs(self.build_temp, exist_ok=True)

        swig_output = os.path.join(self.build_temp, "pc_tiling_wrap.cxx")
        swig_cmd = [
            "swig", "-python", "-c++",
            "-o", swig_output,
            "-outdir", PKG_DIR,
            "-I./include",
            *[f"-I{d}" for d in self.extensions[0].include_dirs],
            "./swig/pc_tiling.i",
        ]
        subprocess.check_call(swig_cmd)

        self.extensions[0].sources = [swig_output]
        super().build_extensions()

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

ext_modules = [
    Extension(
        name=f"{PACKAGE_NAME}._pc_tiling",
        sources=[],  # to be filled in by build_ext
        include_dirs=[
            sysconfig.get_path("include"),
            "./include",
        ],
        libraries=["pc_tiling"],
        library_dirs=[PKG_DIR],
        extra_compile_args=["-fPIC"],
        extra_link_args=["-Wl,-rpath,$ORIGIN"],
    )
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": CMakeBuildExt},
    distclass=BinaryDistribution,
    include_package_data=True,
    packages=["pc_tiling"],
    package_dir={"pc_tiling": "src/pc_tiling"},
    package_data={"pc_tiling": ["libpc_tiling.so"]},  # <- This line ensures .so gets included
)