#!/usr/bin/env python
import simplejson as json
import os
import copy
import sys

path = sys.argv[1]

if len(sys.argv) < 2:
    print "Missing parameters"
    sys.exit()

visibochromeextensionBasePath = path
productNames = ['FreshStart', 'FriendsMural', 'IncredibleStartPage', 'TabJump', 'TooManyTabs', 'TwitterWatch']

# langList should not include en
langList = ['ja', 'ru', 'es', 'it', 'pt', 'pt_BR', 'de', 'fr', 'zh_TW', 'cs', 'sk']

# loop each folder
for productName in productNames:
    # header to be printed on the table
    print "==" + productName + "=="
    print "|| *Language* || *Words to be translated* ||"
    if os.path.exists(visibochromeextensionBasePath + '/' + productName + '/en/messages.json') == False:
        print 'no en locale file exists!'
        print ""
        continue
    f = open(visibochromeextensionBasePath + '/' + productName + '/en/messages.json', 'r')
    jsonContent = f.read()
    f.close()
    enStringList = []
    enLangString = json.loads(jsonContent)
    for x in enLangString.iteritems():
        # generate the name list
        enStringList.append(x[0])
    
    for x in langList:
        # no such lang folder, then skip
        if os.path.exists(visibochromeextensionBasePath + '/' + productName + '/' + x ) == False:
            continue
        path = visibochromeextensionBasePath + '/' + productName + '/' + x + '/messages.json'
        notTranslatedCount = 0
        if (os.path.exists(path)):
            f = open(path, 'r')
            jsonContent = f.read()
            f.close()

            langString = json.loads(jsonContent)
            stringList = []

            for y in langString.iteritems():
                stringList.append(y[0])

            newLangString = {}
            for y in enLangString.iteritems():
                if ('remark' in y[1]) and (y[1]['remark'] == 'NO NEED TO TRANSLATE'):
                    newLangString[y[0]] = copy.deepcopy(enLangString[y[0]])
                else:
                    if y[0] in langString:
                        if langString[y[0]]['message'] == y[1]['message']:
                            newLangString[y[0]] = copy.deepcopy(y[1])
                            newLangString[y[0]]['remark'] = 'NEED TRANSLATION'
                            notTranslatedCount += 1
                        else:
                            newLangString[y[0]] = copy.deepcopy(langString[y[0]])
                            if 'remark' in newLangString[y[0]]:
                                del newLangString[y[0]]['remark']
                    else:
                        newLangString[y[0]] = copy.deepcopy(y[1])
                        newLangString[y[0]]['remark'] = 'NEED TRANSLATION'
                        notTranslatedCount += 1
        else:
            newLangString = copy.deepcopy(enLangString)
            for y in newLangString:
                if (('remark' in newLangString[y]) and (newLangString[y]['remark'] != "NO NEED TO TRANSLATE") or ('remark' not in newLangString[y])):
                    newLangString[y]['remark'] = "NEED TRANSLATION"
                    notTranslatedCount += 1
                    
        print "|| " + x + " || " + str(notTranslatedCount) + "/" + str(len(enStringList)) + " ||"
        s = json.dumps(newLangString, sort_keys = True, indent = 4 * ' ', ensure_ascii = False)
        f = open(visibochromeextensionBasePath + '/' + productName + '/' + x + '/messages.json', 'w')
        f.write(s.encode('utf-8'))
        f.close()
    print ""
