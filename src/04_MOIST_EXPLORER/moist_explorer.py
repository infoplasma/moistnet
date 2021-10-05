#!/usr/bin/env python3

print("*** INFO: LOADING PROGRAM, PLEASE BE PATIENT. ***")
 
import npyscreen as nps
from pod_grapher import Pod 
from mbt_grapher import MBTPlot
import config_pod as cfg


class myEntryForm(nps.FormBaseNewWithMenus):
    def create(self):
        self.pager = self.add(nps.Pager, values=["WELCOME TO SOIL EXPLORER", "PREMERE CTRL-X PER INIZIARE. GRAZIE"])
        self.menu = self.new_menu(name='OPTION MENU', shortcut=None)
        self.menu.addItem(text='CONFIGURATOR-PARAMETRI.......', onSelect=self.configurator_parametri, shortcut='1')
        self.menu.addItem(text='SERIEM-TEMPORIS INDAGATOR....', onSelect=self.seriem_temporis, shortcut='2')
        self.menu.addItem(text="CALOR-TABULA INDAGATOR.......", onSelect=self.calor_tabula, shortcut='3')
        self.menu.addItem(text="MOIST-BATTERY-TEMP GRAPHS....", onSelect=self.mbt_grapher, shortcut="4")
        self.menu.addItem(text='EXODUS.......................', onSelect=self.exit_func, shortcut='0')

    def configurator_parametri(self):
        self.parentApp.switchForm("CONFIGURATOR PARAMETRIS")

    def seriem_temporis(self):
        self.parentApp.switchForm("SERIEM TEMPORIS")

    def calor_tabula(self):
        self.parentApp.switchForm("CALOR TABULA")

    def mbt_grapher(self):
        self.parentApp.switchForm("MBT GRAPHER")

    def exit_func(self):
        nps.notify_wait("*** INFO: EXITING PROGRAM: >>> GOODBYE! <<< ***")
        self.parentApp.switchForm(None)

class configuratorForm(nps.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("MAIN")
    
    def create(self):
        self.p = Pod()
        self.pager = self.add(nps.Pager, 
                values=["AVAILABLE PODS: {}".format(str(self.p.POD_LIST))], max_height=3)
        self.pod_select = self.add(nps.TitleMultiSelect, scroll_exit=True, max_height=5, 
                name="SELECT PODS:", values=self.p.POD_LIST)

    def on_ok(self):
        mem = self.parentApp.getForm("CONFIGURATOR PARAMETRIS")
        mem.pod_select.value = [self.pod_select.values[i] for i in self.pod_select.value]
        self.parentApp.switchForm("CONFIGURATOR PARAMETRIS")

class seriemForm(nps.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("MAIN")
    
    def create(self):
        self.p = Pod()
        self.avail_pods = self.add(nps.Pager, 
                values=["AVAILABLE PODS: {}".format(str(self.p.POD_LIST))], max_height=3)
        self.seriem_text = self.add(nps.TitleText, name="POD LIST:", value=str(','.join(str(i) for i in self.p.POD_LIST))) 
        self.days_to_display = self.add(nps.TitleText, 
                name="DAYS NUMBER:", value=str(cfg.DAYS))

    def on_ok(self):
        self.pod_list = list(map(int, self.seriem_text.value.split(',')))
        nps.notify_wait("""
INFO: PROCESSING DATAPOINTS, PLEASE WAIT......
CLOSE WITH UPPER RIGHT 'x' ON GRAPH ONCE DONE.
            """)
        self.p.__init__()
        self.p.display_pod_timeseries(self.pod_list, days=int(self.days_to_display.value))

class calorForm(nps.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("MAIN")
    
    def create(self):
        self.p = Pod()
        self.avail_pods = self.add(nps.Pager, 
                values=["I SUGGEST TO SELECT UP TO 4 PODS MAXIMUM",
                    "AND UP TO A MONTH WORTH OF DATA",
                    "AVAILABLE PODS: {}".format(str(self.p.POD_LIST))], max_height=3)
        self.pod_select = self.add(nps.TitleMultiSelect, scroll_exit=True, max_height=5, 
                name="SELECT PODS:", values=self.p.POD_LIST)
        self.start_date = self.add(nps.TitleDateCombo, name="START DATE:")
        self.end_date = self.add(nps.TitleDateCombo, name="END DATE:")
        
    def on_ok(self):
        nps.notify_wait("""
INFO: PROCESSING DATAPOINTS, PLEASE WAIT......
CLOSE WITH UPPER RIGHT 'x' ON GRAPH ONCE DONE.
            """)
        self.p.__init__()
        self.p.display_pod_heatmap(pod_list=[self.pod_select.values[i] for i in self.pod_select.value], 
                sd=str(self.start_date.value), ed=str(self.end_date.value))
                

class mbtGrapherForm(nps.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("MAIN")

    def create(self):
        self.p = Pod()
        self.avail_pods = self.add(nps.Pager, 
                values=["SELECT BETWEEN 2 AND 4 PODS MAXIMUM", 
                    "AVAILABLE PODS: {}".format(str(self.p.POD_LIST))], max_height=3)
        self.pod_select = self.add(nps.TitleMultiSelect, scroll_exit=True, max_height=5, 
                name="SELECT PODS:", values=self.p.POD_LIST)
        self.start_date = self.add(nps.TitleDateCombo, name="START DATE:")
        self.end_date = self.add(nps.TitleDateCombo, name="END DATE:")

    def on_ok(self):
        nps.notify_wait("""
INFO: PROCESSING DATAPOINTS, PLEASE WAIT...... 
CLOSE WITH UPPER RIGHT 'x' ON GRAPH ONCE DONE.
            """)
        self.p.__init__()
        self.p.plot_mbt(pod_list=[self.pod_select.values[i] for i in self.pod_select.value], 
                sd=str(self.start_date.value), ed=str(self.end_date.value))

class MyApplication(nps.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', myEntryForm, name='SOIL EXPLORER')
        self.addForm('SERIEM TEMPORIS', seriemForm, name="SERIEM TEMPORIS")
        self.addForm('CALOR TABULA', calorForm, name="CALOR TABULA")
        self.addForm("CONFIGURATOR PARAMETRIS", configuratorForm, name="CONFIGURATOR PARAMETRI")
        self.addForm("MBT GRAPHER", mbtGrapherForm, name="MOIST/BATTERY/TEMP GRAPHER")

if __name__ == "__main__":
    MyApplication().run()
    print('*** INFO: PROGRAM ENDED, GOODBYE. ***')
