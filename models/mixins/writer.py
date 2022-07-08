from pathlib import Path


class Writer:

    def _write(self, url, directory):
        filepath = Path(
            f'results/{self.name}/{self.search_type}/{directory}.txt')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'a+', encoding='utf-8', errors='ignore') as f:
            f.write(f'{url}\n')
