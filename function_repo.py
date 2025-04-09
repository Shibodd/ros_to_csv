def parse_path(path):
  return [x.strip() for x in path.split('.')]

def path_get(msg, path):
  v = msg
  for p in path:
    v = getattr(v, p)
  return v

def bag_stamp_factory():
  def bag_stamp(t, _):
    return t
  return bag_stamp

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

def scale_offset_factory(path, scale, offset):
  path = parse_path(path)
  def scale_offset(_, msg):
    return path_get(msg, path) * float(scale) + float(offset)
  return scale_offset
   

FUNCTION_FACTORIES = {
  'GET': get_factory,
  'STAMP_TO_NS': stamp_to_ns_factory,
  'SCALE_OFFSET': scale_offset_factory,
  'BAG_STAMP': bag_stamp_factory
}
