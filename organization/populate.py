import organization
from .models import EcoSystem, Organization, Sector, SubEcosystem
import pandas as pd

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

    with open('organization/revised_data.csv', mode='r', encoding='UTF-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # line_count = 0
        for row in csv_reader:
            row['sector'] = Sector.objects.get(name = str(row['sector']))
            print(row['ecosystem'])
            row['ecosystem'] = EcoSystem.objects.get(name = str(row['ecosystem']))
            
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
        'Business support': [{'name': 'Business Advisory'}, {'name': 'Mentoring'}, {'name': 'Resources'}, {'name': 'Incubators'}, {'name':'Others'}],

        'Training' : [{'name': 'Enterprise Support Organizations'}, {'name': 'Incubators'}, {'name':'Others'}],

        'Funding' : [{'name': 'Loan Providers'}, {'name': 'Grant Providers'}, {'name': 'Equity Funders'}, {'name': 'Crowdfunding'}, {'name':'Others'}],

        'Market Access':[{'name': 'Tech Platforms'}, {'name': 'Organizations'},{'name':'Others'}],
        
        'Policy and Regulation': [{'name': 'Regulators'}, {'name': 'Entrepreneurship Advocacy groups'}, {'name': 'Government'}, {'name':'Others'}],

        # 'Resources':[{'name':'Virtual Resources'}, {'name':'In-person Resources'}, {'name':'Tools'}, {'name':'Services'}, {'name':'Others'}],

        'Research and Development' :[{'name': 'Research Organizations/Centres'}, {'name': 'Others'}],
  
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

    sectors = ['Health',
 'Manufacturing',
 'Development Sector',
 'Others',
 'Technology',
 'Private Sector',
 'Public Sector',
 'Creatives',
 'Agribusiness',
 'Education']

    for i in sectors:
        Sector.objects.create(name=i)
        print('{} Done'.format(i))





################ DATA CLEANING FUNCTION #################

def process_data(file):
    """ This function takes in the file that was uploaded, reads it with pandas and cleans the data for saving into the model."""
    #read the file
    revised_data = pd.read_csv(file)
    #sector
    revised_data.sector.fillna('Others',inplace=True)
    revised_data.sector.replace('Access to Credit Platform Facilitators', 'Access to Credit Platform Facilitator', inplace=True)
    #ecosystem
    revised_data.ecosystem.replace('Research & Development', 'Research and Development', inplace=True)
    revised_data.ecosystem.replace('MSMEs & Startups', 'MSMEs and Startups', inplace=True)
    # sub_ecosystems
    revised_data.sub_ecosystem.fillna('Others', inplace=True)
    revised_data.ceo_gender.fillna('Nil', inplace =True)
    revised_data.ceo_gender = revised_data.ceo_gender.apply(lambda x : x.title())
    revised_data.rename(columns={'ceo/founder/director name':'ceo_name'}, inplace=True)
    revised_data.ceo_name.fillna('Nil', inplace=True)
    revised_data.fillna('', inplace=True)
    revised_data.set_index('name', inplace=True)
    
    cols = ['name']
    cols.extend([k for k in revised_data.columns])
    rows = []
    for row in revised_data.itertuples():
        each_data = {}
        for i in range(len(cols)):
            each_data[cols[i]]=row[i]

        rows.append(each_data)
    return rows