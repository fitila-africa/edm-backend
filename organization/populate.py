import organization
from .models import EcoSystem, Organization, Sector, SubEcosystem

def populate_ecosystem():
    a = EcoSystem.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    
    eco = ['Business support',
    'Policy and Regulation',
    'Research and Development',
    'MSMEs and Startups',
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

    with open('organization/data-29-03-2021.csv', mode='r', encoding='UTF-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # line_count = 0
        for row in csv_reader:
            row['sector'] = Sector.objects.get(name = str(row['sector']))
            row['ecosystem'] = EcoSystem.objects.get(name = str(row['ecosystem']))
            print(row['sub_ecosystem'])
            row['sub_ecosystem'] = SubEcosystem.objects.get(name = str(row['sub_ecosystem']), ecosystem=row['ecosystem'])
            # print(row['ecosystem'])
            # print(row)
            Organization.objects.create(**row, is_active=True, responded = True, is_approved=True )
            print(row['name'], 'Done')


def populate_sub():
    a = SubEcosystem.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")

    data  = {
        'Business support': [{ 'name':'Business Advisory'},{ 'name':'Mentoring' },  {'name':'Incubators'},{'name':'Accelerators'}, {'name':'Resources'}, {'name':'Others'}],

        'Training' : [{'name':'Enterprise Support Organizations'}, {'name':'Incubators'},{'name':'Accelerators'}, {'name':'Virtual Learning'}, {'name':'Others'}],

        'Funding' : [{'name':'Loan Providers'}, {'name':'Grant Providers'}, {'name':'Equity Funders'},{'name': 'Crowd Funding'}, {'name':'Others'}],

        'Market Access':[{'name':'Distribution channels that facilitate trade'}, {'name':'Organizations'}, {'name':'Tech Platforms'},{'name':'Others'}],
        
        'Policy and Regulation': [{'name':'Government'},{'name': 'Regulators'}, {'name': 'Entrepreneurship Advocacy groups'}, {'name':'Others'}],

        # 'Resources':[{'name':'Virtual Resources'}, {'name':'In-person Resources'}, {'name':'Tools'}, {'name':'Services'}, {'name':'Others'}],

        'Research and Development' :[{'name':'Makerspaces'}, {'name':'Research Organizations/Centers'}, {'name':'Innovation and Design spaces for hardware and software'}, {'name':'Others'}],
  
        'MSMEs and Startups':[{'name':'MSMEs'}, {'name':'Others'}]}

    for key in data.keys():
        ecosystem = EcoSystem.objects.get(name=key)
        for val in data[key]:
            SubEcosystem.objects.create(**val, ecosystem=ecosystem)
            print(val['name'], 'Done')

        print(key, 'Done')
        print('====================\n')




def add_sector():
    a = Sector.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")

    sectors = ['Incubators & Accelerators', 'Government',
       'Development/Non Profit Organisation',
       'Private Sector Groups & Associations',
       'Equity-Venture Capital/Angel Investors', 'Trade Groups/Associations',
       'Loans/Debt', 'Academia', 'Non-Profit', 'Others',
       'For Profit/Corporates', 'Virtual Information Portals', 'Grants',
       'Access to Credit Platform Facilitators', 'Crowdfunding', 'eCommerce']

    for i in sectors:
        Sector.objects.create(name=i)
        print('{} Done'.format(i))