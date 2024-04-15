# import functions from various packages
from typing import List
from typing import Optional
from sqlalchemy import Integer, String, Numeric, Date, desc, text, select, func
from sqlalchemy import ForeignKey, create_engine, Table, Column
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.orm import relationship, sessionmaker, Session

#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://postgres:C.@localhost/Phase3")

class Base(DeclarativeBase):
   pass

# Define Employee and client association table and columns
employee_client_association = Table(
   "employee_client_association", Base.metadata,
   Column("employee_id", Integer, ForeignKey("Employees.EmployeeID")),
   Column("client_id", String(40), ForeignKey("Clients.ClientID")),)


# Define Employees table
class Employee(Base):
   __tablename__ = "Employees"

   # Define Employees table columns
   EmployeeID: Mapped[int] = mapped_column(Integer, primary_key=True)
   EmployeeName: Mapped[str] = mapped_column(String(40))
   Clients = relationship("Client", secondary=employee_client_association, back_populates="Employees")

   def __repr__(self):
       return (f"Employee(EmployeeID={self.EmployeeID}, "
               f"EmployeeName={self.EmployeeName})")


# Define Clients table
class Client(Base):
   __tablename__ = "Clients"

   # Define Clients table columns
   ClientID: Mapped[str] = mapped_column(String(6), primary_key=True)
   Balance: Mapped[int] = mapped_column(Numeric)
   ClientNotes: Mapped[str] = mapped_column(String(50))
   FullName: Mapped[str] = mapped_column(String(50))
   PhoneNumber: Mapped[int] = mapped_column(Numeric(40))
   Email: Mapped[str] = mapped_column(String(50))
   Address: Mapped[str] = mapped_column(String(70))
   Employees = relationship("Employee", secondary=employee_client_association, back_populates='Clients')

   def __repr__(self):
       return (f"Client(ClientID={self.ClientID!r}, Balance={self.Balance!r}, "
               f"ClientNotes={self.ClientNotes!r}, FullName={self.FullName!r}, "
               f"PhoneNumber={self.PhoneNumber!r}, Email={self.Email!r}, "
               f"Address={self.Address!r}")


class jewelry(Base):
    __tablename__ = "jewelry"

    lotID: Mapped[int] = mapped_column(Integer, primary_key=True)
    styleID: Mapped[str] = mapped_column(String(20))
    MSRP: Mapped[int] = mapped_column(Integer)
    styleDescription: Mapped[str] = mapped_column(String(500))
    totalSize: Mapped[int] = mapped_column(Integer)
    largeStoneQual: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str: #represents the object as a string 
        return (f"jewelry(lotID={self.lotID!r}, "
                f"styleID={self.styleID!r}, "
                f"MSRP={self.MSRP!r}, "
                f"styleDescription={self.styleDescription!r}, "
                f"totalSize={self.totalSize!r}, "
                f"largeStoneQual={self.largeStoneQual!r})")

class Transactions(Base):
    __tablename__ = "Transactions"

    transactionID: Mapped[int] = mapped_column(Integer, primary_key=True)
    cash: Mapped[int] = mapped_column(Integer)
    ACH: Mapped[int] = mapped_column(Integer)
    CC: Mapped[int] = mapped_column(Integer)
    cclast4digits: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return (f"Transactions(transactionID={self.transactionID!r}, "
                f"cash={self.cash!r}, "
                f"ACH={self.ACH!r}, "
                f"CC={self.CC!r}, "
                f"cclast4digits={self.cclast4digits!r})")

class Orders(Base):
    __tablename__ = "Orders"

    order_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_date: Mapped[Date] = mapped_column(Date)
    shipping_cost: Mapped[int] = mapped_column(Integer)
    Sales_Tax_Code: Mapped[str] = mapped_column(String)
    ClientID: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return (f"Orders(order_ID={self.order_ID!r}, "
                f"order_date={self.order_date!r}, "
                f"shipping_cost={self.shipping_cost!r}, "
                f"Sales_Tax_Code={self.Sales_Tax_Code!r}, "
                f"ClientID={self.ClientID!r})")
  
class order_Line(Base):
    __tablename__ = "order_Line"

    lotID: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_ID: Mapped[Numeric] = mapped_column(Numeric, primary_key=True)
    unit_price: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    itemCount: Mapped[int] = mapped_column(Integer)
    lineNum: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return (f"order_Line(lotID={self.lotID!r}, "
                f"order_ID={self.order_ID!r}, "
                f"unit_price={self.unit_price!r}, "
                f"itemCount={self.itemCount!r}, "
                f"lineNum={self.lineNum!r})")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

#Insert Data
with Session(engine) as session:
    # insert values into Employee class - streamlined by defining all client objects within a single list and then just inserting the list instead of each object
    Emps = [
        Employee(EmployeeID=3789, EmployeeName="Ethan Johnson"),
        Employee(EmployeeID=3678, EmployeeName="Emily Brown"),
        Employee(EmployeeID=3965, EmployeeName="Martinize Rodriguez"),
        Employee(EmployeeID=3098, EmployeeName="Mahmood Ibrahim"),
        Employee(EmployeeID=3094, EmployeeName="Mira Jin",),
        Employee(EmployeeID=3021, EmployeeName="Anna Mei"),
        Employee(EmployeeID=3111, EmployeeName="Fatima Bilal")
    ]

# insert values into Client class
    Clients = [
        Client(ClientID="A123", Balance=500, ClientNotes="VIP Customer", FullName="John Johnson", PhoneNumber=1234567890, Email="john@yahoo.com", Address="3522 S State St, Chicago IL 60609"),
        Client(ClientID="D456", Balance=750, ClientNotes="Product issue reported", FullName="Jane Lee", PhoneNumber=9876543210, Email="jane@gmail.com", Address="Quad, 3330 S Michigan Ave Chicago IL 60616"),
        Client(ClientID="G789", Balance=300, ClientNotes="Referral from colleague", FullName="Michael Johnson", PhoneNumber=5551234567, Email="michael@outlook.com", Address="2230 Main St Evanston IL 60202"),
        Client(ClientID="J012", Balance=1000, ClientNotes="Request watch repair", FullName="Emily Brown", PhoneNumber=4445678901, Email="emilyBrown@yahoo.com", Address="10010 Grey Ave Evanston IL 60202"),
        Client(ClientID="O345", Balance=200, ClientNotes="Inquired about Patek Philip watches", FullName="David Lee", PhoneNumber=6667890123, Email="david@gmail.com", Address="2527 Marcy Ave Evanston IL 60201"),
        Client(ClientID="R678", Balance=600, ClientNotes="upcoming wedding, inquired about engagement ring", FullName="Sarah Wilson", PhoneNumber=2223456789, Email="sarah@outlook.com", Address="2527 Marcy Ave, Evanston, IL 60201"),
        Client(ClientID="U901", Balance=850, ClientNotes="Referral from colleague", FullName="Chris Lewis", PhoneNumber=7778901234, Email="chris@yahoo.com", Address="4635 Malden St, Chicago, IL 60640"),
        Client(ClientID="X234", Balance=400, ClientNotes="VIP Customer", FullName="Jessica Martinez", PhoneNumber=3336789012, Email="jessica@gmail.com", Address="4726 N Beacon St, Chicago, IL 60640"),
        Client(ClientID="A567", Balance=1200, ClientNotes="Product issue reported", FullName="Ryan Garcia", PhoneNumber=8889012345, Email="ryan@outlook.com", Address="4706 N Racine Ave, Chicago, IL 60640"),
        Client(ClientID="D890", Balance=700, ClientNotes="VIP Customer", FullName="Amanda Rodriguez", PhoneNumber=1114567890, Email="amanda@yahoo.com", Address="4745 N Dover St, Chicago, IL 60640"),
        Client(ClientID="G123", Balance=550, ClientNotes="Asked about Moon Phase", FullName="Daniel White", PhoneNumber=9995678901, Email="daniel@gmail.com", Address="Chicago, IL 60606"),
        Client(ClientID="H456", Balance=950, ClientNotes="Product issue reported", FullName="Jennifer Nguyen", PhoneNumber=6661234567, Email="jennifer@outlook.com", Address="499-411 W Washington St, Chicago, IL 60606"),
        Client(ClientID="K789", Balance=350, ClientNotes="Asked about Rolex", FullName="Matthew Scott", PhoneNumber=8882345678, Email="matthew@yahoo.com", Address="218 N Jefferson St, Chicago, IL 60661"),
        Client(ClientID="N012", Balance=800, ClientNotes="Referral from colleague", FullName="Lisa Carter", PhoneNumber=4446789012, Email="lisa@gmail.com", Address="1330 W Chicago Ave, Chicago, IL 60653"),
        Client(ClientID="Q345", Balance=250, ClientNotes="Asked about Rolex was not in stock", FullName="Ashley Martinez", PhoneNumber=7779012345, Email="ashley@outlook.com", Address="1220 N Bosworth Ave, Chicago, IL 60642"),
        Client(ClientID="T678", Balance=1100, ClientNotes="Inquired on product catalog", FullName="Mark Thompson", PhoneNumber=2223456789, Email="mark@yahoo.com", Address="1220 N Bosworth Ave, Chicago, IL 60642"),
        Client(ClientID="V901", Balance=500, ClientNotes="Inquired on product catalog", FullName="Nicole Hall", PhoneNumber=3339012345, Email="nicole@gmail.com", Address="1325 N Bosworth Ave, Chicago, IL 60642"),
        Client(ClientID="Z234", Balance=400, ClientNotes="Inquired on product catalog", FullName="Brandon Lewis", PhoneNumber=8886789012, Email="brandon@outlook.com", Address="1544 N Ashland Ave, Chicago, IL 60622"),
        Client(ClientID="B567", Balance=900, ClientNotes="no purchase was made", FullName="Rachel Turner", PhoneNumber=1117890123, Email="rachel@yahoo.com", Address="7560 Oak Ave, River Forest, IL 60305"),
        Client(ClientID="F890", Balance=600, ClientNotes="Referral from colleague", FullName="Justin Moore", PhoneNumber=9992345678, Email="justin@gmail.com", Address="398-322 Melrose Ave, Kenilworth, IL 60043"),
        Client(ClientID="M123", Balance=450, ClientNotes="Asked about warranty", FullName="Michelle Adams", PhoneNumber=5557890123, Email="michelle@gmail.com", Address="3522 S State St, Chicago IL 60609"),
        Client(ClientID="L456", Balance=2000, ClientNotes="VIP Customer", FullName="Kevin Wilson", PhoneNumber=7770123456, Email="kevin@yahoo.com", Address="4726 N Beacon St, Chicago, IL 60640"),
        Client(ClientID="P789", Balance=300, ClientNotes="Product issue reported", FullName="Samantha Taylor", PhoneNumber=3335678901, Email="samantha@hotmail.com", Address="2527 Marcy Ave Evanston IL 60201"),
        Client(ClientID="R012", Balance=30, ClientNotes="Inquired about delivery", FullName="Patrick Brown", PhoneNumber=8886789012, Email="patrick@gmail.com", Address="2527 Marcy Ave, Evanston, IL 60201"),
        Client(ClientID="S345", Balance=5000, ClientNotes="Referral from friend", FullName="Christina Hernandez", PhoneNumber=1112345678, Email="christina@yahoo.com", Address="7560 Oak Ave, River Forest, IL 60305"),
        Client(ClientID="W678", Balance=800, ClientNotes="Asked about product availability", FullName="Andrew Martinez", PhoneNumber=9997890123, Email="andrew@gmail.com", Address="1220 N Bosworth Ave, Chicago, IL 60642"),
        Client(ClientID="Y901", Balance=340, ClientNotes="VIP Customer", FullName="Stephanie Nguyen", PhoneNumber=4440123456, Email="stephanie@hotmail.com", Address="3522 S State St, Chicago IL 60609"),
        Client(ClientID="X9020", Balance=750, ClientNotes="Product issue reported", FullName="Thomas Lee", PhoneNumber=6665678901, Email="thomas@yahoo.com", Address="4635 Malden St, Chicago, IL 60640"),
        Client(ClientID="B500", Balance=1250, ClientNotes="Inquired about return policy", FullName="Jessica Hernandez", PhoneNumber=8882345678, Email="jessica@hotmail.com", Address="4745 N Dover St, Chicago, IL 60640"),
        Client(ClientID="C890", Balance=690, ClientNotes="Referral from colleague", FullName="Brandon Smith", PhoneNumber=7773456789, Email="brandon@gmail.com", Address="499-411 W Washington St, Chicago, IL 60606")
    ]

    jewelry_inventory = [
        jewelry(lotID=200001, styleID='watch', MSRP=52000, styleDescription='Patek Philippe Nautilus Moon Phase - SS, jubilee strap', totalSize=40, largeStoneQual='no stones'),
        jewelry(lotID=200002, styleID='watch', MSRP=55000, styleDescription='Patek Philippe Nautilus Moon Phase - Rose Gold', totalSize=40, largeStoneQual='no stones'),
        jewelry(lotID=200003, styleID='watch', MSRP=40000, styleDescription='Rolex Day Date, 36mm, platinum, diamond bezel', totalSize=36, largeStoneQual='1tcw, G/VVS'),
        jewelry(lotID=200004, styleID='watch', MSRP=44500, styleDescription='Rolex Daytona, 40mm, 18kt Rose Gold, solid links', totalSize=40, largeStoneQual='no stones'),
        jewelry(lotID=200005, styleID='RG-ER', MSRP=24000, styleDescription='Platinum engagement RG. Eternity, 1.5tcw melee, 2ct E/VVS2 center stone, size 4', totalSize=4, largeStoneQual='2ct, E/VVS2'),
        jewelry(lotID=200006, styleID='AB', MSRP=9500, styleDescription='Platinum AB, 50%, 1.0tcw, size 4', totalSize=4, largeStoneQual='FG/VS1'),
        jewelry(lotID=200007, styleID='RG-ER', MSRP=20000, styleDescription='RG-ER A.Jaffe designer engagement RG-S. 14KW, solitaire, size 5', totalSize=5, largeStoneQual='1.5ct, D/VVS1'),
        jewelry(lotID=200008, styleID='AB', MSRP=1500, styleDescription='14KW, Solid metal yellow gold band. 3mm width, size 5', totalSize=5, largeStoneQual='no stones'),
        jewelry(lotID=200009, styleID='BR', MSRP=27000, styleDescription='14KW, tennis bracelet, 6tcw, 12inches long', totalSize=12, largeStoneQual='FG/VVS2'),
        jewelry(lotID=200010, styleID='PT', MSRP=14500, styleDescription='1ct. diamond bezel pendant, 14KY bezel and 18in 14KY rolo chain - 2.1mm', totalSize=18, largeStoneQual='1tcw E/VVS2'),
        jewelry(lotID=200011, styleID='watch', MSRP=52000, styleDescription='Patek Philippe Nautilus Moon Phase - SS, jubilee strap', totalSize=40, largeStoneQual='no stones'),
        jewelry(lotID=200012, styleID='watch', MSRP=12000, styleDescription='Rolex Submarine Two Tone Blue Dial Circa 2002', totalSize=40, largeStoneQual='no stones'),
        jewelry(lotID=200013, styleID='watch', MSRP=7900, styleDescription='Rolex Datejust Roulette Dial Circa 2007', totalSize=36, largeStoneQual='no stones'),
        jewelry(lotID=200014, styleID='watch', MSRP=10200, styleDescription='Rolex President Gold Dial Diamond Bezel Circa 1991 - 1tcw', totalSize=26, largeStoneQual='FG/VS'),
        jewelry(lotID=200015, styleID='EA', MSRP=7650, styleDescription='18KW - 7.31grams, Inside Outside Diamond Hoop Earrings measuring 3/4" x 5/8"', totalSize=1, largeStoneQual='3.1ct, G/VS'),
        jewelry(lotID=200016, styleID='EA', MSRP=3000, styleDescription='14K Black Rhodium Plated Gold Hoop Earrings w/ Black Diamond ', totalSize=1, largeStoneQual='130 round black diamonds'),
        jewelry(lotID=200017, styleID='RG-S', MSRP=28500, styleDescription='Platinum RG-S, Tanzanite solitaire RG, 9.04ct emerald cut, size 6', totalSize=6, largeStoneQual='9.04tcw'),
        jewelry(lotID=200018, styleID='AB', MSRP=3500, styleDescription='18KW, Tiffany & Co, Tiffany Lock RG, w/ 50% pave round dias', totalSize=5, largeStoneQual='.14tcw, FG/VS'),
        jewelry(lotID=200019, styleID='RG', MSRP=27000, styleDescription='18KY, Signet RG, Tiffany & Co, solid metal', totalSize=6, largeStoneQual='no stones'),
        jewelry(lotID=200020, styleID='CH', MSRP=175, styleDescription='Stainless Steel, yellow solid flat curb chain, 18inches long, 3mm', totalSize=18, largeStoneQual='no stones'),
        jewelry(lotID=200021, styleID='CH', MSRP=5500, styleDescription='14KY, solid miami cuban, 18", 6mm', totalSize=18, largeStoneQual='no stones'),
        jewelry(lotID=200022, styleID='CH', MSRP=7300, styleDescription='14KW, solid miami cuban, 24", 6mm', totalSize=24, largeStoneQual='no stones'),
        jewelry(lotID=200023, styleID='CH', MSRP=3400, styleDescription='14KR, solid Rose Gold Rope CH, 20", 4mm', totalSize=20, largeStoneQual='no stones'),
        jewelry(lotID=200024, styleID='CH', MSRP=5000, styleDescription='14KW, solid Franco CH, 20", 4mm', totalSize=20, largeStoneQual='no stones'),
        jewelry(lotID=200025, styleID='RG-CT', MSRP=1900, styleDescription='18KR, Citrine and diamond halo cocktail ring, 7.3g of gold, 9.31ct yellow Citrine, (32)0.32tcw round melee dia cathedral, size 6', totalSize=6, largeStoneQual='0.32tcw GH/VS'),
        jewelry(lotID=200026, styleID='PB', MSRP=700, styleDescription='14KW, RG-Plain band. Solid white gold, high polish, 3mm width, size 9', totalSize=9, largeStoneQual='2tcw emeralds'),
        jewelry(lotID=200027, styleID='DI(OV)', MSRP=25000, styleDescription='Round Brilliant 1.72ct G/VVS1 GIA certified', totalSize=0, largeStoneQual='1.72ct G/VVS1'),
        jewelry(lotID=200028, styleID='CF', MSRP=14850, styleDescription='14KW, Vintage Cabachon and Carved Emerald Cuff-links, 2tcw natural emeralds', totalSize=0, largeStoneQual='2tcw PS-EM'),
        jewelry(lotID=200029, styleID='DI(RB)', MSRP=3400, styleDescription='Round Brilliant 1ct F/VS1 noncertified', totalSize=0, largeStoneQual='1ct F/VS1'),
        jewelry(lotID=200030, styleID='DI(RB)', MSRP=20000, styleDescription='Round Brilliant 1.45ct D/VVS1 GIA certified', totalSize=0, largeStoneQual='1.45ct D/VVS1'),
        jewelry(lotID=200031, styleID='DI(EM)', MSRP=35000, styleDescription='Emerald cut, 2.01ct F/VVS2 GIA certified', totalSize=0, largeStoneQual='2.01ct F/VVS2'),
        jewelry(lotID=200032, styleID='RG-ER', MSRP=1400, styleDescription='14KW, custom RG-ER, no center stone, cathedral setting, high polish, 50% DI(RB) LAB melee, (20)0.45tcw FG/VS', totalSize=0, largeStoneQual='LAB melee (20)0.45tcw FG/VS')
    ]

    Tx = [
        Transactions(transactionID=1000001, cash=0, ACH=57000, CC=0, cclast4digits=0),
        Transactions(transactionID=1000002, cash=0, ACH=0, CC=55400, cclast4digits=3281),
        Transactions(transactionID=1000003, cash=0, ACH=40000, CC=0, cclast4digits=0),
        Transactions(transactionID=1000004, cash=0, ACH=44500, CC=0, cclast4digits=0),
        Transactions(transactionID=1000005, cash=0, ACH=24000, CC=0, cclast4digits=0),
        Transactions(transactionID=1000006, cash=0, ACH=9700, CC=0, cclast4digits=0),
        Transactions(transactionID=1000007, cash=0, ACH=20000, CC=0, cclast4digits=0),
        Transactions(transactionID=1000008, cash=0, ACH=1500, CC=0, cclast4digits=0),
        Transactions(transactionID=1000009, cash=0, ACH=0, CC=27400, cclast4digits=4213),
        Transactions(transactionID=1000010, cash=0, ACH=14500, CC=0, cclast4digits=0),
        Transactions(transactionID=1000011, cash=0, ACH=52000, CC=0, cclast4digits=0),
        Transactions(transactionID=1000012, cash=0, ACH=0, CC=12300, cclast4digits=3519),
        Transactions(transactionID=1000013, cash=0, ACH=7900, CC=0, cclast4digits=0),
        Transactions(transactionID=1000014, cash=0, ACH=10200, CC=0, cclast4digits=0),
        Transactions(transactionID=1000015, cash=0, ACH=7650, CC=0, cclast4digits=0),
        Transactions(transactionID=1000016, cash=0, ACH=3200, CC=0, cclast4digits=0),
        Transactions(transactionID=1000017, cash=0, ACH=28500, CC=0, cclast4digits=0),
        Transactions(transactionID=1000018, cash=0, ACH=5500, CC=0, cclast4digits=0),
        Transactions(transactionID=1000019, cash=0, ACH=0, CC=29100, cclast4digits=4877),
        Transactions(transactionID=1000020, cash=0, ACH=35000, CC=0, cclast4digits=0)
    ]

    Ords = [
        Orders(order_ID=11, order_date='2022-03-14', shipping_cost=0, Sales_Tax_Code='IL', ClientID='A123'),
        Orders(order_ID=12, order_date='2022-04-02', shipping_cost=400, Sales_Tax_Code='OOS', ClientID='D456'),
        Orders(order_ID=13, order_date='2022-02-26', shipping_cost=0, Sales_Tax_Code='IL', ClientID='G789'),
        Orders(order_ID=14, order_date='2022-12-17', shipping_cost=0, Sales_Tax_Code='IL', ClientID='J012'),
        Orders(order_ID=15, order_date='2022-08-08', shipping_cost=0, Sales_Tax_Code='IL', ClientID='O345'),
        Orders(order_ID=16, order_date='2023-06-11', shipping_cost=200, Sales_Tax_Code='WS', ClientID='R678'),
        Orders(order_ID=17, order_date='2023-07-01', shipping_cost=0, Sales_Tax_Code='IL', ClientID='U901'),
        Orders(order_ID=18, order_date='2023-01-15', shipping_cost=200, Sales_Tax_Code='WS', ClientID='X234'),
        Orders(order_ID=19, order_date='2023-06-22', shipping_cost=400, Sales_Tax_Code='OOS', ClientID='A567'),
        Orders(order_ID=20, order_date='2023-09-13', shipping_cost=0, Sales_Tax_Code='IL', ClientID='D890'),
        Orders(order_ID=21, order_date='2022-05-25', shipping_cost=0, Sales_Tax_Code='IL', ClientID='M123'),
        Orders(order_ID=22, order_date='2022-07-12', shipping_cost=300, Sales_Tax_Code='OOS', ClientID='L456'),
        Orders(order_ID=23, order_date='2022-09-03', shipping_cost=0, Sales_Tax_Code='IL', ClientID='P789'),
        Orders(order_ID=24, order_date='2022-11-20', shipping_cost=0, Sales_Tax_Code='IL', ClientID='R012'),
        Orders(order_ID=25, order_date='2023-02-28', shipping_cost=0, Sales_Tax_Code='IL', ClientID='S345'),
        Orders(order_ID=26, order_date='2023-04-15', shipping_cost=200, Sales_Tax_Code='WS', ClientID='W678'),
        Orders(order_ID=27, order_date='2023-08-01', shipping_cost=0, Sales_Tax_Code='IL', ClientID='Y901'),
        Orders(order_ID=28, order_date='2023-10-22', shipping_cost=200, Sales_Tax_Code='WS', ClientID='X9020'),
        Orders(order_ID=29, order_date='2023-12-09', shipping_cost=400, Sales_Tax_Code='OOS', ClientID='B500'),
        Orders(order_ID=30, order_date='2024-01-31', shipping_cost=0, Sales_Tax_Code='IL', ClientID='C890')
    ]

    o_Lines = [
        order_Line(lotID=200001, order_ID=11, unit_price=52000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200020, order_ID=11, unit_price=5000.00, itemCount=1, lineNum=2),
        order_Line(lotID=200002, order_ID=12, unit_price=55000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200003, order_ID=13, unit_price=40000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200004, order_ID=14, unit_price=44500.00, itemCount=1, lineNum=1),
        order_Line(lotID=200005, order_ID=15, unit_price=24000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200006, order_ID=16, unit_price=9500.00, itemCount=1, lineNum=1),
        order_Line(lotID=200007, order_ID=17, unit_price=20000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200008, order_ID=18, unit_price=1500.00, itemCount=1, lineNum=1),
        order_Line(lotID=200009, order_ID=19, unit_price=27000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200010, order_ID=20, unit_price=14500.00, itemCount=1, lineNum=1),
        order_Line(lotID=200011, order_ID=21, unit_price=52000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200012, order_ID=22, unit_price=12000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200013, order_ID=23, unit_price=7900.00, itemCount=1, lineNum=1),
        order_Line(lotID=200014, order_ID=24, unit_price=10200.00, itemCount=1, lineNum=1),
        order_Line(lotID=200015, order_ID=25, unit_price=7650.00, itemCount=1, lineNum=1),
        order_Line(lotID=200016, order_ID=26, unit_price=3000.00, itemCount=1, lineNum=1),
        order_Line(lotID=200017, order_ID=27, unit_price=2850.00, itemCount=1, lineNum=1),
        order_Line(lotID=200025, order_ID=28, unit_price=1900.00, itemCount=1, lineNum=1),
        order_Line(lotID=200029, order_ID=28, unit_price=3400.00, itemCount=1, lineNum=2),
        order_Line(lotID=200026, order_ID=29, unit_price=700.00, itemCount=1, lineNum=1),
        order_Line(lotID=200032, order_ID=29, unit_price=3000.00, itemCount=1, lineNum=2),
        order_Line(lotID=200027, order_ID=29, unit_price=25000.00, itemCount=1, lineNum=3),
        order_Line(lotID=200031, order_ID=30, unit_price=35000.00, itemCount=1, lineNum=1)
    ]

#Assign clients to the employee to represent the many-to-many relationship - edited to match streamlined list insertion of objects by using index-based reference
Emps[0].Clients.extend([Clients[0], Clients[3], Clients[7], Clients[8], Clients[9], Clients[14], Clients[24], Clients[28]])
Emps[1].Clients.extend([Clients[1], Clients[2], Clients[4], Clients[5], Clients[7], Clients[19], Clients[21], Clients[26]])
Emps[2].Clients.extend([Clients[3], Clients[9], Clients[14], Clients[17], Clients[20], Clients[23], Clients[27], Clients[29]])
Emps[3].Clients.extend([Clients[3], Clients[4], Clients[6], Clients[17], Clients[18], Clients[23]])
Emps[4].Clients.extend([Clients[0], Clients[1], Clients[5], Clients[8], Clients[10], Clients[11], Clients[15]])
Emps[5].Clients.extend([Clients[8], Clients[9], Clients[12], Clients[16], Clients[22], Clients[23], Clients[25]])
Emps[6].Clients.extend([Clients[11], Clients[12], Clients[13], Clients[16], Clients[18], Clients[25], Clients[29]])

session.add_all(Emps + Clients + jewelry_inventory + Tx + Ords + o_Lines)
session.commit()

# Simple Queries
session = Session(engine)  

stmt = (
    select(jewelry.styleID, func.count(order_Line.lotID).label('items_sold'), func.sum(order_Line.unit_price * order_Line.itemCount).label('total_sales'))
    .join(order_Line, jewelry.lotID == order_Line.lotID)
    .join(Orders, order_Line.order_ID == Orders.order_ID)
    .where(jewelry.styleID == 'watch') #slight addition from phase2 query. This only returns the values for watches. Remove this for phase2 query
    .group_by(jewelry.styleID)
    .order_by(func.count(order_Line.lotID).desc(), func.sum(order_Line.unit_price * order_Line.itemCount).desc())
)

salesReport = session.execute(stmt).all()

print("## Jewelry Sales Report (by Category) ##")
for result in salesReport:
    print(f"Style ID: {result.styleID:<10} Items Sold: {result.items_sold:<3} Total Sales: ${result.total_sales:,.2f}") #added spacing formatting for better aesthetics on command prompt


# Teammate's query to select client with the highest balance and number of employees who had provided services to said employee
# limiting by five with the highest amount of balance
result = (session.query(Client.FullName,
            func.count(Employee.EmployeeID).label('serviced_by'),
            func.sum(Client.Balance).label('total_remaining_balance'))) \
    .select_from(Client) \
    .join(employee_client_association) \
    .join(Employee) \
    .group_by(Client.FullName) \
    .order_by(desc(text('total_remaining_balance'))) \
    .limit(4) \
    .all()

# Print the results
for row in result:
    client_name, serviced_by, total_balance = row
    print(f"Client Name: {client_name}, Serviced by: {serviced_by}, Total Remaining Balance: {total_balance}")

# # Close the session
# session.close()
