from datetime import datetime, timedelta


def cook_redy(filename):
    with open(f'{filename}', 'r') as cook:
        lines = cook.read().splitlines()

    with open('cook_rdy.txt', 'w') as cook:
        cook.write('# Netscape HTTP Cookie File\n')
        for line in lines:
            name, value, domain, path, expiration, *a, http_only = line.split('\t')
            if name == '':
                continue

            if domain[0] != '.':
                domain = f'.{domain}'

            http_only = 'TRUE' if http_only == '✓' else 'FALSE'

            if expiration == 'Session':
                expiration = datetime.now() + timedelta(weeks=48)
            else:
                expiration = datetime.strptime(expiration, '%Y-%m-%dT%H:%M:%S.%fZ')

            expiration = str(int(expiration.timestamp()))
            cook.write('\t'.join([domain, 'TRUE', path, http_only, expiration, name, value]))
            cook.write('\n')
