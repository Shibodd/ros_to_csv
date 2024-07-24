def parse_path(path):
  return [x.strip() for x in path.split('.')]

def path_get(msg, path):
  v = msg
  for p in path:
    v = getattr(v, p)
  return v

def stamp_to_ns_factory(path):
  path = parse_path(path)
  def stamp_to_ns(_, msg):
    stamp = path_get(msg, path)
    return stamp.sec * 10**9 + stamp.nanosec
  return stamp_to_ns

def get_factory(path):
  path = parse_path(path)
  def get(_, msg):
    return path_get(msg, path)
  return get

FUNCTION_FACTORIES = {
  'GET': get_factory,
  'STAMP_TO_NS': stamp_to_ns_factory
}
