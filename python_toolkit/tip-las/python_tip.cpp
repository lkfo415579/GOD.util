#include <cstdlib>
#include <iostream>
#include <string>

#include <boost/python.hpp>
//
#include "./utility/head.h"
#include "./tagging/Perceptron.h"
#include "Formatting.h"
using namespace utility_train;
using namespace utility;
using namespace Tagging;

using namespace std;

//class Las* las = new Las();
class Model  * model_ws   = NULL;
class Sample * sample_ws  = NULL;
class Perceptron*  tagging_ws = NULL;
class Formatting*  format = NULL;
std::string  delimiter = " ";
bool WsTest(const std::string& text, std::string& val);

bool init(const std::string& model_path="ws.model") {
  format = new  Formatting();
  //
  model_ws  = new Model();
  sample_ws = new Sample();
  std::string modelws_path  =  model_path;
  if (!model_ws->ReadModel(modelws_path, sample_ws))
  {
    std::cout << "Read " << modelws_path << " Error!!!" << std::endl;
    return false;
  }
  tagging_ws = new Perceptron(sample_ws, model_ws);
  return true;
}
boost::python::list las_tokenize_list(boost::python::list& pyinput) {

  //model file
  clock_t start, end;
  start = clock();
  //tokenzing
  std::vector<std::string> input;
  for(int i = 0; i < boost::python::len(pyinput); ++i) {
    input.emplace_back(
        boost::python::extract<std::string>(boost::python::object(pyinput[i])));
  }
  //
  boost::python::list pyoutput;
  for (auto& myLine : input){
    std::string val = "";
    WsTest(myLine,val);
    //std::cout << val << std::endl;
    pyoutput.append(val);
  }
  // delete sample_ws;
  // delete model_ws;
  end = clock();
  //std::cout << "done, time cost: " << double(end - start) / CLOCKS_PER_SEC << " s" << std::endl;
  return pyoutput;
}
std::string las_tokenize(const std::string& myLine) {

  std::string val = "";
  WsTest(myLine,val);

  return val;
}

bool WsTest(const std::string& text, std::string& val)
{
  val.clear();
  std::vector<std::vector<std::string> > fs;
  std::vector<bool> segs;
  std::vector<std::string> result;
  format->WsTest(text, fs, segs);
  tagging_ws->Test(fs, result);
  std::string buffer = "";
  int size = result.size();
  for (int i = 0; i < size; i++)
  {
    buffer += fs[i][0];
    if (segs[i])
    {
      buffer += "\xe0\xbc\x8b";
    }
    if ((result[i] == "E") || (result[i] == "S"))
    {
      val += buffer;
      val += delimiter;
      buffer.clear();
    }
  }
  return true;
}



std::string version() {
  return std::string("1.0,tip python");
}

BOOST_PYTHON_MODULE(libpytip) {
  boost::python::def("init", init);
  boost::python::def("las_tokenize_list", las_tokenize_list);
  boost::python::def("las_tokenize", las_tokenize);
  boost::python::def("version", version);
}
