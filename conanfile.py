from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment


class CapnprotoConan(ConanFile):
    name = "capnproto"
    version = "0.6.1"
    license = "<Put the package license here>"
    url = "https://github.com/imadari/conan-capnproto"
    description = "<Description of Capnproto here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/sandstorm-io/capnproto.git")
        self.run("cd capnproto && git checkout tags/v0.6.1")
        

    def build(self):
        with tools.chdir("capnproto"):
            with tools.chdir("c++"):
                self.run('autoreconf -i')
                env_build = AutoToolsBuildEnvironment(self)
                env_build.configure(args=['--enable-shared'])
                env_build.make()

    def package(self):
        self.copy("*.h", dst="include/capnp", src="capnproto/c++/src/capnp/")
        self.copy("*.h", dst="include/kj", src="capnproto/c++/src/kj/")
        self.copy("*.so", dst="lib", src="capnproto/c++/.libs/", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["capnp", "kj"]

