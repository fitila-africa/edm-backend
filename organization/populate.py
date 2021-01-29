import organization
from .models import EcoSystem, Organization, SubEcosystem

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
    a = Organization.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    import csv

    with open('organization/updated_data.csv', mode='r', encoding='UTF-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # line_count = 0
        for row in csv_reader:
            row['ecosystem'], created = EcoSystem.objects.get_or_create(name = str(row['ecosystem']))
            print(row['sub_ecosystem'])
            row['sub_ecosystem'], created = SubEcosystem.objects.get_or_create(name = str(row['sub_ecosystem']), ecosystem=row['ecosystem'])
            # print(row['ecosystem'])
            # print(row)
            Organization.objects.create(**row, is_active=True )
            print(row['name'], 'Done')


def populate_sub():
    a = SubEcosystem.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")

    data  = {
        'Business support': [{ 'name':'Business Advisory'},{ 'name':'Mentoring' },  {'name':'Incubators'},{'name':'Accelerators'},{'name':'Churches/Mosques'}],

        'Training' : [{'name':'Enterprise Support Organizations'}, {'name':'Incubators'},{'name':'Accelerators'},{'name':'Churches/Mosques'}, {'name':'Virtual Learning'}],

        'Funding' : [{'name':'Loan Providers'}, {'name':'Grant Providers'}, {'name':'Equity Funders'}],

        'Market Access':[{'name':'Distribution channels that facilitate trade'}, {'name':'Tech platforms that facilitate trade'}],
        
        'Policy and Regulation': [{'name':'Government'},{'name': 'Regulators'}, {'name': 'Entrepreneurship Advocacy groups'}],

        'Resources':[{'name':'Virtual Resources'}, {'name':'In-person Resources'}, {'name':'Tools'}, {'name':'Services'}],

        'Research and Development' :[{'name':'Makerspaces'}, {'name':'Research centers'}, {'name':'Innovation and Design spaces for hardware and software'}],
  
        'Businesses':[{'name':'MSMEs'}]}

    for key in data.keys():
        ecosystem = EcoSystem.objects.get(name=key)
        for val in data[key]:
            SubEcosystem.objects.create(**val, ecosystem=ecosystem)
            print(val['name'], 'Done')

        print(key, 'Done')
        print('====================\n')




def add_description_eco():
    pass

def add_description_sub():
    pass