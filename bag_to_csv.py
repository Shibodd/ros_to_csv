import argparse
import pathlib
import yaml
import re
import csv
import function_repo

class BagReader:
  def __init__(self, topics, *paths, start = None, stop = None):
    import rosbags.highlevel

    self.__reader = rosbags.highlevel.AnyReader(paths)
    
    self.__topics = topics
    self.__start = start
    self.__stop = stop

  def __enter__(self):
    self.__reader.__enter__()
    return self

  def __exit__(self, *args, **kwargs):
    self.__reader.__exit__(*args, **kwargs)

  def __iter__(self):
    connections = [conn for conn in self.__reader.connections if conn.topic in self.__topics]
    return (
      (t, conn.topic, self.__reader.deserialize(data, conn.msgtype))
      for conn, t, data in
      self.__reader.messages(connections, self.__start, self.__stop)
    )
  
class CsvManager:
  def __init__(self, base_path, topicdef):
    self.__topicdef = topicdef
    self.__base_path = base_path
    self.__files = {}

  def writerow(self, t, topic, msg):
    topicdef = self.__topicdef[topic]
    
    if topic not in self.__files:
      filename = topic.strip('/').replace('/', '_') + ".csv"
      f = open(self.__base_path / filename, "w")
      self.__files[topic] = (f, csv.writer(f))
      self.__files[topic][1].writerow(field_name for field_name, _ in topicdef)

    self.__files[topic][1].writerow(field_parser(t, msg) for _, field_parser in topicdef)
  
  def __enter__(self):
    return self

  def __exit__(self, *args, **kwargs):
    for f in self.__files.values():
      f[0].close()

def parse_topicfile(path: pathlib.Path):
  with path.open('r') as f:
    content = yaml.safe_load(f)

  assert isinstance(content, dict
  ), "The topicfile must be a dictionary."
  assert all(isinstance(topic_def, list) for topic_def in content.values()
  ), "Each topic definition value must be a list."
  assert all(
    all(isinstance(field_def, dict) for field_def in topic_def)
    for topic_def in content.values()
  ), "Each field definition must be a dictionary."
  assert all(
    all(len(field_def.keys()) == 1 and isinstance(next(iter(field_def.values())), str) for field_def in topic_def)
    for topic_def in content.values()
  ), "Each field definition must be a column name and string pair."

  def parse_field_def(field_def):
    cmd = re.match(r'^\$([A-Z0-9_]+)\(([^\)]+)\)$', field_def)
    if cmd:
      name, args = cmd.group(1), [x.strip() for x in cmd.group(2).split(',')]
    else:
      name, args = "GET", [field_def]
    return function_repo.FUNCTION_FACTORIES[name](*args)
  
  for topic_def in content.values():
    for i in range(len(topic_def)):
      topic_name, field_def = next(iter(topic_def[i].items()))
      topic_def[i] = topic_name, parse_field_def(field_def)

  return content

if __name__ == '__main__':
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('-b', '--bag', required=True, type=pathlib.Path)
  arg_parser.add_argument('-o', '--outputdir', required=True, type=pathlib.Path)
  arg_parser.add_argument('-t', '--topicfile', required=True, type=pathlib.Path)
  args = arg_parser.parse_args()

  topics = parse_topicfile(args.topicfile)

  args.outputdir.mkdir(exist_ok=True)

  with BagReader(topics.keys(), args.bag) as reader:
    with CsvManager(args.outputdir, topics) as fm:
      for entry in reader:
        fm.writerow(*entry)