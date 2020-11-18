import organization
from .models import EcoSystem, Organization

def populate_ecosystem():
    eco = ['Business support',
    'Policy and Regulation',
    'Resources',
    'Research and Development',
    'Businesses',
    'Market Access',
    'Funding',
    'Training']

    for i in eco:
        EcoSystem.objects.create(name=i)
        print('{} Done'.format(i))

def populate_organization():
    import csv

    with open('organization/file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # line_count = 0
        for row in csv_reader:
            row['ecosystem'] = EcoSystem.objects.get(name = str(row['ecosystem']))
            # print(row['ecosystem'])

            Organization.objects.create(**row)
            print(row['name'], 'Done')