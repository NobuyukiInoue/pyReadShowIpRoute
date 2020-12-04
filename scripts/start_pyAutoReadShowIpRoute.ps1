##----------------------------------------------------------------------------##
## Main function.
##----------------------------------------------------------------------------##
function Main()
{
    Add-Type -Assembly System.Windows.Forms

    $CMD1 = "./dist/pyAutoReadShowIpRoute.exe"
    $CMD2 = "./pyAutoReadShowIpRoute.exe"
    $OPTION = "--logfile_pattern *.log"

    if (Test-Path $CMD1) {
        $CMD = $CMD1
    }
    elseif (Test-Path $CMD2) {
        $CMD = $CMD2
    }
    else {
        $CMD = SelectFile "pyAutoReadShowIpRoute.exeを選択してください。"
    }

    if ($NULL -eq $CMD) {
        return
    }

    $LOG_DIR = SelectFolder("logファイル群が格納されているディレクトリを選択してください。")
    if ($NULL -eq $LOG_DIR) {
        return
    }

    $DEST_DIR = SelectFolder("RouteTableの出力先ディレクトリを選択してください。")
    if ($NULL -eq $DEST_DIR) {
        return
    }

    $CMDLINE = "$CMD $LOG_DIR $DEST_DIR $OPTION"

    Add-Type -Assembly System.Windows.Forms
    $res = [System.Windows.Forms.MessageBox]::Show("$CMDLINE`n`n実行しますか？", "実行確認", "YesNo", "Question")
    if ($res -eq "Yes") {
        Invoke-Expression $CMDLINE
    }
}

##----------------------------------------------------------------------------##
## Display Select EXE File Dialog.
##----------------------------------------------------------------------------##
function SelectFile([string]$message)
{
    [void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Filter = "EXEファイル(*.EXE)|*.EXE;"
    $dialog.InitialDirectory = Get-Location
    $dialog.Title = $message

    if($dialog.ShowDialog() -eq "OK") {
        return $dialog.FileName
    }
    else {
        return $NULL
    }
}

##----------------------------------------------------------------------------##
## Display Select Folder Dialog.
##----------------------------------------------------------------------------##
function SelectFolder([string]$message)
{
    [void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.SelectedPath = Get-Location
    $dialog.Description = $message

    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        return $dialog.SelectedPath
    }
    else {
        return $NULL
    }
}

##----------------------------------------------------------------------------##
## Call Main function.
##----------------------------------------------------------------------------##

Main
