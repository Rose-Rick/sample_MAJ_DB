# import functions from various packages
from typing import List
from typing import Optional
from sqlalchemy import Integer, String, Numeric, Date
from sqlalchemy import ForeignKey, create_engine, Table, Column
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.orm import relationship, sessionmaker, Session

#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://postgres:ChicagoCharlotte23.@localhost/Phase3")

class Base(DeclarativeBase):
   pass

# # Define Employee and client association table and columns
# employee_client_association = Table(
#    "employee_client_association", Base.metadata,
#    Column("employee_id", Integer, ForeignKey("Employees.EmployeeID")),
#    Column("client_id", String(40), ForeignKey("Clients.ClientID")),)

# # Define Employees table
# class Employee(Base):
#    __tablename__ = "Employees"

#    # Define Employees table columns
#    EmployeeID: Mapped[int] = mapped_column(Integer, primary_key=True)
#    EmployeeName: Mapped[str] = mapped_column(String(40))
#    Clients = relationship("Client", secondary=employee_client_association,
#                           back_populates="Employees")

#    def __repr__(self):
#        return (f"Employee(EmployeeID={self.EmployeeID}, "
#                f"EmployeeName={self.EmployeeName})")

#TODO populate jewelry and Transactions
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
            f"TransactionID={self.TransactionID!r}), "
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
#Create Tables
Base.metadata.create_all(engine)

#Insert Data
with Session(engine) as session:

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
        Transactions(transactionID=1000001, cash=0, ACH=57000, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000002, cash=0, ACH=0, CC=55400, CClast4Digits=3281),
        Transactions(transactionID=1000003, cash=0, ACH=40000, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000004, cash=0, ACH=44500, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000005, cash=0, ACH=24000, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000006, cash=0, ACH=9700, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000007, cash=0, ACH=20000, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000008, cash=0, ACH=1500, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000009, cash=0, ACH=0, CC=27400, CClast4Digits=4213),
        Transactions(transactionID=1000010, cash=0, ACH=14500, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000011, cash=0, ACH=52000, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000012, cash=0, ACH=0, CC=12300, CClast4Digits=3519),
        Transactions(transactionID=1000013, cash=0, ACH=7900, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000014, cash=0, ACH=10200, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000015, cash=0, ACH=7650, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000016, cash=0, ACH=3200, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000017, cash=0, ACH=28500, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000018, cash=0, ACH=5500, CC=0, CClast4Digits=0),
        Transactions(transactionID=1000019, cash=0, ACH=0, CC=29100, CClast4Digits=4877),
        Transactions(transactionID=1000020, cash=0, ACH=35000, CC=0, CClast4Digits=0)
    ]


    Ords = [
        Orders(order_ID=11, order_date='2022-03-14', shipping_cost=0, sales_tax_code='IL', ClientID='A123'),
        Orders(order_ID=12, order_date='2022-04-02', shipping_cost=400, sales_tax_code='OOS', ClientID='D456'),
        Orders(order_ID=13, order_date='2022-02-26', shipping_cost=0, sales_tax_code='IL', ClientID='G789'),
        Orders(order_ID=14, order_date='2022-12-17', shipping_cost=0, sales_tax_code='IL', ClientID='J012'),
        Orders(order_ID=15, order_date='2022-08-08', shipping_cost=0, sales_tax_code='IL', ClientID='O345'),
        Orders(order_ID=16, order_date='2023-06-11', shipping_cost=200, sales_tax_code='WS', ClientID='R678'),
        Orders(order_ID=17, order_date='2023-07-01', shipping_cost=0, sales_tax_code='IL', ClientID='U901'),
        Orders(order_ID=18, order_date='2023-01-15', shipping_cost=200, sales_tax_code='WS', ClientID='X234'),
        Orders(order_ID=19, order_date='2023-06-22', shipping_cost=400, sales_tax_code='OOS', ClientID='A567'),
        Orders(order_ID=20, order_date='2023-09-13', shipping_cost=0, sales_tax_code='IL', ClientID='D890'),
        Orders(order_ID=21, order_date='2022-05-25', shipping_cost=0, sales_tax_code='IL', ClientID='M123'),
        Orders(order_ID=22, order_date='2022-07-12', shipping_cost=300, sales_tax_code='OOS', ClientID='L456'),
        Orders(order_ID=23, order_date='2022-09-03', shipping_cost=0, sales_tax_code='IL', ClientID='P789'),
        Orders(order_ID=24, order_date='2022-11-20', shipping_cost=0, sales_tax_code='IL', ClientID='R012'),
        Orders(order_ID=25, order_date='2023-02-28', shipping_cost=0, sales_tax_code='IL', ClientID='S345'),
        Orders(order_ID=26, order_date='2023-04-15', shipping_cost=200, sales_tax_code='WS', ClientID='W678'),
        Orders(order_ID=27, order_date='2023-08-01', shipping_cost=0, sales_tax_code='IL', ClientID='Y901'),
        Orders(order_ID=28, order_date='2023-10-22', shipping_cost=200, sales_tax_code='WS', ClientID='X9020'),
        Orders(order_ID=29, order_date='2023-12-09', shipping_cost=400, sales_tax_code='OOS', ClientID='B500'),
        Orders(order_ID=30, order_date='2024-01-31', shipping_cost=0, sales_tax_code='IL', ClientID='C890')
    ]

    o_Lines = [
        order_Line(lotID=200001, order_ID=11, unit_price=52000.00, item_count=1, line_number=1),
        order_Line(lotID=200020, order_ID=11, unit_price=5000.00, item_count=1, line_number=2),
        order_Line(lotID=200002, order_ID=12, unit_price=55000.00, item_count=1, line_number=1),
        order_Line(lotID=200003, order_ID=13, unit_price=40000.00, item_count=1, line_number=1),
        order_Line(lotID=200004, order_ID=14, unit_price=44500.00, item_count=1, line_number=1),
        order_Line(lotID=200005, order_ID=15, unit_price=24000.00, item_count=1, line_number=1),
        order_Line(lotID=200006, order_ID=16, unit_price=9500.00, item_count=1, line_number=1),
        order_Line(lotID=200007, order_ID=17, unit_price=20000.00, item_count=1, line_number=1),
        order_Line(lotID=200008, order_ID=18, unit_price=1500.00, item_count=1, line_number=1),
        order_Line(lotID=200009, order_ID=19, unit_price=27000.00, item_count=1, line_number=1),
        order_Line(lotID=200010, order_ID=20, unit_price=14500.00, item_count=1, line_number=1),
        order_Line(lotID=200011, order_ID=21, unit_price=52000.00, item_count=1, line_number=1),
        order_Line(lotID=200012, order_ID=22, unit_price=12000.00, item_count=1, line_number=1),
        order_Line(lotID=200013, order_ID=23, unit_price=7900.00, item_count=1, line_number=1),
        order_Line(lotID=200014, order_ID=24, unit_price=10200.00, item_count=1, line_number=1),
        order_Line(lotID=200015, order_ID=25, unit_price=7650.00, item_count=1, line_number=1),
        order_Line(lotID=200016, order_ID=26, unit_price=3000.00, item_count=1, line_number=1),
        order_Line(lotID=200017, order_ID=27, unit_price=2850.00, item_count=1, line_number=1),
        order_Line(lotID=200025, order_ID=28, unit_price=1900.00, item_count=1, line_number=1),
        order_Line(lotID=200029, order_ID=28, unit_price=3400.00, item_count=1, line_number=2),
        order_Line(lotID=200026, order_ID=29, unit_price=700.00, item_count=1, line_number=1),
        order_Line(lotID=200032, order_ID=29, unit_price=3000.00, item_count=1, line_number=2),
        order_Line(lotID=200027, order_ID=29, unit_price=25000.00, item_count=1, line_number=3),
        order_Line(lotID=200031, order_ID=30, unit_price=35000.00, item_count=1, line_number=1)
    ]

    session.add_all(jewelry_inventory + Tx + Ords + o_Lines)
    session.commit()

# Simple Queries
session = Session(engine)  

# #TODO write this code but for SQLAlchemyORM python scripts    
# stmt = (
#     #get jewelry's styleID from each lotID in order_line (meaning it was sold) and return that as # of items sold for that styleID
#     select(jewelry)
#     #get the total amount sold for each styleID by multiplying order_line's components, item_count x unit_price and return as total_sales
    
#     #join jewelry, order line, and orders
#     .join(jewelry.order_Line.orders)
#     #group by styleID
#     .where(lotID)
#     #list in descending order of value for query created attributes, items_sold and total_sales 