from  chimera.extension import EMO, manager

# -----------------------------------------------------------------------------
#
class ModelZ_Dialog_EMO ( EMO ):

  def name(self):
    return 'ECSU Label'
  def description(self):
    return self.categoryDescriptions()['Utilities']
  def categories(self):
    return self.categoryDescriptions().keys()
  def categoryDescriptions(self):
    # since we want to use specialized descriptions for certain categories...
    return {
      'Utilities': 'Detect anomalous residues from Cryo-EM proteins',
    }
  def icon(self):
    return None #self.path('volseg.png')
  def activate(self):
    # self.module('volumedialog').show_volume_dialog()
    d = self.module('gui').main()
    return None

# -----------------------------------------------------------------------------
# Register dialogs and menu entry.
#
manager.registerExtension ( ModelZ_Dialog_EMO ( __file__ ) )

