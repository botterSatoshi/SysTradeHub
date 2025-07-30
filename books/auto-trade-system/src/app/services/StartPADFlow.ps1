# Power Automate for desktopのフローを実行するPowerShellスクリプト
#   @param [string] $flowName 実行するフロー名
#   @param [bool] $flgExit PAD終了フラグ
#
# 動作確認：バージョン 2.40.157.24023 (インストーラー版)
#

Param(
  [parameter(mandatory=$true)][string]$flowName,
  [bool]$flgExit = $false
)

#Power Automate for desktop起動
Start-Process -FilePath "ms-powerautomate://"

#UI Automation
Add-Type -AssemblyName "UIAutomationClient"
Add-Type -AssemblyName "UIAutomationTypes"
$uiAuto = [System.Windows.Automation.AutomationElement]
$pcdn = [System.Windows.Automation.PropertyCondition]
$acdn = [System.Windows.Automation.AndCondition]
$tree = [System.Windows.Automation.TreeScope]
$iptn = [System.Windows.Automation.InvokePattern]::Pattern
$wptn = [System.Windows.Automation.WindowPattern]::Pattern
$icptn = [System.Windows.Automation.ItemContainerPattern]::Pattern
$siptn = [System.Windows.Automation.ScrollItemPattern]::Pattern
$selptn = [System.Windows.Automation.SelectionItemPattern]::Pattern
$root = $uiAuto::RootElement

#Power Automate for desktopウィンドウ取得
$cndPadWindowId = New-Object $pcdn($uiAuto::AutomationIdProperty, "ConsoleMainWindow")
$cndPadWindowClassName = New-Object $pcdn($uiAuto::ClassNameProperty, "WinAutomationWindow")
$cndPadWindow = New-Object $acdn($cndPadWindowId, $cndPadWindowClassName)
do{
  Start-Sleep -m 200
  $elmPadWindow = $root.FindFirst($tree::Children, $cndPadWindow)
}while($elmPadWindow -eq $null)

#タブ取得
$cndTab = New-Object $pcdn($uiAuto::AutomationIdProperty, "ProcessesTabControl")
$elmTab = $elmPadWindow.FindFirst($tree::Subtree, $cndTab)

#タブ項目取得・選択
if($elmTab -ne $null){
  $cndTabItem = New-Object $pcdn($uiAuto::AutomationIdProperty, "MyFlowsTab")
  $elmTabItem = $elmTab.FindFirst($tree::Children, $cndTabItem)
  if($elmTabItem -ne $null){
    $selTabItem = $elmTabItem.GetCurrentPattern($selptn)
    $selTabItem.Select()
  }
}

#データグリッド取得
if($elmPadWindow -ne $null){
  $cndDataGrid = New-Object $pcdn($uiAuto::AutomationIdProperty, "MyFlowsListGrid")
  $elmDataGrid = $elmPadWindow.FindFirst($tree::Subtree, $cndDataGrid)
}

#データ項目取得・選択
if($elmDataGrid -ne $null){
  $icDataGrid = $elmDataGrid.GetCurrentPattern($icptn)
  $elmDataItem = $icDataGrid.FindItemByProperty($null, $uiAuto::NameProperty, $flowName)
  if($elmDataItem -ne $null){
    $siDataItem = $elmDataItem.GetCurrentPattern($siptn)
    $siDataItem.ScrollIntoView()
    $selDataItem = $elmDataItem.GetCurrentPattern($selptn)
    $selDataItem.Select()
  }
}

#実行ボタン取得・押下
if($elmDataItem -ne $null){
  $cndStartButton = New-Object $pcdn($uiAuto::AutomationIdProperty, "StartFlowButton")
  $elmStartButton = $elmDataItem.FindFirst($tree::Subtree, $cndStartButton)
  if($elmStartButton -ne $null){
    $ivkStartButton = $elmStartButton.GetCurrentPattern($iptn)
    $ivkStartButton.Invoke()
  }
}

if($flgExit){
  #フロー終了待ち
  if($elmStartButton -ne $null){
    do{
      Start-Sleep -m 800
    }while($elmStartButton.GetCurrentPropertyValue($uiAuto::IsEnabledProperty) -eq $false)
  }

  #Power Automate for desktop終了
  $winPadWindow = $elmPadWindow.GetCurrentPattern($wptn)
  $winPadWindow.Close()
}