from pathlib import Path

from mutate import mutate

def example():
    js_function = Path('transformer.js').read_text(encoding='utf-8')

    print(mutate(js_function, 'hello'))

if __name__ == '__main__':
    example()

