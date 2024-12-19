import os
import argparse
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser(description='Generate Nginx configuration')
parser.add_argument('--template', required=True, help='Path to the Nginx template file')
parser.add_argument('--output', required=True, help='Path to output the generated configuration')
args = parser.parse_args()
template_dir = os.path.dirname(args.template)
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(os.path.basename(args.template))
domain_name = os.getenv('DOMAIN_NAME')
output = template.render(DOMAIN_NAME=domain_name)
with open(args.output, 'w') as f:
    f.write(output)

print(f'Nginx configuration generated successfully and saved in {args.output}!')
