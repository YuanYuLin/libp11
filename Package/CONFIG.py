import ops
import iopc

pkg_path = ""
output_dir = ""
arch = ""
src_usr_lib_dir = ""
dst_lib_dir = ""
src_include_dir = ""
dst_include_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global arch
    global src_usr_lib_dir
    global dst_lib_dir
    global src_include_dir
    global dst_include_dir
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    if arch == "armhf":
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/arm-linux-gnueabihf")
    elif arch == "armel":
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/arm-linux-gnueabi")
    elif arch == "x86_64":
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/x86_64-linux-gnu")
    else:
        sys.exit(1)
    dst_lib_dir = ops.path_join(output_dir, "lib")

    src_include_dir = iopc.getBaseRootFile("usr/include/p11-kit-1/p11-kit")
    dst_include_dir = ops.path_join("include",args["pkg_name"])


def MAIN_ENV(args):
    set_global(args)
    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.mkdir(dst_lib_dir)
    ops.copyto(ops.path_join(src_usr_lib_dir, "libp11-kit.so.0.2.0"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libp11-kit.so.0.2.0", "libp11-kit.so.0.2")
    ops.ln(dst_lib_dir, "libp11-kit.so.0.2.0", "libp11-kit.so.0")
    ops.ln(dst_lib_dir, "libp11-kit.so.0.2.0", "libp11-kit.so")
    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(build_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)
    return False

def MAIN_BUILD(args):
    set_global(args)
    return False

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "deprecated.h"), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "iter.h"), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "p11-kit.h"), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pin.h"), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pkcs11.h"), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pkcs11x.h"), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "remote.h"), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "uri.h"), dst_include_dir)

    iopc.installBin(args["pkg_name"], ops.path_join(dst_lib_dir, "."), "lib") 
    return False

def MAIN_SDKENV(args):
    set_global(args)

    cflags = ""
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), 'usr/include/' + args["pkg_name"])
    iopc.add_includes(cflags)

    libs = ""
    libs += " -lp11-kit"
    iopc.add_libs(libs)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)
    return False

def MAIN(args):
    set_global(args)

