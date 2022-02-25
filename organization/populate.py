from account.send_notice import User
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
    user = User.objects.last()
    with open('organization/new_revised_data.csv', mode='r', encoding='UTF-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # line_count = 0
        orgs = []
        for row in csv_reader:
            row['sector'] = Sector.objects.get(name = str(row['sector']))
            # print(row['ecosystem'])
            row['ecosystem'] = EcoSystem.objects.get(name = str(row['ecosystem']))
            
            row['sub_ecosystem'] = SubEcosystem.objects.get(name = str(row['sub_ecosystem']), ecosystem=row['ecosystem'])
            
            if row['sub_ecosystem_sub_class']:
                row['sub_ecosystem_sub_class'] = SubecosystemSubclass.objects.get(name=str(row['sub_ecosystem_sub_class']), sub_ecosystem=row['sub_ecosystem'], ecosystem=row['ecosystem'])
                
            else:
                s = row.pop('sub_ecosystem_sub_class')
            if any(org.name==row['name'] for org in orgs):
                print(f"Did not add {row['name']}")
                continue
            orgs.append(Organization(**row, is_active=True, responded = True, is_approved=True, user=user))
    Organization.objects.bulk_create(orgs)
        


def populate_sub():
    """This function is clears all of the sub_ecosystem in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    
    a = SubEcosystem.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")


    data=[('Business support', 'Accelerators'), ('Business support', 'Business Advisory'), ('Business support', 'Incubators'), ('Business support', 'Resources'), ('Funding', 'Crowdfunding'), ('Funding', 'Equity Funders'), ('Funding', 'Grant Providers'), ('Funding', 'Loan Providers'), ('MSMEs and Startups', 'MSMEs'), ('MSMEs and Startups', 'Startups'), ('Market Access', 'Organizations That Facilitate Trade'), ('Market Access', 'Tech Platforms'), ('Policy and Regulation', 'Entrepreneurship Advocacy Groups'), ('Policy and Regulation', 'Government'), ('Policy and Regulation', 'Regulators'), ('Research and Development', 'Research Organizations/Centres'), ('Training', 'Accelerators'), ('Training', 'Enterprise Support Organizations'), ('Training', 'Incubators')]

    for key in data:
        ecosystem = EcoSystem.objects.get(name=key[0])
        
        SubEcosystem.objects.create(name=key[1], ecosystem=ecosystem)
        print(key, 'Done')

        print('====================\n')




def add_sector():
    """This function is clears all of the sectors in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    
    a = Sector.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    
    sectors = ['Manufacturing',
            'Education',
            'Private Sector',
            'Creatives',
            'Agribusiness',
            'Health',
            'Others',
            'Technology',
            'Development Sector',
            'Public Sector']


    for i in sectors:
        Sector.objects.create(name=i)
        print('{} Done'.format(i))


def populate_sub_ecosystem_sub_class():
    """This function is clears all of the sub ecosystem sub class in the db and populates it with new ones. Only used to populate staging data must not be run in production"""
    a = SubecosystemSubclass.objects.all()
    a.delete()
    print("Cleared former data")
    print("=================\nWorking on new data\n")
    
    data = [('Business support', 'Accelerators', ''), ('Business support', 'Business Advisory', 'Book-Keeping'), ('Business support', 'Business Advisory', 'Human Resources'), ('Business support', 'Business Advisory', 'Legal'), ('Business support', 'Business Advisory', 'Mentoring'), ('Business support', 'Business Advisory', 'Tax'), ('Business support', 'Incubators', ''), ('Business support', 'Resources', ''), ('Funding', 'Crowdfunding', ''), ('Funding', 'Equity Funders', 'Angel Investors'), ('Funding', 'Equity Funders', 'Venture Capital'), ('Funding', 'Grant Providers', ''), ('Funding', 'Loan Providers', ''), ('MSMEs and Startups', 'MSMEs', ''), ('MSMEs and Startups', 'Startups', ''), ('Market Access', 'Organizations That Facilitate Trade', ''), ('Market Access', 'Tech Platforms', ''), ('Policy and Regulation', 'Entrepreneurship Advocacy Groups', ''), ('Policy and Regulation', 'Government', ''), ('Policy and Regulation', 'Regulators', ''), ('Research and Development', 'Research Organizations/Centres', ''), ('Training', 'Accelerators', ''), ('Training', 'Enterprise Support Organizations', ''), ('Training', 'Incubators', '')]
    
    for i in data:
        ecosystem = EcoSystem.objects.get(name=i[0])
        sub       = SubEcosystem.objects.get(name = i[1], ecosystem=ecosystem)
        
        if i[2]:
            SubecosystemSubclass.objects.create(name = i[2], sub_ecosystem=sub, ecosystem=ecosystem)
            print(i[2], " done")
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
    revised_data.rename(columns={'subclass_subecosystem':'sub_ecosystem_sub_class'}, inplace=True)
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