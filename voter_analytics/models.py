from django.db import models

class Voter(models.Model):
    '''
    Store/represent voter data with participation information from recent elections.
    Includes:
    Last Name, First Name, Residential Address - Street Number, Residential Address - Street Name,
    Residential Address - Apartment Number, Residential Address - Zip Code, Date of Birth,
    Date of Registration, Party Affiliation, Precinct Number, Election participation indicators, Voter Score.
    '''
    # Voter identification and address fields
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    residential_address_street_number = models.CharField(max_length=10)
    residential_address_street_name = models.CharField(max_length=100)
    residential_address_apartment_number = models.CharField(max_length=10, blank=True, null=True)
    residential_address_zip_code = models.CharField(max_length=10)
    
    # Other voter details
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    
    # Election participation fields
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    @property
    def voter_score(self):
        '''Calculate voter score based on participation in the past 5 elections.'''
        participation_fields = [self.v20state, self.v21town, self.v21primary, self.v22general, self.v23town]
        return sum(participation_fields)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}, Voter Score: {self.voter_score}"

def load_data():
    '''Function to load voter data records from a CSV file into Django model instances.'''
    filename = '/Users/rpetr/Desktop/CS412/HW10/newton_voters.csv'
    with open(filename) as f:
        f.readline()
        for line in f:
            fields = line.strip().split(',')

            try:
                # Create a new instance of Voter with this record from the CSV
                voter = Voter(
                    last_name=fields[1],   # Last Name
                    first_name=fields[2],  # First Name
                    residential_address_street_number=fields[3],  # Street Number
                    residential_address_street_name=fields[4],    # Street Name
                    residential_address_apartment_number=fields[5] if fields[5] else None,  # Apartment Number (optional)
                    residential_address_zip_code=fields[6],       # Zip Code
                    date_of_birth=fields[7],                     # Date of Birth (YYYY-MM-DD)
                    date_of_registration=fields[8],              # Date of Registration (YYYY-MM-DD)
                    party_affiliation=fields[9].strip(),         # Party Affiliation
                    precinct_number=fields[10],                  # Precinct Number
                    v20state=fields[11] == 'TRUE',               # Participation in 2020 state election
                    v21town=fields[12] == 'TRUE',                # Participation in 2021 town election
                    v21primary=fields[13] == 'TRUE',             # Participation in 2021 primary election
                    v22general=fields[14] == 'TRUE',             # Participation in 2022 general election
                    v23town=fields[15] == 'TRUE'                 # Participation in 2023 town election
                )
                voter.save()  # Commit to database
                #print(f'Created voter: {voter}')

            except Exception as e:
                None
                #print(f"Skipped: {fields}, due to error: {e}")

    print(f'Done. Created {Voter.objects.count()} Voter records.')