# Set path to ndk-bundle
export NDK_BUNDLE_DIR=/home/revo/Android/Sdk/ndk-bundle

# Export PATH to contain directories of clang and aarch64-linux-android-* utilities
export PATH=${NDK_BUNDLE_DIR}/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/:${NDK_BUNDLE_DIR}/toolchains/llvm/prebuilt/linux-x86_64/bin:$PATH

# Setup LDFLAGS so that loader can find libgcc and pass -lm for sqrt
export LDFLAGS="-L${NDK_BUNDLE_DIR}/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/lib/gcc/aarch64-linux-android/4.9.x -lm"

# Setup the clang cross compile options
export CLANG_FLAGS="-target aarch64-linux-android --sysroot ${NDK_BUNDLE_DIR}/platforms/android-24/arch-arm64 -gcc-toolchain ${NDK_BUNDLE_DIR}/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/"

# Compile
make TARGET=ARMV8 ONLY_CBLAS=1 AR=ar CC="clang ${CLANG_FLAGS}" HOSTCC=gcc -j4 
