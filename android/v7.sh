# Set path to ndk-bundle
export NDK_BUNDLE_DIR=/home/revo/Android/Sdk/ndk-bundle

# Set the PATH to contain paths to clang and arm-linux-androideabi-* utilities
export PATH=${NDK_BUNDLE_DIR}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin:${NDK_BUNDLE_DIR}/toolchains/llvm/prebuilt/linux-x86_64/bin:$PATH

# Set LDFLAGS so that the linker finds the appropriate libgcc
export LDFLAGS="-L${NDK_BUNDLE_DIR}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/lib/gcc/arm-linux-androideabi/4.9.x"

# Set the clang cross compile flags
export CLANG_FLAGS="-target arm-linux-androideabi -marm -mfpu=vfp -mfloat-abi=softfp --sysroot ${NDK_BUNDLE_DIR}/platforms/android-24/arch-arm -gcc-toolchain ${NDK_BUNDLE_DIR}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/"

# export LIBRARY_PATH=$LIBRARY_PATH:${NDK_BUNDLE_DIR}/platforms/android-24/arch-arm/usr/lib

#OpenBLAS Compile
make PREFIX=build-v7/ TARGET=ARMV7 ONLY_CBLAS=1 AR=ar CC="clang ${CLANG_FLAGS}" HOSTCC=gcc ARM_SOFTFP_ABI=1 -j
