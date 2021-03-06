﻿#   Copyright (C) 2015 Kevin S. Graer
#
#
# This file is part of PseudoTV Live.
#
# PseudoTV Live is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PseudoTV Live is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PseudoTV Live.  If not, see <http://www.gnu.org/licenses/>.


import os, xbmc, xbmcgui, xbmcaddon, xbmcvfs
from time import sleep

# Plugin Info
ADDON_ID = 'script.pseudotv.live'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
ADDON_ID = REAL_SETTINGS.getAddonInfo('id')
ADDON_NAME = REAL_SETTINGS.getAddonInfo('name')
ADDON_PATH = REAL_SETTINGS.getAddonInfo('path')
ADDON_VERSION = REAL_SETTINGS.getAddonInfo('version')
THUMB = (xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'images')) + '/' + 'icon.png')


# Swap Org/Hub versions if 'Hub Installer' found.
def HubSwap():
    icon = ADDON_PATH + '/icon'
    HUB = xbmc.getCondVisibility('System.HasAddon(plugin.program.addoninstaller)') == 1
    if HUB == True:
        xbmc.log('script.pseudotv.live-Service: HubSwap = Hub Edition')
        if REAL_SETTINGS.getSetting('Hub') == 'false':
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("PseudoTV Live","Hub-Edition Activated", 4000, THUMB) )
            REAL_SETTINGS.setSetting("Hub","true")
    else:
        xbmc.log('script.pseudotv.live-Service: HubSwap = Master')
        if REAL_SETTINGS.getSetting('Hub') == 'true':
            REAL_SETTINGS.setSetting("Hub","false")
    return          

    
def donorCHK():
    DonorPath = (os.path.join(ADDON_PATH, 'resources', 'lib', 'Donor.pyo'))
    DL_DonorPath = (os.path.join(ADDON_PATH, 'resources', 'lib', 'Donor.py'))
    
    if xbmcvfs.exists(DonorPath) or xbmcvfs.exists(DL_DonorPath):
        xbmc.log('script.pseudotv.live-Service: donorCHK = Donor') 
        if xbmcgui.Window(10000).getProperty("Donor") != "true":
            REAL_SETTINGS.setSetting("AT_Donor", "true")
            REAL_SETTINGS.setSetting("COM_Donor", "true")
            REAL_SETTINGS.setSetting("TRL_Donor", "true")
            REAL_SETTINGS.setSetting("CAT_Donor", "true")  
            xbmcgui.Window(10000).setProperty("Donor", "true") 
    else:
        xbmc.log('script.pseudotv.live-Service: donorCHK = FreeUser') 
        if xbmcgui.Window(10000).getProperty("Donor") != "false":
            REAL_SETTINGS.setSetting("AT_Donor", "false")
            REAL_SETTINGS.setSetting("COM_Donor", "false")
            REAL_SETTINGS.setSetting("TRL_Donor", "false")
            REAL_SETTINGS.setSetting("CAT_Donor", "false")
            xbmcgui.Window(10000).setProperty("Donor", "false")
    return
        
        
# execute service functions
def service():
    while not xbmc.abortRequested:
        xbmc.log("script.pseudotv.live-Service: Started")
        
        if xbmcgui.Window(10000).getProperty("PseudoTVRunning") != "true" and not xbmc.getCondVisibility('Window.IsActive(addonsettings)'):
            donorCHK()
            HubSwap()
            
            # if autostart enabled, and first boot. Start PTVL!
            if REAL_SETTINGS.getSetting("Auto_Start") == "true" and xbmcgui.Window(10000).getProperty("Auto_Start_Exit") != "true":
                xbmcgui.Window(10000).setProperty("Auto_Start_Exit", "true")
                autostart()
        else:
            xbmc.log('script.pseudotv.live-Service: Ignored')
                
        xbmc.log('script.pseudotv.live-Service: Idle')
        xbmc.sleep(10000)


def autostart():
    xbmc.log('script.pseudotv.live-Service: autostart')   
    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("AutoStart PseudoTV Live","Service Starting...", 4000, THUMB) )
    AUTOSTART_TIMER = [0,5,10,15,20]#in seconds
    IDLE_TIME = AUTOSTART_TIMER[int(REAL_SETTINGS.getSetting('timer_amount'))] 
    sleep(IDLE_TIME)
    xbmc.executebuiltin('RunScript("' + ADDON_PATH + '/default.py' + '")')
    return
    
service()