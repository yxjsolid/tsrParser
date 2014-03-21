__author__ = 'xyang'
import wx
import wx.lib.agw.customtreectrl as CT
import wx.richtext
import re


fileName = "techSupport_0F5954_3-19.wri"
#fileName = "11.txt"
outFileName = 'tsrout.xml'
outFileName1 = 'tsrout1.xml'

#System : Status_START
#System : Status_END

class myConfiguration():
    parseOutRangedCat = False
    xmlValidate = True


class Tsr2Xml():
    def __init__(self, inFileName, outFileName):
        self.inFd = open(inFileName, "rU")
        self.outFd = open(outFileName, 'w')
        self.pattern = '^#([\w\s\S]*) : ([\w\s\S]*)_(START|END)'
        self.pattern2 = '^#(Debug) ([\w\s\S]*)_(START|END)'
        self.lastLabel = ""
        self.doConvert()

    def doConvert(self):
        p1 = re.compile(self.pattern)
        p2 = re.compile(self.pattern2)
        while True:
            lineStr = self.inFd.readline()

            if lineStr == "":
                break

            m = p1.match(lineStr)
            if not m:
                m = p2.match(lineStr)

            if m:
                g = m.groups()
                print g
                if 1:
                    if self.lastLabel != g[0]:

                        if self.lastLabel != "":
                            self.outFd.write("</%s>\n" % self.lastLabel)
                        self.outFd.write("<%s>\n" % g[0])
                        self.tagOpen = True
                        self.lastLabel = g[0]
                else:
                    pass

                if g[2] == "START":
                    self.outFd.write("<%s>\n" % g[1])
                else:
                    self.outFd.write("</%s>\n"% g[1])
            else:
                self.outFd.write(lineStr)
                pass

        self.outFd.write("</%s>\n" % self.lastLabel)
        self.outFd.flush()
        self.outFd.close()


class TsrCategory2Xml():
    def __init__(self, inFileName, outFileName):
        self.inFd = open(inFileName, "rU")
        self.outFd = open(outFileName, 'w')
        self.parser = None
        self.inOffset = 0
        pass

    def setParser(self, parser):
        self.parser = parser


    def xmlSectionOutput(self, secItem):
        offStart = secItem.offStart
        offEnd = secItem.offEnd

        if self.inOffset < offStart:
            self.xmlCopyData(self.inOffset, offStart)

        tag = self.xmlGenTag(secItem.label)

        self.xmlWriteString("<%s>\n\n"%tag)
        self.xmlCopyData(offStart, offEnd)
        self.xmlWriteString("</%s>\n\n"%tag)
        self.inOffset = offEnd


    def xmlGenTag(self, label):

        if not myConfiguration.xmlValidate:
            return label
        else:
            if label[0].isdigit():
                label = "_"+label

            return label.replace("&", "and").replace(" ", "_").replace("/","_")

    def xmlOutput(self):
        tsrCategory = self.parser.tsrCategory

        xmlDesc = r'<?xml version="1.0" encoding="ISO-8859-1"?>'

        self.xmlWriteString(xmlDesc+"\n")
        self.xmlWriteString("<root>\n")
        for cat in tsrCategory:
            offStart = cat.offStart
            offEnd = cat.offEnd
            if self.inOffset < offStart:
                self.xmlCopyData(self.inOffset, offStart)
                self.inOffset = offStart

            tag = self.xmlGenTag(cat.label)

            self.xmlWriteString("<%s>\n\n"%tag)
            for secItem in cat.section:
                self.xmlSectionOutput(secItem)
            self.xmlWriteString("</%s>\n\n"%tag)

        self.xmlWriteString("</root>\n")
        #self.outFd.close()

    def xmlWriteString(self, inStr):
        self.outFd.write(inStr)
        self.outFd.flush()

    def xmlCopyData(self, start, end):
        self.inFd.seek(start)
        strTmp = self.inFd.read(end - start)


        if  myConfiguration.xmlValidate:
            strTmp = strTmp.replace("&", "&amp;")
            strTmp = strTmp.replace("<", "&lt;")
            strTmp = strTmp.replace(">", "&gt;")
            strTmp = strTmp.replace("\n", "\r\n")


        self.outFd.write(strTmp)

        self.inOffset = end

        # while True:
        #     offStart = fd.tell()
        #     lineStr = fd.readline()
        #     offEnd = fd.tell()
        #     if lineStr == '':
        #         break

        pass





class TsrElemNodeEntry():
    def __init__(self, label, filePosInfo):
        self.label = label
        self.offStart = 0
        self.offEnd = 0
        self.lineStart = 0
        self.lineEnd = 0
        self.entryTagOpen(filePosInfo)

    def initEntry(self ):
        pass

    def updateEntry(self):
        pass

    def entryTagOpen(self, filePosInfo):
        offStart, offEnd, iLine = filePosInfo
        self.offStart = offStart
        self.lineStart = iLine

    def entryTagClose(self, filePosInfo):
        offStart, offEnd, iLine = filePosInfo
        self.offEnd = offEnd
        self.lineEnd = iLine

    def isEntryMatch(self, label):
        if self.label == label:
            return True
        return False

    def dumpEntryInfo(self, level):
        pad = "".join(['    ' for i in range(level)])
        outFormat = "%-*s  from %d to %d "
        print pad, outFormat%(50-len(pad), self.label, self.lineStart + 1 , self.lineEnd + 1)


class SectionEntry(TsrElemNodeEntry):
    def __init__(self, label, filePosInfo):
        TsrElemNodeEntry.__init__(self, label, filePosInfo)


class CategoryEntry(TsrElemNodeEntry):
    def __init__(self, label, filePosInfo):
        TsrElemNodeEntry.__init__(self, label,filePosInfo)
        self.section = []

    def updateSectionEntry(self, catInfo, filePosInfo):
        catStr, sectionStr, isStart = catInfo

        isTagOpen = False

        if isStart:
            currentSection = SectionEntry(sectionStr, filePosInfo)
            self.section.append(currentSection)
            isTagOpen = True
        else:
            currentSection = self.section[-1]
            if not currentSection.isEntryMatch(sectionStr):
                print "addSectionEntry  error!!!!"

            currentSection.entryTagClose(filePosInfo)
            self.entryTagClose(filePosInfo)

        return isTagOpen

    def dumpCategoryEntry(self):
        self.dumpEntryInfo(0)

        for secItem in self.section:
            secItem.dumpEntryInfo(1)


class TsrFileParser():
    def __init__(self, fileName):
        self.tsrCategory = []
        self.outRangeCat = None
        self.isTagOpen = False
        self.parseTsrFile(fileName)


    def updateCategoryEntry(self, catInfo, filePosInfo):

        currentCat = None
        if len(self.tsrCategory):
            currentCat = self.tsrCategory[-1]

        if currentCat:
            if not currentCat.isEntryMatch(catInfo[0]):
                currentCat = CategoryEntry(catInfo[0], filePosInfo)
                self.tsrCategory.append(currentCat)

        else:
            currentCat = CategoryEntry(catInfo[0], filePosInfo)
            self.tsrCategory.append(currentCat)

        isTagOpen = currentCat.updateSectionEntry(catInfo, filePosInfo)
        return isTagOpen

    def getCategory(self, lineStr, offStart, offEnd, iLine):
        #System : Status_START
        #System : Status_END"
        #Debug Information_START
        #Debug Information_END
        #WAN Acceleration : Bandwidth Optimization Device_START
        #WAN Acceleration : Bandwidth Optimization Device_END
        #DPI-SSL : Server SSL_START
        #DPI-SSL : Server SSL_END

        pattern = '^#([\w\s\S]*) : ([\w\s\S]*)_(START|END)'
        pattern2 = '^#(Debug) ([\w\s\S]*)_(START|END)'

        filePosInfo = [offStart, offEnd, iLine]
        findMatch = False

        if lineStr[0] is '#':
            p = re.compile(pattern)
            m = p.match(lineStr)

            # special case for debug format not correct
            if not m:
                p = re.compile(pattern2)
                m = p.match(lineStr)

            if m:
                g = m.groups()
                if g[-1] == 'START':
                    catInfo = [g[0], g[1], 1]
                else:
                    catInfo = [g[0], g[1], 0]

                findMatch = True

                if self.outRangeCat:
                    self.outRangeCat.entryTagClose([filePosInfo[0], filePosInfo[0], filePosInfo[2]-1])
                    self.outRangeCat = None

                self.isTagOpen = self.updateCategoryEntry(catInfo, filePosInfo)

        if not self.isTagOpen and not findMatch:

            if myConfiguration.parseOutRangedCat:
                return

            # if lineStr.strip() != "":
            #
            #     if not self.outRangeCat:
            #         self.outRangeCat =  CategoryEntry("unknown", filePosInfo)
            #         self.tsrCategory.append(self.outRangeCat)
            #
            #     print iLine, lineStr.strip()
            #self.index += 1

    def parseTsrFile(self, fileName):
        fd = open(fileName, "rU")
        self.fd = fd
        iLine = 0
        while True:
            offStart = fd.tell()
            lineStr = fd.readline()
            offEnd = fd.tell()
            if lineStr == '':
                break

            self.getCategory(lineStr, offStart, offEnd, iLine)
            iLine += 1

        #fd.close()

    def dumpCategory(self):
        for cat in self.tsrCategory:
            cat.dumpCategoryEntry()

    def writeCategoryInfo(self, cat, writer):
        fd = self.fd
        offStart = cat.offStart
        offEnd = cat.offEnd
        fd.seek(offStart)
        totalSize = offEnd - offStart
        line = fd.read(totalSize)
        writer.doWrite(line)


class CustomTreeCtrlDemo(wx.Panel):

    def __init__(self, parent, parser):
        wx.Panel.__init__(self, parent)

        self.parser = parser

        splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        # Create the CustomTreeCtrl, using a derived class defined below
        self.tree = wx.TreeCtrl(splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        self.richText = wx.richtext.RichTextCtrl(splitter, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS)
        self.richText.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Courier New"))

        splitter.SplitVertically(self.tree, self.richText, 300)
        splitter.SetMinimumPaneSize(100)

        sizer = wx.BoxSizer()
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelChanged)
        self.buildTreeView()

    def onTreeSelChanged( self, event ):
            root = self.tree.GetRootItem()
            item = event.GetItem()

            if item != root:
                cat = self.tree.GetItemPyData(item)

                self.richText.Clear()
                self.parser.writeCategoryInfo(cat, self)

            event.Skip()

    def doWrite(self, data):
        print "doWrite"
        self.richText.WriteText(data)

    def buildTreeView(self):
        root = self.tree.AddRoot("test")
        for catItem in self.parser.tsrCategory:
            catNode = self.tree.AppendItem(root, catItem.label)
            self.tree.SetPyData(catNode, catItem)

            for secItem in catItem.section:
                sectionNode = self.tree.AppendItem(catNode, secItem.label)
                self.tree.SetPyData(sectionNode, secItem)

if __name__ == '__main__':
    parser = TsrFileParser(fileName)
    parser.dumpCategory()

    fac = TsrCategory2Xml(fileName, outFileName)
    fac.setParser(parser)
    fac.xmlOutput()


    convert = Tsr2Xml(fileName, outFileName1)



    app = wx.App(0)
    frame = wx.Frame(None)
    panel = CustomTreeCtrlDemo(frame, parser)
    frame.Show()
    app.MainLoop()


