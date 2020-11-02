@#{import yaml}
@#{local_args = locals()}
@#(local_args)
@#{from io import StringIO}
@#{ss = StringIO()}
@#{a = yaml.dump(args)}
@#(a)
@#{import pickle}
@#{local_args = locals()}
@#(pickle.dumps(local_args))
