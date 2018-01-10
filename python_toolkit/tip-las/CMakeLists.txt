project (pytip)

cmake_minimum_required(VERSION 3.5.1)
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
set(CMAKE_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR})
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set (CMAKE_CXX_FLAGS " -std=c++11 -O2 -march=native")

set(BOOST_COMPONENTS system timer iostreams filesystem chrono program_options thread)

find_package(PythonLibs 2.7)
if(PYTHONLIBS_FOUND)
  set(BOOST_COMPONENTS ${BOOST_COMPONENTS} python)
  message(STATUS "Found Python")
  include_directories(${PYTHON_INCLUDE_DIRS})
  set(EXT_LIBS ${EXT_LIBS} ${PYTHON_LIBRARIES})
else(PYTHONLIBS_FOUND)
  message(WARNING "Cannot find python libraries. Building without bindings.")
endif(PYTHONLIBS_FOUND)

find_package(Boost COMPONENTS ${BOOST_COMPONENTS})
if(Boost_FOUND)
  include_directories(${Boost_INCLUDE_DIRS})
  set(EXT_LIBS ${EXT_LIBS} ${Boost_LIBRARIES})
else(Boost_FOUND)
  message(SEND_ERROR "Cannot find Boost libraries. Terminating.")
endif(Boost_FOUND)

#found boost & python
include_directories(.)
include_directories(../)

add_library( main SHARED
  python_tip.cpp
  ../utility/SentenceSplit.cpp
  ../utility/StringOperation.cpp
  ../utility/POSExtract.cpp
  ../utility/StringSplit.cpp
  ../utility/StringType.cpp
  ../utility/TextClassification.cpp
  ../utility/Tokenize.cpp
  ../tagging/Sample.cpp
  ../tagging/Model.cpp
  ../tagging/Decoder.cpp
  ../tagging/Perceptron.cpp
  ../Formatting.cpp
  ../Las.cpp
)
#warpper
#add_library( pytip SHARED python_tip.cpp )
set_target_properties(main PROPERTIES OUTPUT_NAME pytip)
target_link_libraries(main ${Boost_LIBRARIES})

#add_executable(pytip python_tip.cpp)

# set_target_properties(pytip PROPERTIES EXCLUDE_FROM_ALL 1)
# set_target_properties(pytip PROPERTIES OUTPUT_NAME pytip)
# set_target_properties(pytip PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
# set_target_properties(pytip PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
