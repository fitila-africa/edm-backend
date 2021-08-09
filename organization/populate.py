from .models import EcoSystem, Organization, Sector, SubEcosystem, SubecosystemSubclass
import pandas as pd

def populate_ecosystem():
    
    """This function is clears all of the ecosystem in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    a = EcoSystem.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    
    eco = ['Business support',
            'Training',
            'Research and Development',
            'Funding',
            'MSMEs and Startups',
            'Market Access',
            'Policy and Regulation'
        ]


    for i in eco:
        EcoSystem.objects.create(name=i)
        print('{} Done'.format(i))

def populate_organization():
    
    """This function is clears all of the organization in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    
    a = Organization.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    import csv

    with open('organization/new_revised_data.csv', mode='r', encoding='UTF-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # line_count = 0
        for row in csv_reader:
            row['sector'] = Sector.objects.get(name = str(row['sector']))
            print(row['ecosystem'])
            row['ecosystem'] = EcoSystem.objects.get(name = str(row['ecosystem']))
            
            row['sub_ecosystem'] = SubEcosystem.objects.get(name = str(row['sub_ecosystem']), ecosystem=row['ecosystem'])
            
            if row['sub_ecosystem_sub_class']:
                row['sub_ecosystem_sub_class'] = SubecosystemSubclass.objects.get(name=str(row['sub_ecosystem_sub_class']), sub_ecosystem=row['sub_ecosystem'], ecosystem=row['ecosystem'])
                
            else:
                s = row.pop('sub_ecosystem_sub_class')
            Organization.objects.create(**row, is_active=True, responded = True, is_approved=True )
            print(row['name'], 'Done')


def populate_sub():
    """This function is clears all of the sub_ecosystem in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    
    a = SubEcosystem.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")

    # data  = {
        # 'Business support': [{'name': 'Business Advisory'}, {'name': 'Mentoring'}, {'name': 'Resources'}, {'name': 'Incubators'}, {'name':'Others'}],

        # 'Training' : [{'name': 'Enterprise Support Organizations'}, {'name': 'Incubators'}, {'name':'Others'}],

        # 'Funding' : [{'name': 'Loan Providers'}, {'name': 'Grant Providers'}, {'name': 'Equity Funders'}, {'name': 'Crowdfunding'}, {'name':'Others'}],

        # 'Market Access':[{'name': 'Tech Platforms'}, {'name': 'Organizations'},{'name':'Others'}],
        
        # 'Policy and Regulation': [{'name': 'Regulators'}, {'name': 'Entrepreneurship Advocacy groups'}, {'name': 'Government'}, {'name':'Others'}],

        # # 'Resources':[{'name':'Virtual Resources'}, {'name':'In-person Resources'}, {'name':'Tools'}, {'name':'Services'}, {'name':'Others'}],

        # 'Research and Development' :[{'name': 'Research Organizations/Centres'}, {'name': 'Others'}],
  
        # 'MSMEs and Startups':[{'name':'MSMEs'}, {'name':'Others'}]}
        
    data  = {'Business support': [{'name': 'Incubators'},
  {'name': 'Entrepreneurship Advocacy groups'},
  {'name': 'Resources'},
  {'name': 'Others'},
  {'name': 'Mentoring'},
  {'name': 'Government'},
  {'name': 'Research Organizations/Centres'},
  {'name': 'Regulators'},
  {'name': 'Accelerators'},
  {'name': 'Business Advisory'},
  {'name': 'Equity Funders'},
  {'name': 'Enterprise Support Organizations'}],
 'Funding': [{'name': 'Incubators'},
  {'name': 'Grant Providers'},
  {'name': 'Resources'},
  {'name': 'Others'},
  {'name': 'Government'},
  {'name': 'Research Organizations/Centres'},
  {'name': 'Loan Providers'},
  {'name': 'Crowdfunding'},
  {'name': 'Accelerators'},
  {'name': 'Business Advisory'},
  {'name': 'Equity Funders'},
  {'name': 'Enterprise Support Organizations'}],
 'MSMEs and Startups': [{'name': 'MSMEs'}, {'name': 'Startups'}],
 'Market Access': [{'name': 'Government'},
  {'name': 'Tech Platforms'},
  {'name': 'Organizations'}],
 'Policy and Regulation': [{'name': 'Entrepreneurship Advocacy groups'},
  {'name': 'Resources'},
  {'name': 'Government'},
  {'name': 'Organizations'},
  {'name': 'Research Organizations/Centres'},
  {'name': 'Loan Providers'},
  {'name': 'Regulators'},
  {'name': 'Enterprise Support Organizations'}],
 'Research and Development': [{'name': 'Resources'},
  {'name': 'Others'},
  {'name': 'Mentoring'},
  {'name': 'Government'},
  {'name': 'Research Organizations/Centres'},
  {'name': 'Loan Providers'},
  {'name': 'Business Advisory'},
  {'name': 'Enterprise Support Organizations'}],
 'Training': [{'name': 'Incubators'},
  {'name': 'Entrepreneurship Advocacy groups'},
  {'name': 'Resources'},
  {'name': 'Mentoring'},
  {'name': 'Research Organizations/Centres'},
  {'name': 'Regulators'},
  {'name': 'Enterprise Support Organizations'},
  {'name': 'Accelerators'},
  {'name': 'Business Advisory'},
  {'name': 'Equity Funders'},
  {'name': 'Government'}]}

    for key in data.keys():
        ecosystem = EcoSystem.objects.get(name=key)
        for val in data[key]:
            SubEcosystem.objects.create(**val, ecosystem=ecosystem)
            print(val['name'], 'Done')

        print(key, 'Done')
        print('====================\n')




def add_sector():
    """This function is clears all of the sectors in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    
    a = Sector.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    
    sectors = ['Development Sector',
                'Education',
                'Agribusiness',
                'Health',
                'Others',
                'Technology',
                'Manufacturing',
                'Public Sector',
                'Private Sector',
                'Creatives'
        ]


    for i in sectors:
        Sector.objects.create(name=i)
        print('{} Done'.format(i))


def populate_sub_ecosystem_sub_class():
    """This function is clears all of the sub ecosystem sub class in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    a = SubecosystemSubclass.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    
    data = {('Business support', 'Accelerators'): [{'name': ''}, {'name': 'Venture Capital'}, {'name': 'Mentoring'}], 
            ('Business support', 'Business Advisory'): [{'name': ''}, {'name': 'Tax'}, {'name': 'Legal'}, {'name': 'Human Resources'}, {'name': 'Book-Keeping'}, {'name': 'Mentoring'}, {'name': 'Venture Capital'}], 
            ('Business support', 'Incubators'): [{'name': ''}, {'name': 'Venture Capital'}, {'name': 'Mentoring'}], 
            ('Business support', 'Mentoring'): [{'name': ''}, {'name': 'Mentoring'}], 
            ('Business support', 'Resources'): [{'name': ''}, {'name': 'Venture Capital'}, {'name': 'Mentoring'}], 
            ('Funding', 'Crowdfunding'): [{'name': ''}], 
            ('Funding', 'Equity Funders'): [{'name': ''}, {'name': 'Angel Investors'}, {'name': 'Venture Capital'}, {'name': 'Mentoring'}], ('Funding', 'Grant Providers'): [{'name': ''}], 
            ('Funding', 'Loan Providers'): [{'name': ''}], 
            ('MSMEs and Startups', 'MSMEs'): [{'name': ''}], 
            ('MSMEs and Startups', 'Startups'): [{'name': ''}], 
            ('Market Access', 'Organizations'): [{'name': ''}], 
            ('Market Access', 'Tech Platforms'): [{'name': ''}], 
            ('Policy and Regulation', 'Entrepreneurship Advocacy groups'): [{'name': ''}], 
            ('Policy and Regulation', 'Government'): [{'name': ''}], 
            ('Policy and Regulation', 'Regulators'): [{'name': ''}], ('Research and Development', 'Others'): [{'name': ''}, {'name': 'Tax'}], 
            ('Research and Development', 'Research Organizations/Centres'): [{'name': ''}, {'name': 'Mentoring'}], 
            ('Training', 'Accelerators'): [{'name': ''}, {'name': 'Venture Capital'}, {'name': 'Mentoring'}], 
            ('Training', 'Enterprise Support Organizations'): [{'name': ''}, {'name': 'Venture Capital'}, {'name': 'Mentoring'}], 
            ('Training', 'Incubators'): [{'name': ''}, {'name': 'Venture Capital'}, {'name': 'Mentoring'}]}
    
    for i in data.keys():
        ecosystem = EcoSystem.objects.get(name=i[0])
        sub       = SubEcosystem.objects.get(name = i[1], ecosystem=ecosystem)
        for v in data[i]:
            if v['name']:
                SubecosystemSubclass.objects.create(name = v['name'], sub_ecosystem=sub, ecosystem=ecosystem)
                print(v['name'], " done")
        print(i, "Done")
        print()
    
    
    
    
    
    
    
    
    
    


################ DATA CLEANING FUNCTION #################

def process_data(file):
    """ This is a helper function that takes in the file that was uploaded, reads it with pandas and cleans the data for saving into the db. Check views.py, upload function for usage."""
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