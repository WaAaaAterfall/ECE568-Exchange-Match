#!/usr/bin/env python3
from parse import *
from match_price import *
from addTodb import *
from server import *
import time

'''
This file is the test for unit testing, you could directly run this, without the server start,
By adjusting the sub-function in the main, you could directly see the update in the database.
For server test please go to testing directory to run the client_test.py there.
'''


'''
@func: This is the unit test and combination test for order matching and adding to database function
'''


def testMatch():
    addAccount(1, 10000000)
    addAccount(2, 10000000)
    addAccount(3, 10000000)
    addAccount(4, 10000000)
    addAccount(5, 10000000)
    addAccount(6, 10000000)
    addAccount(7, 10000000)
    addPosition(1, 'X', 50000000)
    addPosition(2, 'X', 50000000)
    addPosition(3, 'X', 50000000)
    addPosition(4, 'X', 50000000)
    addPosition(5, 'X', 50000000)
    addPosition(6, 'X', 500000000)
    addPosition(7, 'X', 50000000)

    addTranscation(1, 'X', 300, 125)
    # execute_order(1)
    addTranscation(2, 'X', -100, 130)
    addTranscation(3, 'X', 200, 127)
    # execute_order(3)
    addTranscation(4, 'X', -500, 128)
    addTranscation(5, 'X', -200, 140)
    time.sleep(1)
    addTranscation(6, 'X', 400, 125)
    time.sleep(1)
    addTranscation(7, 'X', -400, 120)


def testMatch1():
    session = createEngine()
    testMatch()
    execute_order(7, 'X', -400, 120, 7)
    session.close()


def testParseMatch():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print("----Test 1----")
    xmlString = "<create><account id=\"1\" balance=\"100000\"/><account id=\"2\" balance=\"100000\"/><account id=\"3\" balance=\"100000\"/><account id=\"4\" balance=\"100000\"/><account id=\"5\" balance=\"100000\"/><account id=\"6\" balance=\"100000\"/><account id=\"7\" balance=\"100000\"/>"
    xmlString += "<symbol sym=\"X\"><account id=\"1\">500</account><account id=\"2\">500</account><account id=\"3\">500</account><account id=\"4\">500</account><account id=\"5\">500</account><account id=\"6\">500</account><account id=\"7\">500</account></symbol></create>"
    xmlString1 = "<transactions id=\"1\"><order sym=\"X\" amount=\"300\" limit=\"125\"/></transactions>"
    xmlString2 = "<transactions id=\"2\"><order sym=\"X\" amount=\"-100\" limit=\"130\"/></transactions>"
    xmlString3 = "<transactions id=\"3\"><order sym=\"X\" amount=\"200\" limit=\"127\"/></transactions>"
    xmlString4 = "<transactions id=\"4\"><order sym=\"X\" amount=\"-500\" limit=\"128\"/></transactions>"
    xmlString5 = "<transactions id=\"5\"><order sym=\"X\" amount=\"-200\" limit=\"140\"/></transactions>"
    xmlString6 = "<transactions id=\"6\"><order sym=\"X\" amount=\"400\" limit=\"125\"/></transactions>"
    xmlString7 = "<transactions id=\"7\"><order sym=\"X\" amount=\"-400\" limit=\"124\"/></transactions>"

    print(parsing_XML(xmlString))
    print(parsing_XML(xmlString1))
    print(parsing_XML(xmlString2))
    print(parsing_XML(xmlString3))
    print(parsing_XML(xmlString4))
    print(parsing_XML(xmlString5))
    print(parsing_XML(xmlString6))
    print("Before matching:")
    printAccountPosition(engine)
    printOrderStatus(engine)
    print("New order:")
    print(xmlString7)
    print(parsing_XML(xmlString7))
    print("After matching:")
    printAccountPosition(engine)
    printOrderStatus(engine)
    session.close()


'''
@func: This is the unit test and combination test for XML parser and adding to databse functions
'''


def testParse():
    session = createEngine()
    print("----Test 1 Failed: Account exist is 0, balance is negative, account does not exist----")
    xmlString = "<create><account id=\"0\" balance=\"50000\"/><account id=\"2\" balance=\"-100000\"/><symbol sym=\"TESLA\"><account id=\"1\">200</account></symbol></create>"
    print("Request:")
    print(xmlString)
    print("Response:")
    print(parsing_XML(xmlString))
    print("")
    print("----Test 2 Failed: Query number and cancel number does not exist----")
    xmlString2 = "<create><account id=\"1\" balance=\"50000\"/><symbol sym=\"TESLA\"><account id=\"1\">500</account></symbol></create>"
    xmlString3 = "<transactions id=\"1\"><query id=\"1\"/><cancel id=\"1\"/></transactions>"
    print("Request:")
    print(xmlString2)
    print(xmlString3)
    print("Response:")
    print(parsing_XML(xmlString2))
    print(parsing_XML(xmlString3))
    print("")
    print("----Test 3 Failed: Trasaciton account id doesn't exsit, transcation doesn't belong to account----")
    xmlString8 = "<transactions id=\"1000\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/><query id=\"1\"/><cancel id=\"1\"/></transactions>"
    xmlString7 = "<transactions id=\"1\"><cancel id=\"1\"/><query id=\"1\"/></transactions>"
    print("Request:")
    print(xmlString8)
    print(xmlString7)
    print("Response:")
    print(parsing_XML(xmlString8))
    print(parsing_XML(xmlString7))
    print("")
    print("----Test 4 Success: Open a order, query it, then delete it and query again----")
    xmlString4 = "<create><account id=\"2\" balance=\"50000\"/><symbol sym=\"TB\"><account id=\"2\">500</account></symbol></create>"
    xmlString5 = "<transactions id=\"2\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/><order sym=\"TB\" amount=\"-100\" limit=\"120\"/><query id=\"1\"/><query id=\"2\"/></transactions>"
    xmlString6 = "<transactions id=\"2\"><query id=\"1\"/></transactions>"
    xmlString9 = "<transactions id=\"2\"><cancel id=\"1\"/><cancel id=\"2\"/><query id=\"1\"/><query id=\"2\"/></transactions>"
    print("Request:")
    print(xmlString4)
    print(xmlString5)
    # print(xmlString6)
    print(xmlString9)
    print("Response:")
    print(parsing_XML(xmlString4))
    print(parsing_XML(xmlString5))
    time.sleep(1)
    # addStatus(  1, 'executed', 50, 250, getCurrentTime())
    # print(parsing_XML(  xmlString6)
    time.sleep(1)
    print(parsing_XML(xmlString9))
    session.close()


'''
@func: This is the unit test for adding to database function
'''


def testAdd():
    session = createEngine()
    try:
        print("----Test 1 Failed: Account exist----")
        addAccount(1, 100000)
        addAccount(1, 200)
    except Exception as e:
        print(e)

    print("")
    try:
        print("----Test 2 Failed: Balance not sufficient----")
        addPosition(1, 'T5asdf', 200)
        addPosition(1, 'T5asdf', 300)
        addTranscation(1, 'T5asdf', 400, 125)
        addTranscation(1, 'T5asdf', 400, 125)
        addTranscation(1, 'T5asdf', 200, 125)

    except Exception as e:
        print(e)

    print("")
    try:
        print("----Test 3 Failed: Amount not sufficient----")
        addAccount(2, 200)
        addPosition(2, 'T5asdf', 200)
        addTranscation(2, 'T5asdf', -400, 125)
    except Exception as e:
        print(e)
    try:
        addPosition(1, 'S&P', 300)
        addPosition(1, 'BTC', 100)
        addStatus(session, 1, 'executed', 100, 100, getCurrentTime())
    except Exception as e:
        print(e)
    session.close()


def testCancel():
    xmlString4 = "<create><account id=\"2\" balance=\"50000\"/><symbol sym=\"TB\"><account id=\"2\">500</account></symbol></create>"
    xmlString5 = "<transactions id=\"2\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/><order sym=\"TB\" amount=\"-100\" limit=\"120\"/><query id=\"1\"/><query id=\"2\"/></transactions>"
    xmlString6 = "<transactions id=\"2\"><cancel id=\"1\"/><cancel id=\"2\"/><query id=\"1\"/></transactions>"
    xmlString9 = "<transactions id=\"2\"><cancel id=\"1\"/><cancel id=\"2\"/><query id=\"1\"/><query id=\"2\"/></transactions>"
    print("Request:")
    print(xmlString4)
    print(xmlString5)
    print(xmlString6)
    print(xmlString9)
    print("Response:")
    print(parsing_XML(xmlString4))
    print(parsing_XML(xmlString5))
    print(parsing_XML(xmlString6))
    print(parsing_XML(xmlString9))


def testSocket():
    serverLitsen()


def main():
    '''
    Some of the tests cannot be run together, such as testParse()+testAdd()
    Please try them seperately appreciate!
    '''
    # testMatch1()
    # testTrans()
    testParseMatch()
    testParse()
    # testAdd()
    # testCancel()


if __name__ == '__main__':
    main()
