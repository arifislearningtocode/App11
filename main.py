import pandas

df = pandas.read_csv("hotels.csv", dtype={'id': str})
dp = pandas.read_csv("cards.csv", dtype=str).to_dict(orient='records')
ds = pandas.read_csv("card_security.csv", dtype=str)

class Hotel:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def available(self):
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False


class ReservationTicket:

    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object


    def generate(self):
        content = f'''
        Thank you for the reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        '''

        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {'number': self.number, 'expiration': expiration,
                     'holder': holder, 'cvc': cvc}
        if card_data in dp:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = ds.loc[ds['number'] == self.number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            return False


class SpaReservation(Hotel):
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f'''
        Thank you for your SPA reservation!
        Here are your SPA booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        '''

        return content


print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard('1234')
    if credit_card.validate(expiration="12/26", holder='JOHN SMITH', cvc='123'):
        if credit_card.authenticate("mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(name, hotel)
            print(reservation_ticket.generate())
            spaquestion = input('Do you want to book a spa package? ')
            if spaquestion == 'yes':
                spa = SpaReservation(name, hotel)
                print(spa.generate())
        else:
            print('Wrong Password!')
    else:
        print('There was a problem with your payment.')
else:
    print("Hotel is not free.")


