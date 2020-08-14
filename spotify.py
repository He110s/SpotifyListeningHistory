import json
import os

def read(data, count):
    jsonFile = open(input("Json filename (with '.json'): "), "r", encoding="utf-8")
    newSet = json.load(jsonFile)
    jsonFile.close()

    for song in newSet:
        data[count] =    {  
                                    "artistName" : song["artistName"],
                                    "trackName" : song["trackName"],
                                    "endTime" : song["endTime"],
                                    "msPlayed" : song["msPlayed"]
                                    }
        count += 1
    return data, count

def readFromFolder(data):
    count = 0
    for root, dirs, files in os.walk("."):
        #print(root)
        if root == "./jsonDirectory":
            print("\nReading from files:")
            for filename in files:
                print("  "+filename)
                jsonFile = open(root+"/"+filename, "r", encoding="utf-8")
                newSet = json.load(jsonFile)
                jsonFile.close()

                for song in newSet:
                    data[count] =    {  
                                                "artistName" : song["artistName"],
                                                "trackName" : song["trackName"],
                                                "endTime" : song["endTime"],
                                                "msPlayed" : song["msPlayed"]
                                                }
                    count += 1
    print("")
    return data

def filterDuplicates(data):
    position = set()
    duplicates = 0
    print("\n Looking for Duplicates!")
    for e1 in range(0,len(data)):
        for e2 in range(e1+1,len(data)):
            if data[e1]["artistName"] == data[e2]["artistName"] and data[e1]["trackName"] == data[e2]["trackName"] and data[e1]["msPlayed"] == data[e2]["msPlayed"] and data[e1]["endTime"] == data[e2]["endTime"]:
                position.add(e2)
                duplicates += 1
    if duplicates > 0:
        print(duplicates, "Duplicates FOUND!")
        print(" Deleting Duplicates!")
    else:
        print(" NO Duplicates FOUND!")
    print("")
    for a in position:
        del data[a]
        print(a)
    return data


def full(data):
    newSet = {}
    for n in data:
        if data[n]["artistName"] in newSet:
            newSet[data[n]["artistName"]]["count"] += 1
            if data[n]["trackName"] in newSet[data[n]["artistName"]]["track"]:
                newSet[data[n]["artistName"]]["track"][data[n]["trackName"]] += 1
            else:
                newSet[data[n]["artistName"]]["track"][data[n]["trackName"]] = 1
        else:
            newSet[data[n]["artistName"]] = {}
            newSet[data[n]["artistName"]]["count"] = 1
            newSet[data[n]["artistName"]]["track"] = {}
            newSet[data[n]["artistName"]]["track"][data[n]["trackName"]] = 1

    return newSet
    #show(newSet)
    #sort_data = sorted(newSet[], key=lambda x: x[1])
    #for i in data:
    #    print(i,data[i])


def interval(data):
    show(data, {})

def show(data, order):
    sortedOrder = sorted(order.items(), key=lambda item: item[1])
    print("")
    for artist in sortedOrder:
        print(data[artist[0]]["count"], artist[0])
        sortedTracks = sorted(data[artist[0]]["track"].items(), key=lambda item: item[1], reverse=True)
        for track in sortedTracks:
            print("   ",track[1],track[0])
    print("")
        

def reWrite(data):
    order = {}
    for number in data:
        order[number] = data[number]["count"]
    return order

def exportJSON(data, order):
    sortedOrder = sorted(order.items(), key=lambda item: item[1], reverse=True)
    newSet = {}

    for artist in sortedOrder:
        newSet[artist[0]] = data[artist[0]]
        sortedTracks = sorted(newSet[artist[0]]["track"].items(), key=lambda item: item[1], reverse=True)
        newTrack = {}
        for value in sortedTracks:
            newTrack[value[0]] = value[1]
        newSet[artist[0]]["track"] = newTrack

    f = open("output.json", "w", encoding="utf-8")
    json.dump(newSet, f, indent=4, ensure_ascii=False)
    f.close()

def exportTXT(data, order):
    f = open("output.txt", "w", encoding="utf-8")

    sortedOrder = sorted(order.items(), key=lambda item: item[1], reverse=True)

    for artist in sortedOrder:
        f.write(str(data[artist[0]]["count"])+" "+artist[0]+"\n")
        sortedTracks = sorted(data[artist[0]]["track"].items(), key=lambda item: item[1], reverse=True)
        for track in sortedTracks:
            f.write("    "+str(track[1])+" "+track[0]+"\n")

    f.close()

def tresholdFilter(data):
    treshold = int(input("\n Time in miliseconds (ms): "))
    tbDeleted = set()
    for song in data:
        if data[song]["msPlayed"] < treshold:
            tbDeleted.add(song)

    for num in tbDeleted:
        del data[num]

    print(" Removed Total:",len(tbDeleted))
    print("")

    return data

def menu(data, count):
    print("Total Lines: " + str(len(data)))
    print("(1.) Add json file.")
    print("(2.) Remove duplicates.")
    print("(3.) Show data from all.")
    print("(4.) Show data from interval. (NOT WRITTEN!!!)")
    print("(5.) Export Json.")
    print("(6.) Export txt.")
    print("(7.) Set Minimum listening time (ms).")
    print("(8.) Folder Read.")
    
    choice = int(input())

    if choice == 1:
        data, count = read(data, count)
    elif choice == 2:
        data = filterDuplicates(data)
    elif choice == 3:
        show(full(data), reWrite(full(data)))
    elif choice == 4:
        interval(data)
    elif choice == 5:
        exportJSON(full(data), reWrite(full(data)))
    elif choice == 6:
        exportTXT(full(data), reWrite(full(data)))
    elif choice == 7:
        data = tresholdFilter(data)
    elif choice == 8:
        data = readFromFolder(data)
    else:
        print("\n !!! ERROR !!!")
        print(" Choice Out of the Range.\n")
    menu(data, count)

menu({}, 0)