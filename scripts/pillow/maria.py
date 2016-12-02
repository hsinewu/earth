from yaml import load as yaml_load

with open('database.yaml') as f:
	db_cfg = yaml_load(f.read())

print(db_cfg)