# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		
		self.m_scrolledWindow2 = wx.ScrolledWindow( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow2.SetScrollRate( 5, 5 )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_richText2 = wx.richtext.RichTextCtrl( self.m_scrolledWindow2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer9.Add( self.m_richText2, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_scrolledWindow2.SetSizer( bSizer9 )
		self.m_scrolledWindow2.Layout()
		bSizer9.Fit( self.m_scrolledWindow2 )
		self.m_splitter2.Initialize( self.m_scrolledWindow2 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		self.m_treeCtrl4 = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		self.m_treeCtrl4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Courier New" ) )
		
		bSizer1.Add( self.m_treeCtrl4, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.m_treeCtrl4.Bind( wx.EVT_TREE_SEL_CHANGED, self.m_treeCtrl4OnTreeSelChanged )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_treeCtrl4OnTreeSelChanged( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 245 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

