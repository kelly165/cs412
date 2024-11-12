from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    voter_id_number = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=255)
    apartment_number = models.IntegerField(null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=10)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def load_data():
    '''Load data records from a CSV file into Voter model instances.'''

    # Clear out any existing Voter records
    Voter.objects.all().delete()

    # Define the file path to the CSV file
    filename = '/Users/kellychen/Downloads/newton_voters.csv'  # Adjust the path as needed
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip the header row
        print(f"Headers: {headers}")

        # Iterate over each row in the CSV file
        for row in reader:
            try:
                # Parse each field with safety checks
                date_of_birth = datetime.strptime(row[7], "%Y-%m-%d").date() if row[7] else None
                date_of_registration = datetime.strptime(row[8], "%Y-%m-%d").date() if row[8] else None
                v20state = row[11] == 'TRUE'
                v21town = row[12] == 'TRUE'
                v21primary = row[13] == 'TRUE'
                v22general = row[14] == 'TRUE'
                v23town = row[15] == 'TRUE'
                voter_score = int(row[16]) if row[16].isdigit() else 0

                # Safely parse street_number and apartment_number to integers or None if empty
                street_number = int(row[3]) if row[3].isdigit() else None
                apartment_number = int(row[5]) if row[5].isdigit() else None

                # Strip any trailing whitespace in party_affiliation
                party_affiliation = row[9].strip() if row[9] else None

                # Create and save the Voter instance
                voter = Voter(
                    voter_id_number=row[0],
                    last_name=row[1],
                    first_name=row[2],
                    street_number=street_number,
                    street_name=row[4],
                    apartment_number=apartment_number,
                    zip_code=row[6],
                    date_of_birth=date_of_birth,
                    date_of_registration=date_of_registration,
                    party_affiliation=party_affiliation,
                    precinct_number=row[10],
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=voter_score,
                )
                voter.save()  # Save this instance to the database
                print(f'Created voter: {voter}')

            except Exception as e:
                # Log the error for this row
                print(f"Error processing row {row}: {e}")
