"""Run one explicit recipe. --list and --dry-run make no API calls."""
import argparse
import json
import os
import sys
from pathlib import Path
from live import ROOT, configure, resolve, run_actor, write_json, select_named_match


def main():
    configure()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recipe', nargs='?')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--reuse', action='store_true', help='Reuse matching successful local exports; results may be stale.')
    parser.add_argument('--ai', action='store_true', help='Send evidence to the configured OpenAI model (separate charges).')
    args = parser.parse_args()
    recipes = {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'recipes').glob('*.json')}
    if args.list:
        for name, recipe in sorted(recipes.items()):
            print(f"{name:34} {recipe['title']}")
        return
    if args.recipe not in recipes:
        parser.error('Choose a recipe from python run.py --list')
    recipe = resolve(recipes[args.recipe])
    if args.ai and recipe['process'] not in ('scout', 'recap', 'query', 'evidence'):
        parser.error('--ai is supported only by AI recipes')
    if args.ai and not all(os.getenv(k) for k in ('OPENAI_API_KEY', 'OPENAI_MODEL')):
        parser.error('--ai requires OPENAI_API_KEY and OPENAI_MODEL before starting paid Actor runs')
    if args.dry_run:
        print(json.dumps(recipe, ensure_ascii=False, indent=2))
        return
    output = ROOT / 'output' / args.recipe
    write_json(output/'recipe.json', recipe)
    batches = {}
    for step in recipe['steps']:
        batches[step['name']] = run_actor(step['actor'], step['input'], output/step['name'], reuse=args.reuse)
    if 'match_selection' in recipe:
        name = recipe['steps'][0]['name']
        selected = select_named_match(batches[name], recipe['match_selection'])
        write_json(output/'selected-match.json', selected)
        batches[name] = [selected]
    from workflows import process
    process(recipe, batches, output, ai=args.ai, reuse=args.reuse)
    print(f'Done: {output}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # Transport errors can contain request URLs: never print a token-bearing exception.
        message = str(exc)
        for key in ('APIFY_TOKEN', 'OPENAI_API_KEY'):
            if os.getenv(key):
                message = message.replace(os.environ[key], '[REDACTED]')
        print(f'{type(exc).__name__}: {message}', file=sys.stderr)
        sys.exit(1)
